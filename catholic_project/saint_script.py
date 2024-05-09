import os
import logging
import warnings
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from pymongo.server_api import ServerApi
from selenium.webdriver.common.by import By
from pymongo.mongo_client import MongoClient
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

load_dotenv()
warnings.filterwarnings("ignore")
# configure logging library
logging.basicConfig(filename='info.log', level=logging.INFO,
                    format='%(levelname)s (%(asctime)s) : %(message)s (%(lineno)d)')

# getting environment variables
uri = os.getenv("URI")

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

# items_list stores data scrapped from website
items_list = []

def get_data() -> None:
    """function gets the data from the web page
    using selenium and updates item dictionary with data
    or raises error occurred"""

    try:
        # attempt to get data of saint with about column
        saint_with_about = driver.find_elements(by=By.XPATH,
                                                value="//section[@class='section section--evidence section--isStatic']//div[@class='section__head']")
        about_saint = driver.find_elements(by=By.CLASS_NAME, value="section__content")
        # delete first data of about scrapped as it contains non-necessary information
        about_saint.pop(0)
        for num in range(len(saint_with_about)):
            # set value of key date to the current day
            items = {'date': datetime.today().strftime('%m-%d-%Y'), 'saint': '', 'about_saint': ''}
            # logging data obtained to log file
            logging.info(saint_with_about[num].text)
            logging.info(about_saint[num].text.split('Read all')[0].strip())
            # update saint and bout_saint keys in items dictionary
            items['saint']= saint_with_about[num].text
            items['about_saint']= about_saint[num].text.split('Read all')[0].strip()
            # append to items_list
            items_list.append(items)
    except Exception as e:
        logging.error(e)
    finally:
        try:
            # attempt get data of saints which come without about column
            saint_without_about = driver.find_elements(by=By.XPATH,
                                                       value="//section[@class='section section--isStatic']//div[@class='section__head']")
            for num in range(len(saint_without_about)):
                # set value of key date to the current day
                items = {'date': datetime.today().strftime('%m-%d-%Y'), 'saint': '', 'about_saint': ''}
                # log data to file
                logging.info(saint_without_about[num].text)
                # update keys with data gotten
                items['saint']=saint_without_about[num].text
                items['about_saint']="more details soon"
                #append to items_list
                items_list.append(items)
        except Exception as e:
            logging.error(e)


def send_to_database(document) -> None:
    """function connects to postgres database
     creates table in database and updates table
     with data gotten from get data function"""

    #  Connect to an existing database
    try:
        # create instance of mongodb client
        client = MongoClient(uri, server_api=ServerApi("1"))
        database = client["catholic"]
        collection = database["saints"]
        #insert documents into database
        result = collection.insert_many(document)
        print(result.acknowledged)
        client.close()
    except Exception as e:
        print("Error occured", e);

def combined():
    get_data()
    send_to_database(items_list)

if __name__ == "__main__":
    combined()


    # print(ssl.OPENSSL_VERSION)