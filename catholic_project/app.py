import os
import logging
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, abort, render_template


load_dotenv()
# setting up logger
logging.basicConfig(filename="info_app.log",level=logging.INFO,format = '%(levelname)s (%(asctime)s) : %(message)s (%(lineno)d)')
# getting environment variables
# getting environment variables
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

# instance of flask app and api created
app = Flask(__name__, template_folder="templates")

@app.route('/')
@app.route('/saints/<date>')
def get_saints(date=None) -> jsonify:
    """function connects to existing posgrest database
    and fetches data requires from requested from table
    returns a json object"""

    if date == None:
        return render_template('saints.html')

    # Connect to an existing database
    with psycopg2.connect(host="dpg-cm70icun7f5s73cbhlsg-a", dbname="catholic_saints", user="catholic_saints_user",
                          password="ISh7frD50z82acWego9uorybWQBW3aG5", port=5432) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # condition statements check the request passed in and get records from table
            if date == "all":
                sql_command = """SELECT * FROM saints"""
                cur.execute(sql_command)
            elif date == 'today':
                try:
                    date = datetime.today().strftime('%m-%d-%Y')
                    sql_command = """SELECT * FROM saints WHERE date = %s"""
                    cur.execute(sql_command, (date,))
                except Exception as e:
                    # return error 404 message letting user know data not found in database
                    # abort(404)
                    return f'Data not found for date: {date} : {e}'
            else:
                # attempt to cast passed in request to datetime and looks for corresponding record in table
                try:
                    if isinstance(datetime.strptime(date, '%m_%d_%Y'), datetime):
                        date = datetime.strptime(date, '%m_%d_%Y').strftime('%m-%d-%Y')
                        sql_command = """SELECT * FROM saints WHERE date = %s"""
                        cur.execute(sql_command, (date,))
                except Exception as e:
                    # abort(404, message=f'Data not found for date: {date} : {e}')
                    return f'Data not found for date: {date} : {e}'
            # else:
            #     abort(400, message=f'wrong input')
            #     return None

            columns = [col[0] for col in cur.description]
            data = [dict(zip(columns,data)) for data in cur.fetchall()]

    return jsonify(data)



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000,debug=False)
