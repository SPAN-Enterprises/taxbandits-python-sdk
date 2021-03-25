import requests
from core import CreateBusinessRequest
import json
from utils import HeaderUtils, Config, EndPointConfig


# Create the new Business
def create(businessName, einOrSSN):
    inputData = json.dumps(CreateBusinessRequest.create(businessName, einOrSSN))
    print(json.dumps(inputData))
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_BUSINESS,
                             data=json.dumps(CreateBusinessRequest.create(businessName, einOrSSN)),
                             headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()


# Get Business Information by using BusinessId and EIN
def get_business_detail(BusinessId, EIN):

    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS,
                            params={"BusinessId": BusinessId, "EIN": EIN}, headers=HeaderUtils.getheaders())

    print(response.json())

    return  response.json()
