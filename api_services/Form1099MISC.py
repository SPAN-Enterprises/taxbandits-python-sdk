import json

import requests

from core import GetNecListRequest
from core.CreateBusinessRequest import CreateBusinessRequest
from core.CreateForm1099NECModel import CreateForm1099NECModel
from core.ForeignAddress import ForeignAddress
from core.MISCFormDataModel import MISCFormDataModel
from core.RecipientModel import RecipientModel
from core.ReturnDataModel import ReturnDataModel
from core.ReturnHeaderModel import ReturnHeaderModel
from core.StatesModel import StatesModel
from core.SubmissionManifestModel import SubmissionManifestModel
from core.TransmitForm1099NECModel import TransmitForm1099NECModel
from utils import HeaderUtils, Config, EndPointConfig


def isValidString(param):
    return param is not None and len(param) > 0


def create(formRequest: json):
    requestModel = CreateForm1099NECModel()

    returnHeader = ReturnHeaderModel()
    businessModel = CreateBusinessRequest()

    if 'business_list' in formRequest:
        businessModel.set_BusinessId(formRequest['business_list'][0])
    returnHeader.set_Business(businessModel.__dict__)
    requestModel.set_ReturnHeader(returnHeader.__dict__)

    submissionManifest = SubmissionManifestModel()
    submissionManifest.set_TaxYear(2020)
    submissionManifest.set_IsFederalFiling(2020)
    submissionManifest.set_IsStateFiling(True)
    submissionManifest.set_IsPostal(True)
    submissionManifest.set_IsOnlineAccess(True)
    submissionManifest.set_IsTinMatching(True)
    submissionManifest.set_IsScheduleFiling(True)
    scheduleFiling = SubmissionManifestModel()
    scheduleFiling.set_EfileDate("04/21/2021")
    submissionManifest.set_ScheduleFiling(scheduleFiling.__dict__)
    requestModel.set_SubmissionManifest(submissionManifest.__dict__)
    returnDataList = []
    returnData = ReturnDataModel()
    # returnData.set_RecordId(null)
    returnData.set_SequenceId("1")
    # set Recipient data
    recipientModel = RecipientModel()
    recipientId = -1

    if 'recipientsDropDown' in formRequest:
        recipientId = formRequest['recipientsDropDown'][0]

    if recipientId != '-1':
        recipientModel.set_RecipientId(recipientId)
    else:
        recipientModel.set_RecipientId('')

    recipientModel.set_TINType("EIN")

    if 'rTIN' in formRequest and formRequest['rTIN']:
        recipientModel.set_TIN(formRequest['rTIN'][0])

    if 'rName' in formRequest:
        recipientModel.set_FirstPayeeNm(formRequest['rName'][0])

    recipientModel.set_SecondPayeeNm("")
    recipientModel.set_IsForeign(False)
    usAddress = ForeignAddress()
    usAddress.set_Address1("1751 Kinsey Rd")
    usAddress.set_Address2("Main St")
    usAddress.set_City("Dothan")
    usAddress.set_State("AL")
    usAddress.set_ZipCd("36303")
    recipientModel.set_USAddress(usAddress.__dict__)
    recipientModel.set_Email("sharmila.k@dotnetethics.com")
    recipientModel.set_Fax("1234567890")
    recipientModel.set_Phone("1234567890")
    returnData.set_Recipient(recipientModel.__dict__)
    # set NEC data
    miscFormDataModel = MISCFormDataModel()

    if 'rentsAmt' in formRequest and formRequest['rentsAmt'] is not None and isValidString(formRequest['rentsAmt'][0]):
        miscFormDataModel.set_B1Rents(float(formRequest['rentsAmt'][0]))

    if 'royaltiesAmt' in formRequest and formRequest['royaltiesAmt'] is not None and isValidString(formRequest['royaltiesAmt'][0]):
        miscFormDataModel.set_B2Royalties(float(formRequest['royaltiesAmt'][0]))

    if 'otherIncomeAmt' in formRequest and formRequest['otherIncomeAmt'] is not None and isValidString(formRequest['otherIncomeAmt'][0]):
        miscFormDataModel.set_B3OtherIncome(float(formRequest['otherIncomeAmt'][0]))

    if 'incomeAmt' in formRequest and formRequest['incomeAmt'] is not None and isValidString(formRequest['incomeAmt'][0]):
        miscFormDataModel.set_B4FedIncomeTaxWH(float(formRequest['incomeAmt'][0]))

    miscFormDataModel.set_B5FishingBoatProceeds(0)
    miscFormDataModel.set_B6MedHealthcarePymts(0)
    miscFormDataModel.set_B7IsDirectSale(0)
    miscFormDataModel.set_B8SubstitutePymts(0)
    miscFormDataModel.set_B9CropInsurance(0)
    miscFormDataModel.set_B10GrossProceeds(0)
    miscFormDataModel.set_B12Sec409ADeferrals(0)
    miscFormDataModel.set_B13EPP(0)
    miscFormDataModel.set_B14NonQualDefComp(0)
    miscFormDataModel.set_IsFATCA(True)
    miscFormDataModel.set_Is2ndTINnot(True)
    miscFormDataModel.set_AccountNum("587879879879")
    statesList = []
    stateModel = StatesModel()
    stateModel.set_StateCd("PA")
    stateModel.set_StateWH(15)
    stateModel.set_StateIdNum("99999999")
    stateModel.set_StateIncome(16)
    statesList.append(stateModel.__dict__)  # State 1
    stateModel = StatesModel()
    stateModel.set_StateCd("AZ")
    stateModel.set_StateWH(17)
    stateModel.set_StateIdNum("99-999999")
    stateModel.set_StateIncome(18)
    statesList.append(stateModel.__dict__)  # State 2
    miscFormDataModel.set_States(statesList)

    returnData.set_NECFormData(None)
    returnData.set_MISCFormData(miscFormDataModel.__dict__)
    returnDataList.append(returnData.__dict__)

    requestModel.set_ReturnData(returnDataList)

    print(f"Request = \n{requestModel.__dict__}")

    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM1099_MISC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response


def transmitForm1099MISC(submissionId, recordId):
    requestModel = TransmitForm1099NECModel()

    requestModel.set_SubmissionId(submissionId)
    requestModel.set_RecordIds(recordId)

    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.TRANSMIT_FORM_1099MISC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


# Get MISC List by business_id
def get_misc_list(get_list_request: GetNecListRequest):

    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_FORM_1099MISC_LIST,
                            params={"Page": get_list_request.get_page(),
                                    "PageSize": get_list_request.get_page_size(),
                                    "FromDate": get_list_request.get_from_date(),
                                    "BusinessId": get_list_request.get_business_id(),
                                    "ToDate": get_list_request.get_to_date()}, headers=HeaderUtils.getheaders())

    print(f"response = \n{response.json()}")
    return response.json()


# Get MISC List by business_id
def get_misc_pdf(SubmissionId, RecordIds, TINMaskType):
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_MISC_PDF,
                            params={"SubmissionId": SubmissionId,
                                    "RecordIds": RecordIds,
                                    "TINMaskType": TINMaskType}, headers=HeaderUtils.getheaders())

    return response.json()
