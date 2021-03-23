from utils import Config

def getheaders():
    return {'Authorization': 'Bearer ' + Config.access_token, 'Content-Type': 'application/json'}
