import json
import ssl
import pymongo


def save_response_in_mongodb(response):
    client = pymongo.MongoClient(
        "mongodb+srv://<username>:<password>@cluster0.kaf9y.mongodb.net/<database_name>?retryWrites=true&w=majority&authSource=admin",
        ssl_cert_reqs=ssl.CERT_NONE)
    my_database = client["<database_name>"]
    my_collection = my_database["<collection_name>"]
    entity = json.loads(response)
    return my_collection.save(entity)