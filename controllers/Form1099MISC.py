from models.Business import Business
from models.Form1099CreateRequest import Form1099CreateRequest
from models.MISCFormData import MISCFormData
from models.Recipient import Recipient
from models.ReturnData import ReturnData
from models.ReturnHeader import ReturnHeader
from models.ScheduleFiling import ScheduleFiling
from models.States import States
from models.SubmissionManifest import SubmissionManifest
from models.TransmitFormRequest import TransmitFormRequest
from models.USAddress import USAddress


def save_form_1099misc(formRequest):
    requestModel = Form1099CreateRequest()

    returnHeader = ReturnHeader()
    business = Business()

    if 'MISCForms_Business_BusinessId' in formRequest:
        business.set_BusinessId(formRequest['MISCForms_Business_BusinessId'][0])
    returnHeader.set_Business(business.__dict__)
    requestModel.set_ReturnHeader(returnHeader.__dict__)

    submissionManifest = SubmissionManifest()
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
    recipientId = -1

    if 'MISCForms_Recipient_RecipientId' in formRequest:
        recipientId = formRequest['MISCForms_Recipient_RecipientId'][0]

    if recipientId != '-1':
        recipientModel.set_RecipientId(recipientId)
    else:
        recipientModel.set_RecipientId('')

    recipientModel.set_TINType("EIN")

    if 'MISCForms_Recipient_TIN' in formRequest and formRequest['MISCForms_Recipient_TIN']:
        recipientModel.set_TIN(formRequest['MISCForms_Recipient_TIN'][0])

    if 'MISCForms_Recipient_RecipientNm' in formRequest:
        recipientModel.set_FirstPayeeNm(formRequest['MISCForms_Recipient_RecipientNm'][0])

    recipientModel.set_SecondPayeeNm("")
    recipientModel.set_IsForeign(False)
    usAddress = USAddress()
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
    miscFormDataModel = MISCFormData()

    if 'MISCForms_MISCFormDetails_Box1' in formRequest and formRequest[
        'MISCForms_MISCFormDetails_Box1'] is not None and is_valid_str(
        formRequest['MISCForms_MISCFormDetails_Box1'][0]):
        miscFormDataModel.set_B1Rents(float(formRequest['MISCForms_MISCFormDetails_Box1'][0]))

    if 'MISCForms_MISCFormDetails_Box2' in formRequest and formRequest[
        'MISCForms_MISCFormDetails_Box2'] is not None and is_valid_str(
        formRequest['MISCForms_MISCFormDetails_Box2'][0]):
        miscFormDataModel.set_B2Royalties(float(formRequest['MISCForms_MISCFormDetails_Box2'][0]))

    if 'MISCForms_MISCFormDetails_Box3' in formRequest and formRequest[
        'MISCForms_MISCFormDetails_Box3'] is not None and is_valid_str(
        formRequest['MISCForms_MISCFormDetails_Box3'][0]):
        miscFormDataModel.set_B3OtherIncome(float(formRequest['MISCForms_MISCFormDetails_Box3'][0]))

    if 'MISCForms_MISCFormDetails_Box4' in formRequest and formRequest[
        'MISCForms_MISCFormDetails_Box4'] is not None and is_valid_str(
        formRequest['MISCForms_MISCFormDetails_Box4'][0]):
        miscFormDataModel.set_B4FedIncomeTaxWH(float(formRequest['MISCForms_MISCFormDetails_Box4'][0]))

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
    miscFormDataModel.set_States(statesList)

    returnData.set_NECFormData(None)
    returnData.set_MISCFormData(miscFormDataModel.__dict__)
    returnDataList.append(returnData.__dict__)

    requestModel.set_ReturnData(returnDataList)

    return requestModel


def transmit(submissionId):
    requestModel = TransmitFormRequest()
    requestModel.set_SubmissionId(submissionId)
    return requestModel


def is_valid_str(param):
    return param is not None and len(param) > 0
