from api_services import JwtGeneration
from utils import Config


def getheaders():
    if Config.access_token is None or len(Config.access_token) == 0:
        jws = JwtGeneration.get_jws()

        JwtGeneration.get_access_token_by_jws(jws)

    return {'Authorization': 'Bearer ' + Config.access_token, 'Content-Type': 'application/json'}
