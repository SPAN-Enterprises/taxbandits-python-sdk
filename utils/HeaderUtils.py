from api_services import JwtGeneration
from utils import Config


def getheaders():
    if Config.ACCESS_TOKEN is None or len(Config.ACCESS_TOKEN) == 0:
        jws = JwtGeneration.get_jws()

        JwtGeneration.get_access_token_by_jws(jws)

    return {'Authorization': 'Bearer ' + Config.ACCESS_TOKEN, 'Content-Type': 'application/json'}
