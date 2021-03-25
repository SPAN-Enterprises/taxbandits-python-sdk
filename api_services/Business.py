import requests
from core.ForeignAddress import ForeignAddress
from core.GetBusinssList import BusinessListRequest
import json
from utils import HeaderUtils, Config, EndPointConfig
from core.CreateBusinessRequest import CreateBusinessRequest
from core.SigningAuthority import SigningAuthority

# Create the new Business
def create(businessName, einOrSSN):

    requestModel = CreateBusinessRequest()
    requestModel.set_BusinessNm("ER Systems")
    requestModel.set_IsEIN(True)
    requestModel.set_EINorSSN("003453453")
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

    saModel = SigningAuthority()
    saModel.set_SAName("Peter")
    saModel.set_SAPhone("9836476853")
    saModel.set_SABusinessMemberType("ADMINISTRATOR")

    requestModel.set_SigningAuthority(saModel)

    addressModel = ForeignAddress()
    addressModel.set_Address1("22 St")
    addressModel.set_Address2("Clair Ave E")
    addressModel.set_City("Toronto")
    addressModel.set_ProvinceOrStateNm("Ontario")
    addressModel.set_Country("M1R 0E9")
    addressModel.set_PostalCd("M1R 0E9")

    requestModel.set_ForeignAddress(addressModel)

    # inputData = json.dumps(CreateBusinessRequest.create(requestModel))
    print(f"Request Model = {requestModel}")
    # print(json.dumps(requestModel))
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_BUSINESS,
                             data=json.dumps(requestModel),
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
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS_LIST,
                            params={"Page": get_business_request.get_page(),
                                    "PageSize": get_business_request.get_page_size(),
                                    "FromDate": get_business_request.get_from_date(),
                                    "ToDate": get_business_request.get_to_date()}, headers=HeaderUtils.getheaders())

    print(response.json())
