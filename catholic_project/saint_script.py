import os
import json
import logging
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

load_dotenv()
# configure logging library
logging.basicConfig(filename='info.log', level=logging.INFO,
                    format='%(levelname)s (%(asctime)s) : %(message)s (%(lineno)d)')

# getting environment variables
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

# setting up driver for selenium used for scrapping data
options = webdriver.ChromeOptions()
# headless argument removes need of chrome browser instance from running before scrapping is done
options.add_argument('headless')
# argument passed in service ensures webdriver is automatically uodated with chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.set_window_size(1120, 1000)
driver.get('https://www.vaticannews.va/en/saints.html')
# wait 30s to find element before returning error if not found
driver.implicitly_wait(30)

# items dictionary stores data scrapped from website
items = {'date': '', 'saint': [], 'about_saint': []}


def get_data() -> None:
    """function gets the data from the web page
    using selenium and updates item dictionary with data
    or raises error occurred"""

    # set value of key date to the current day
    items['date'] = datetime.today().strftime('%m-%d-%Y')
    try:
        # attempt to get data of saint with about column
        saint_with_about = driver.find_elements(by=By.XPATH,
                                                value="//section[@class='section section--evidence section--isStatic']//div[@class='section__head']")
        about_saint = driver.find_elements(by=By.CLASS_NAME, value="section__content")
        # delete first data of about scrapped as it contains non-necessary information
        about_saint.pop(0)
        for num in range(len(saint_with_about)):
            # logging data obtained to log file
            logging.info(saint_with_about[num].text)
            logging.info(about_saint[num].text.split('Read all')[0].strip())
            # update saint and bout_saint keys in items dictionary
            items['saint'].append(saint_with_about[num].text)
            items['about_saint'].append(about_saint[num].text.split('Read all')[0].strip())
    except Exception as e:
        logging.error(e)
    finally:
        try:
            # attempt get data of saints which come without about column
            saint_without_about = driver.find_elements(by=By.XPATH,
                                                       value="//section[@class='section section--isStatic']//div[@class='section__head']")
            for num in range(len(saint_without_about)):
                # log data to file
                logging.info(saint_without_about[num].text)
                # update keys with data gotten
                items['saint'].append(saint_without_about[num].text)
                items['about_saint'].append("more details soon")
        except Exception as e:
            logging.error(e)


def send_to_database() -> None:
    """function connects to postgres database
    creates table in database and updates table
    with data gotten from get data function"""

    # Connect to an existing database
    with psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            create_table = """CREATE TABLE IF NOT EXISTS saints(
                            id int NOT NULL generated always as identity,
                            saint_of_the_day VARCHAR(255) UNIQUE,
                            about_saint text,
                            date VARCHAR(255),
                            PRIMARY KEY (id,saint_of_the_day)
                            )"""
            cur.execute(create_table)

            # sql command: this inserts into created table if the data does not already exist
            insert_table = """INSERT INTO saints(
                            saint_of_the_day,
                            about_saint,
                            date
                            )values (%s,%s,%s) ON CONFLICT(saint_of_the_day) DO NOTHING"""

            # loop over data content in items dictionary and execute insert command
            for row in range(len(items['saint'])):
                cur.execute(insert_table, (items['saint'][row],
                                           items['about_saint'][row],
                                           items['date']))


if __name__ == "__main__":
    get_data()
    send_to_database()
