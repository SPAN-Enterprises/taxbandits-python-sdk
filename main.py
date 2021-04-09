from flask import Flask
from pyngrok import ngrok


appInstance = Flask(__name__)

public_url = ngrok.connect(port='80')
print (public_url)

