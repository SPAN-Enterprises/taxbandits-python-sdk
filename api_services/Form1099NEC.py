import requests
import json

from core import GetFormListRequest
from core.ScheduleFiling import ScheduleFiling
from utils import HeaderUtils, Config, EndPointConfig
from api_services import JwtGeneration
from core.CreateForm1099NEC import CreateForm1099NEC
from core.SubmissionManifest import SubmissionManifest
from core.States import States
from core.ReturnHeader import ReturnHeader
from core.ReturnData import ReturnData
from core.NECFormData import NECFormData
from core.Recipient import Recipient
from core.ForeignAddress import ForeignAddress
from core.TransmitFormRequest import TransmitFormRequest
from core.Business import Business
from core.USAddress import USAddress


def create(businessId, rName, rTIN, amount, recipientId):
    requestModel = CreateForm1099NEC()

    returnHeader = ReturnHeader()

    business = Business()
    # businessModel.set_BusinessId("0fd6e0a3-f122-4cdc-a4da-25cb155010e1")
    business.set_BusinessId(businessId)
    returnHeader.set_Business(business.__dict__)
    requestModel.set_ReturnHeader(returnHeader.__dict__)

    submissionManifest = SubmissionManifest()
    # submissionManifest.set_SubmissionId(null)
    submissionManifest.set_TaxYear(2020)
    submissionManifest.set_IsFederalFiling(2020)
    submissionManifest.set_IsStateFiling(True)
    submissionManifest.set_IsPostal(True)
    submissionManifest.set_IsOnlineAccess(True)
    submissionManifest.set_IsTinMatching(True)
    submissionManifest.set_IsScheduleFiling(True)
    scheduleFiling = ScheduleFiling()
    scheduleFiling.set_EfileDate("04/21/2021")
    submissionManifest.set_ScheduleFiling(scheduleFiling.__dict__)
    requestModel.set_SubmissionManifest(submissionManifest.__dict__)
    returnDataList = []
    returnData = ReturnData()
    # returnData.set_RecordId(null)
    returnData.set_SequenceId("1")
    # set Recipient data
    recipientModel = Recipient()
    if recipientId != '-1':
        recipientModel.set_RecipientId(recipientId)
    else:
        recipientModel.set_RecipientId('')

    recipientModel.set_TINType("EIN")
    recipientModel.set_TIN(rTIN)
    recipientModel.set_FirstPayeeNm(rName)
    recipientModel.set_SecondPayeeNm("")
    recipientModel.set_IsForeign(False)
    usAddress = USAddress()
    usAddress.set_Address1("1751 Kinsey Rd")
    usAddress.set_Address2("Main St")
    usAddress.set_City("Dothan")
    usAddress.set_State("AL")
    usAddress.set_ZipCd("36303")
    recipientModel.set_USAddress(usAddress.__dict__)
    # recipientModel.set_ForeignAddress(null)
    recipientModel.set_Email("sharmila.k@dotnetethics.com")
    recipientModel.set_Fax("1234567890")
    recipientModel.set_Phone("1234567890")
    returnData.set_Recipient(recipientModel.__dict__)
    # set NEC data
    necFormDataModel = NECFormData()
    necFormDataModel.set_B1NEC(amount)
    necFormDataModel.set_B4FedTaxWH(54.12)
    necFormDataModel.set_IsFATCA(True)
    necFormDataModel.set_Is2ndTINnot(True)
    necFormDataModel.set_AccountNum("20123130000009000001")
    statesList = []
    stateModel = States()
    stateModel.set_StateCd("PA")
    stateModel.set_StateWH(15)
    stateModel.set_StateIdNum("99999999")
    stateModel.set_StateIncome(16)
    statesList.append(stateModel.__dict__)  # State 1
    stateModel = States()
    stateModel.set_StateCd("AZ")
    stateModel.set_StateWH(17)
    stateModel.set_StateIdNum("99-999999")
    stateModel.set_StateIncome(18)
    statesList.append(stateModel.__dict__)  # State 2
    necFormDataModel.set_States(statesList)

    returnData.set_NECFormData(necFormDataModel.__dict__)
    returnData.set_MISCFormData(None)
    returnDataList.append(returnData.__dict__)

    requestModel.set_ReturnData(returnDataList)

    # Create a new Form 1099-NEC
    # Method: Form1099NEC/Create (POST)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM1099_NEC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response


# Returns Form 1099-NEC list of specific business
def getForm1099NECList(businessId):

    # Get NEC list of specific Business Id
    # Method: Form1099NEC/List (GET)
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_FORM1099_NEC_LIST,
                            params={"BusinessId": businessId}, headers=HeaderUtils.getheaders())

    return response.json()


# Transmits Form 1099-NEC
def transmitForm1099NEC(submissionId, recordId):
    requestModel = TransmitFormRequest()

    requestModel.set_SubmissionId(submissionId)
    requestModel.set_RecordIds(recordId)

    # Transmits a particular Form 1099-NEC
    # Method: Form1099NEC/Transmit (POST)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.TRANSMIT_FORM_1099NEC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


# Returns NEC List of specific business Id
def get_nec_list(get_list_request: GetNecListRequest):

    # Get NEC list of specific Business Id
    # Method: Form1099NEC/List (GET)
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_FORM_1099NEC_LIST,
                            params={"Page": get_list_request.get_page(),
                                    "PageSize": get_list_request.get_page_size(),
                                    "FromDate": get_list_request.get_from_date(),
                                    "BusinessId": get_list_request.get_business_id(),
                                    "ToDate": get_list_request.get_to_date()}, headers=HeaderUtils.getheaders())
    return response.json()


def get_pdf(SubmissionId, RecordIds, TINMaskType):

    # Get Form-1099 NEC PDF of particular submission Id and its Record Id
    # Method: Form1099NEC/GetPDF
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_PDF,
                            params={"SubmissionId": SubmissionId,
                                    "RecordIds": RecordIds,
                                    "TINMaskType": TINMaskType}, headers=HeaderUtils.getheaders())

    return response.json()
