import json
import pymongo
from os.path import dirname, abspath


## --- MONGO DATA
collection_name = 'youtubetest'
url ='127.0.0.1:27017'
db_name = 'webscrape'


def upload_file(file_path: str):
    #Connect to MongoDB
    client = pymongo.MongoClient()
    db = client[db_name]

    #Get data
    data = json.load(open(file_path, 'r', encoding='utf-8'))

    # Insert data into MongoDB collection
    collection = db[collection_name]
    collection.insert_one(data)

    # Close MongoDB connection
    client.close()

keyword = 'chatGPT'
upload_file(f"{dirname(abspath(__file__))}\youtube-{keyword}.json")
