from utils import Config
import jwt
import time
import requests


# get JWT Token by using user credential
def get_jwt_token():
    epoch_time = int(time.time())

    payload = {"iss": Config.userCredential["CLIENT_ID"], "sub": Config.userCredential["CLIENT_ID"],
               "aud": Config.userCredential["USER_TOKEN"], "iat": epoch_time}

    print(f"Time = {epoch_time}")

    return jwt.encode(payload, Config.userCredential["SECRET_ID"], algorithm="HS256")


# get Access token by using jwt token
def get_access_token_by_jwt_token(jwtToken):
    headers = {'Authentication': jwtToken, 'Content-Type': 'application/json'}

    response = requests.get(Config.apiBaseUrls["O_AUTH_BASE_URL"], headers=headers)

    if response.status_code == 200:

        Config.access_token = response.json()['AccessToken']

    # return response.json()['AccessToken']

    else:

        print(response.status_code)
