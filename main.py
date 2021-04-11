import base64
import ssl
import threading
import os
import pymongo
import json
from flask import Flask, request
from pyngrok import ngrok
import hmac
import hashlib
from utils import Config


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
    entity = json.loads(response)
    mycol.save(entity)


@app.route("/getWebhook", methods=['POST'])
def getWebhook():
    json_content = request.json
    response = json.dumps(json_content)
    Timestamp = request.headers.get('Timestamp')
    Signature = request.headers.get('Signature')


    isSignatureValid = validate(Timestamp, Signature)

    if isSignatureValid:
        saveResponseInMongoDb(response)


# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()


def validate(Timestamp, Signature):
    message = Config.userCredential["CLIENT_ID"] + "\n" + Timestamp

    digest = hmac.new(Config.userCredential["SECRET_ID"].encode('utf-8'),
                      msg=message.encode('utf-8'),
                      digestmod=hashlib.sha256
                      ).digest()
    signature = base64.b64encode(digest).decode()



    if (signature == Signature):
        return True
    else:
        return False
