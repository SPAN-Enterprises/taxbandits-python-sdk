from utils import Config
import jwt
import time
import requests


# Generate JWS using the Client Id, Secret Id and User Token
def get_jwt_token():

    epoch_time = int(time.time())  # current UTC time in milliseconds

    payload = {"iss": Config.userCredential["CLIENT_ID"],  # Issuer: Client ID retrieved from the console site
               "sub": Config.userCredential["CLIENT_ID"],  # Subject: Client ID retrieved from the console site
               "aud": Config.userCredential["USER_TOKEN"],  # Audience: User Token retrieved from the console site
               "iat": epoch_time  # Issued at: Number of seconds from Jan 1 1970 00:00:00 (Unix epoch format)
               }

    jws = jwt.encode(payload, Config.userCredential["SECRET_ID"], algorithm="HS256")  # JWS generation using HS256 algorithm

    print(jws)

    return jws


# Returns the Access token generated using JWS
def get_access_token_by_jwt_token():

    jwtToken = get_jwt_token()

    headers = {'Authentication': jwtToken, 'Content-Type': 'application/json'}

    response = requests.get(Config.apiBaseUrls["O_AUTH_BASE_URL"], headers=headers)

    if response.status_code == 200:

        Config.access_token = response.json()['AccessToken']

        accessToken = response.json()['AccessToken']

        print(f"\nAccess Token = {accessToken}")

        return accessToken

    else:

        print(response.status_code)
