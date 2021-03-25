import requests

from core import SigningAuthority, ForeignAddress

from core.GetBusinssList import BusinessListRequest
import json

from utils import HeaderUtils, Config, EndPointConfig
from core.CreateBusinessRequest import CreateBusinessRequest


# Create the new Business
def create(businessName, einOrSSN):

    requestModel = CreateBusinessRequest()
    requestModel.set_BusinessNm(businessName)
    requestModel.set_IsEIN(True)
    requestModel.set_EINorSSN(einOrSSN)
    requestModel.set_TradeNm("kodak")
    requestModel.set_Email("sharmila.k@dotnetethics.com")
    requestModel.set_ContactNm("John")
    requestModel.set_Phone("1234567890")
    requestModel.set_PhoneExtn("12345")
    requestModel.set_Fax("1234567890")
    requestModel.set_BusinessType("ESTE")
    requestModel.set_KindOfEmployer("FEDERALGOVT")
    requestModel.set_KindOfPayer("REGULAR941")
    requestModel.set_IsBusinessTerminated(False)
    requestModel.set_IsForeign(True)

    saModel = SigningAuthority.signingAuthority

    requestModel.set_SigningAuthority(saModel)

    addressModel = ForeignAddress.foreignAddress


    requestModel.set_ForeignAddress(addressModel)

   # inputData = json.dumps(CreateBusinessRequest.create(requestModel))


    print(f"Request Model = {json.dumps(requestModel.get_Fax())}")

    print(json.dumps(requestModel.__dict__))
    # print(json.dumps(requestModel))
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_BUSINESS,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()


# Get Business Information by using BusinessId and EIN
def get_business_detail(BusinessId, EIN):
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS,
                            params={"BusinessId": BusinessId, "EIN": EIN}, headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()


# Get Business List
def get_business_list(get_business_request: BusinessListRequest):
    return requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS_LIST,
                            params={"Page": get_business_request.get_page(),
                                    "PageSize": get_business_request.get_page_size(),
                                    "FromDate": get_business_request.get_from_date(),
                                    "ToDate": get_business_request.get_to_date()}, headers=HeaderUtils.getheaders()).json()

