import requests
from core.ForeignAddress import ForeignAddress
from core.GetBusinssList import BusinessListRequest
import json

from core.GetNecListRequest import GetNecListRequest
from utils import HeaderUtils, Config, EndPointConfig
from core.CreateBusinessRequest import CreateBusinessRequest
from core.SigningAuthority import SigningAuthority
from api_services import JwtGeneration


# Create the new Business
def create(requestJson):
    requestModel = CreateBusinessRequest()
    requestModel.set_BusinessNm(requestJson['business_name'][0])

    if 'is_ein' in requestJson:
        requestModel.set_IsEIN(True)
    else:
        requestModel.set_IsEIN(False)

    requestModel.set_EINorSSN(requestJson['ein_or_ssn'][0])

    if 'trade_nm' in requestJson:
        requestModel.set_TradeNm(requestJson['trade_nm'][0])

    requestModel.set_Email(requestJson['email'][0])

    if 'contact_nm' in requestJson:
        requestModel.set_ContactNm(requestJson['contact_nm'][0])

    requestModel.set_Phone(requestJson['phone'][0])

    if 'phone_extn' in requestJson:
        requestModel.set_PhoneExtn(requestJson['phone_extn'][0])

    if 'fax' in requestJson:
        requestModel.set_Fax(requestJson['fax'][0])

    if 'business_Type' in requestJson:
        requestModel.set_BusinessType(requestJson['business_Type'][0])
    else:
        requestModel.set_BusinessType('ESTE')

    if 'kind_of_employer' in requestJson:
        requestModel.set_KindOfEmployer(requestJson['kind_of_employer'][0])
    else:
        requestModel.set_KindOfEmployer('FEDERALGOVT')

    if 'kind_of_payer' in requestJson:
        requestModel.set_KindOfPayer(requestJson['kind_of_payer'][0])
    else:
        requestModel.set_KindOfPayer('REGULAR941')

    if 'is_business_terminated' in requestJson:
        requestModel.set_IsBusinessTerminated(True)
    else:
        requestModel.set_IsBusinessTerminated(False)

    addressModel = ForeignAddress()

    if 'is_foreign' in requestJson:
        requestModel.set_IsForeign(True)
        addressModel.set_Address1(requestJson['address1'][0])
        addressModel.set_Address2(requestJson['address2'][0])
        addressModel.set_City(requestJson['city'][0])
        addressModel.set_ProvinceOrStateNm(requestJson['state'][0])
        addressModel.set_Country(requestJson['country'][0])
        addressModel.set_PostalCd(requestJson['zip_cd'][0])
        requestModel.set_ForeignAddress(addressModel.__dict__)
    else:
        requestModel.set_IsForeign(False)
        addressModel.set_Address1(requestJson['address1'][0])
        addressModel.set_Address2(requestJson['address2'][0])
        addressModel.set_City(requestJson['city'][0])
        addressModel.set_State(requestJson['state_drop_down'][0])
        addressModel.set_ZipCd(requestJson['zip_cd'][0])
        requestModel.set_USAddress(addressModel.__dict__)

    saModel = SigningAuthority()

    if 'sa_name' in requestJson:
        saModel.set_SAName(requestJson['sa_name'][0])

    if 'sa_phone' in requestJson:
        saModel.set_SAPhone(requestJson['sa_phone'][0])

    if 'business_member_type' in requestJson:
        saModel.set_SABusinessMemberType(requestJson['business_member_type'][0])

    else:
        saModel.set_SABusinessMemberType('ADMINISTRATOR')

    requestModel.set_SigningAuthority(saModel.__dict__)

    # inputData = json.dumps(CreateBusinessRequest.create(requestModel))

    convertedModel = json.dumps(requestModel.__dict__)

    print(f"Request Model = {convertedModel}")
    # print(json.dumps(requestModel))
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_BUSINESS,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    print(f'statuscode = {response.status_code}')
    print(f'response header = {response}')

    if response.status_code == 200:
        json_obj = json.loads(response.text)
        return json_obj
    else:
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

    return response.json()


# Get NEC List by business_id
def get_nec_list(get_list_request: GetNecListRequest):
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_FORM_1099NEC_LIST,
                            params={"Page": get_list_request.get_page(),
                                    "PageSize": get_list_request.get_page_size(),
                                    "FromDate": get_list_request.get_from_date(),
                                    "BusinessId": get_list_request.get_business_id(),
                                    "ToDate": get_list_request.get_to_date()}, headers=HeaderUtils.getheaders())

    return response.json()
