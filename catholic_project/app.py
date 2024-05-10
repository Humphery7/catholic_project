import os
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask,jsonify, abort, render_template
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient


load_dotenv()
uri = os.getenv("URI")
app = Flask(__name__,template_folder="templates")

@app.route('/')
@app.route('/saints/<date>',methods=['GET'])
def get_saints(date=None) -> jsonify:
    global results
    if date == None:
        #return home page if no date is specified
        return render_template("saints.html")
    elif date == "all":
        try:
            #connecting to mongodb cluster
            client = MongoClient(uri,server_api = ServerApi("1"))
            database = client['catholic']
            collection  = database['saints']
            #find all documents in collection
            results = collection.find({},{"_id":0})
        except Exception as e:
            return f'Data not found for date: {date} : {e}'
    elif date == 'today':
        try:
            client = MongoClient(uri,server_api = ServerApi("1"))
            database = client['catholic']
            collection  = database['saints']
            date = datetime.today().strftime('%m-%d-%Y')
            filter_ = {'date':date}
            # find all documents in collection
            results = collection.find(filter_,{"_id":0})
        except Exception as e:
            return f'Data not found for date: {date} : {e}'
    else:
        try:
            if isinstance(datetime.strptime(date, '%m_%d_%Y'), datetime):
                #converting passed in date to string format
                date = datetime.strptime(date, '%m_%d_%Y').strftime('%m-%d-%Y')
                client = MongoClient(uri,server_api = ServerApi("1"))
                database = client['catholic']
                collection  = database['saints']
                filter_ = {'date': date}
                #find documents with specified date
                results = collection.find(filter_,{"_id":0})
        except Exception as e:
            return f'Data not found for date: {date} : {e}'


    document_list = [doc for doc in results]
    return jsonify(document_list)

if __name__ == "__main__":
    app.run(debug=True)

# date = "5_5_2024"
# if isinstance(datetime.strptime(date, '%m_%d_%Y'), datetime):
#     #converting passed in date to string format
#     date = datetime.strptime(date, '%m_%d_%Y').strftime('%m-%d-%Y')
#     print(date)