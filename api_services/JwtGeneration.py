from utils import Config
import jwt
import time
import requests


# Generate JWS using the Client Id, Secret Id and User Token
def get_jws():

    epoch_time = int(time.time())  # current UTC time in milliseconds

    payload = {"iss": Config.userCredential["CLIENT_ID"],  # Issuer: Client ID retrieved from the console site
               # Subject: Client ID retrieved from the console site
               "sub": Config.userCredential["CLIENT_ID"],
               # Audience: User Token retrieved from the console site
               "aud": Config.userCredential["USER_TOKEN"],
               # Issued at: Number of seconds from Jan 1 1970 00:00:00 (Unix epoch format)
               "iat": epoch_time
               }

    # JWS generation using HS256 algorithm
    jws = jwt.encode(
        payload, Config.userCredential["SECRET_ID"], algorithm="HS256")
    print("JWS: " + jws)  # Print JWS
    return jws


# Returns the Access token generated using JWS
def get_access_token_by_jws(jws):

    headers = {'Authentication': jws,  # Generated JWS
               'Content-Type': 'application/json'}

    response = requests.get(
        Config.apiBaseUrls["O_AUTH_BASE_URL"], headers=headers)

    if response.status_code == 200:

        accessToken = response.json()['AccessToken']

        Config.access_token = accessToken
        print("Access Token: " + accessToken)  # Print Access Token
        return accessToken

    else:

        print(response.status_code)
