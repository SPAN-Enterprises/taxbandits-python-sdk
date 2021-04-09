import threading
import os

import json
from flask import Flask, request, render_template
from pyngrok import ngrok

os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
port = 5000

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url+"/getWebhook"
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/getWebhook\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url

# ... Update inbound traffic via APIs to use the public-facing ngrok URL


# Define Flask routes
@app.route("/getWebhook")
def index():
    json_content = request.json
    print (json.dumps(json_content))
    return "EMPTY"


@app.route("/getWebhook" , methods=['POST'])
def index1():
    json_content = request.json
    print ("index1"+json.dumps(json_content))
    return render_template('success.html',
                           response='StatusMessage=' +"Success" + '<br>BusinessId =' +
                                    "Business", ErrorMessage=' Business Created Successfully')


@app.route("/getWebhook" , methods=['GET'])
def index2():
    json_content = request.json
    print ("index2"+json.dumps(json_content))
    return "POST"

# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()


