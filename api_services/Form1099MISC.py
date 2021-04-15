import json

import requests

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


def create(businessId, rName, rTIN, amount, recipientId):
    requestModel = CreateForm1099NECModel()

    returnHeader = ReturnHeaderModel()
    businessModel = CreateBusinessRequest()
    businessModel.set_BusinessId(businessId)
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
    if recipientId != '-1':
        recipientModel.set_RecipientId(recipientId)
    else:
        recipientModel.set_RecipientId('')

    recipientModel.set_TINType("EIN")
    recipientModel.set_TIN(rTIN)
    recipientModel.set_FirstPayeeNm(rName)
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
    miscFormDataModel.set_B1Rents(amount)
    miscFormDataModel.set_B2Royalties(0)
    miscFormDataModel.set_B3OtherIncome(0)
    miscFormDataModel.set_B4FedIncomeTaxWH(0)
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