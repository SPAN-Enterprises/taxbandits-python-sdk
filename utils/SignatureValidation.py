import base64
import hashlib
import hmac
from utils import Config


def validate(Timestamp, Signature):
    message = Config.userCredential["CLIENT_ID"] + "\n" + Timestamp
    print(message)
    digest = hmac.new(Config.userCredential["SECRET_ID"].encode('utf-8'),
                      msg=message.encode('utf-8'),
                      digestmod=hashlib.sha256
                      ).digest()
    signature = base64.b64encode(digest).decode()

    print(signature)

    if (signature == Signature):
        return True
    else:
        return False