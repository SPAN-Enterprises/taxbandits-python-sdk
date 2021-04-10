import json
import ssl
import pymongo


def save_response_in_mongodb(response):
    client = pymongo.MongoClient(
        "mongodb+srv://subbuleaf:d$$9943111606@cluster0.kaf9y.mongodb.net/pythonSDK?retryWrites=true&w=majority&authSource=admin",
        ssl_cert_reqs=ssl.CERT_NONE)
    my_database = client["pythonSDK"]
    my_collection = my_database["FormNEC"]
    print(response)
    entity = json.loads(response)
    my_collection.save(entity)