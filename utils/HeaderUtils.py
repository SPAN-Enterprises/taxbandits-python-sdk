from api_services import JwtGeneration
from utils import Config


def getheaders():
    if Config.access_token is None or len(Config.access_token) == 0:
        jwtToken = JwtGeneration.get_jwt_token()

        JwtGeneration.get_access_token_by_jwt_token(jwtToken)

    return {'Authorization': 'Bearer ' + Config.access_token, 'Content-Type': 'application/json'}
