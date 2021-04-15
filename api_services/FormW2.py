import json
import requests
from core.CreateFormW2Request import CreateFormW2Request
from core.Business import Business
from core.Employee import Employee
from core.USAddress import USAddress
from core.SubmissionManifest import SubmissionManifest
from core.W2FormData import FormDetails
from core.ReturnHeader import ReturnHeader
from core.GetFormListRequest import GetFormListRequest
from core.ReturnDataFormW2 import ReturnDataFormW2
from core.TransmitFormRequest import TransmitFormRequest
from utils import HeaderUtils, Config, EndPointConfig


def generate_form_w2_request(requestJson):
    createFormW2Request = CreateFormW2Request()

    submissionManifest = SubmissionManifest()
    submissionManifest.set_TaxYear(2020)
    submissionManifest.set_IsFederalFiling(True)
    submissionManifest.set_IsStateFiling(False)
    submissionManifest.set_IsPostal(True)
    submissionManifest.set_IsOnlineAccess(False)
    submissionManifest.set_IsTinMatching(False)
    submissionManifest.set_IsScheduleFiling(False)
    scheduleFiling = SubmissionManifest()
    scheduleFiling.set_EfileDate("05/21/2021")
    submissionManifest.set_ScheduleFiling(None)

    createFormW2Request.set_SubmissionManifest(submissionManifest.__dict__)

    returnHeader = ReturnHeader()

    business = Business()
    business.set_BusinessNm(requestJson['W2Forms[0].Business.BusinessNm'][0])
    business.set_EINorSSN(requestJson['W2Forms[0].Business.EINorSSN'][0])
    business.set_ContactNm(requestJson['W2Forms[0].Business.ContactNm'][0])
    business.set_Phone(requestJson['W2Forms[0].Business.Phone'][0])
    business.set_Email(requestJson['W2Forms[0].Business.Email'][0])
    business.set_Email(requestJson['W2Forms[0].Business.Email'][0])
    business.set_KindOfPayer(requestJson['W2Forms[0].Business.KindOfPayer'][0])
    business.set_KindOfEmployer(requestJson['W2Forms[0].Business.KindOfEmployer'][0])
    business.set_IsEIN(True)
    business.set_IsForeign(False)
    usAddress = USAddress()
    usAddress.set_Address1("1751 Kinsey Rd")
    usAddress.set_Address2("Main St")
    usAddress.set_City("Dothan")
    usAddress.set_State("AL")
    usAddress.set_ZipCd("36303")
    business.set_USAddress(usAddress.__dict__)

    returnHeader.set_Business(business.__dict__)

    createFormW2Request.set_ReturnHeader(returnHeader.__dict__)

    returnDataList = []

    returnData = ReturnDataFormW2()

    returnData.set_RecordId(None)
    returnData.set_SequenceId(1)
    employee = Employee()
    employee.set_FirstNm(requestJson['W2Forms[0].Employee.FirstNm'][0])
    employee.set_LastNm(requestJson['W2Forms[0].Employee.LastNm'][0])
    employee.set_MiddleNm(requestJson['W2Forms[0].Employee.MiddleNm'][0])
    employee.set_MiddleNm(requestJson['W2Forms[0].Employee.Suffix'][0])
    employee.set_SSN(requestJson['W2Forms[0].Employee.SSN'][0])
    employee.set_Phone(requestJson['W2Forms[0].Employee.Phone'][0])
    employee.set_Email(requestJson['W2Forms[0].Employee.Email'][0])

    usAddress = USAddress()
    usAddress.set_Address1("1751 Kinsey Rd")
    usAddress.set_Address2("Main St")
    usAddress.set_City("Dothan")
    usAddress.set_State("NC")
    usAddress.set_ZipCd("28201")
    employee.set_USAddress(usAddress.__dict__)
    returnData.set_Employee(employee.__dict__)

    formDetails = FormDetails()
    formDetails.set_B1Wages(requestJson['W2Forms[0].FormDetails.Box1'][0])
    formDetails.set_B2FedTaxWH(requestJson['W2Forms[0].FormDetails.Box2'][0])
    formDetails.set_B3SocSecWages(requestJson['W2Forms[0].FormDetails.Box3'][0])
    formDetails.set_B4SocSecTaxWH(requestJson['W2Forms[0].FormDetails.Box4'][0])
    returnData.set_W2FormData(formDetails.__dict__)

    returnDataList.append(returnData.__dict__)
    createFormW2Request.set_ReturnData(returnDataList)

    print(json.dumps(createFormW2Request.__dict__))

    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM_W2,
                             data=json.dumps(createFormW2Request.__dict__),
                             headers=HeaderUtils.getheaders())

    print(response.status_code)

    print(response.json())
    return response.json()


# Get W2 List by business_id
def get_w2_list(get_request: GetFormListRequest):
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.LIST_FORM_W2,
                            params={"Page": get_request.get_page(),
                                    "PageSize": get_request.get_page_size(),
                                    "FromDate": get_request.get_from_date(),
                                    "BusinessId": get_request.get_business_id(),
                                    "ToDate": get_request.get_to_date()}, headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()


def transmit_formw2(submissionId):
    requestModel = TransmitFormRequest()
    requestModel.set_SubmissionId(submissionId)

    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.TRANSMIT_FORM_W2,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


def get_w2_pdf(SubmissionId, RecordIds, TINMaskType):
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.FORM_W2_GET_PDF,
                            params={"SubmissionId": SubmissionId,
                                    "RecordIds": RecordIds,
                                    "TINMaskType": TINMaskType}, headers=HeaderUtils.getheaders())

    return response.json()