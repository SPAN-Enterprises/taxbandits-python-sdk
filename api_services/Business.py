import requests
import json
from utils import HeaderUtils, Config, EndPointConfig
from models.BusinessListRequest import BusinessListRequest


def create(requestModel):
    # Creates a new Business and returns Business Id on successful creation
    # Method: Business/Create (POST)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_BUSINESS,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return response.json()


# Returns a particular business
def get_business_detail(BusinessId, EIN):
    # Gets particular Business information by using BusinessId and EIN
    # Method: Business/Get?BusinessId (GET)
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS,
                            params={"BusinessId": BusinessId, "EIN": EIN}, headers=HeaderUtils.getheaders())

    return response.json()


# Returns list of all the businesses
def get_business_list(get_business_request: BusinessListRequest):
    # Get a list of all Businesses
    # Method: Business/List (GET)
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS_LIST,
                            params={"Page": get_business_request.get_page(),
                                    "PageSize": get_business_request.get_page_size(),
                                    "FromDate": get_business_request.get_from_date(),
                                    "ToDate": get_business_request.get_to_date()}, headers=HeaderUtils.getheaders())

    return response.json()
