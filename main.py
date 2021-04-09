import base64
import ssl
import threading
import os

import bson
import pymongo
import requests
import json
from flask import Flask, request, render_template
from pyngrok import ngrok
import hmac
import hashlib

from core.WebHookResponse import WebHookResponse
from utils import Config
import pprint
from pprint import pprint

os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
port = 5000

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url + "/getWebhook"
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/getWebhook\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url


# ... Update inbound traffic via APIs to use the public-facing ngrok URL


def saveResponseInMongoDb(response):
    client = pymongo.MongoClient("mongodb+srv://subbuleaf:d$$9943111606@cluster0.kaf9y.mongodb.net/pythonSDK?retryWrites=true&w=majority&authSource=admin",ssl_cert_reqs=ssl.CERT_NONE)
    mydb = client["pythonSDK"]
    mycol = mydb["FormNEC"]
    print(response)
    entity = json.loads(response)
    mycol.save(entity)


@app.route("/getWebhook", methods=['POST'])
def getWebhook():
    json_content = request.json
    response = json.dumps(json_content)
    print("response" + response)
    Timestamp = request.headers.get('Timestamp')
    Signature = request.headers.get('Signature')

    print("Signature " + Signature + "Timestamp " + Timestamp)

    isSignatureValid = validate(Timestamp, Signature)

    if isSignatureValid:
        saveResponseInMongoDb(response)


# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()


def validate(Timestamp, Signature):
    message = Config.userCredential["CLIENT_ID"] + "\n" + Timestamp
    print(message)
    digest = hmac.new(Config.userCredential["SECRET_ID"].encode('utf-8'),
                      msg=message.encode('utf-8'),
                      digestmod=hashlib.sha256
                      ).digest()
    signature = base64.b64encode(digest).decode()

    print(signature)

    if (signature == Signature):
        return True
    else:
        return False
