import json

from flask import render_template

from models.Business import Business
from models.Form1099CreateRequest import Form1099CreateRequest
from models.Form1099NecList import Form1099NecList
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


def form_1099_misc_list_response_validation(response):
    form1099NecList = []
    if response is not None:
        if 'Form1099Records' in response:
            if response['Form1099Records'] is not None:
                for records in response['Form1099Records']:
                    recipientData = Form1099NecList()
                    if 'RecipientNm' in records['Recipient']:
                        recipientData.set_RecipientNm(
                            records['Recipient']['RecipientNm'])
                    elif 'RecipientName' in records['Recipient']:
                        recipientData.set_RecipientNm(
                            records['Recipient']['RecipientName'])
                    recipientData.set_TIN(records['Recipient']['TIN'])
                    recipientData.set_RecipientId(
                        records['Recipient']['RecordId'])
                    recipientData.set_SubmissionId(records['SubmissionId'])
                    recipientData.set_BusinessNm(records['BusinessNm'])
                    recipientData.set_Status(records['Recipient']['Status'])
                    form1099NecList.append(recipientData.__dict__)
    return json.dumps(form1099NecList)


def save_form_1099_misc_response_validation(response):
    if response is not None:
        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='StatusMessage=' + response['StatusMessage'] + '<br>SubmissionId =' +
                                            response['SubmissionId'],
                                   ErrorMessage='Form 1099-MISC Created Successfully', ButtonText="Form 1099-MISC",
                                   FormType="MISC")

        elif 'Form1099Records' in response and response['Form1099Records'] is not None and 'ErrorRecords' in response[
            'Form1099Records'] and response['Form1099Records']['ErrorRecords'][0] is not None and 'Errors' in \
                response['Form1099Records']['ErrorRecords'][0] and response['Form1099Records']['ErrorRecords'][0][
            'Errors'] is not None:

            errorRecords = []

            for errorList in response['Form1099Records']['ErrorRecords']:
                if 'Errors' in errorList and errorList['Errors'] is not None:
                    for err in errorList['Errors']:
                        errorRecords.append(err)

            return render_template('error_list.html', errorList=errorRecords,
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(
                                       response['StatusMessage']))
        else:

            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))


def form_1099_misc_transmi_response_validation(response):
    if response is not None:

        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='Status Timestamp=' + response['Form1099Records']['SuccessRecords'][0][
                                       'StatusTs'],
                                   ErrorMessage='Status= ' + response['Form1099Records']['SuccessRecords'][0]['Status'],
                                   ButtonText="Form 1099-MISC", FormType="MISC")

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(response['StatusMessage']))
        else:
            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))


def form_1099_misc_get_pdf_response_validation(response):
    print(response)
    if 'Form1099NecRecords' in response and response['Form1099NecRecords'] is not None:
        if 'Message' in response['Form1099NecRecords'][0]:
            return render_template('pdf_response.html', errorList=response['Form1099NecRecords'],
                                   FormType="Form 1099-NEC")
        else:
            return "OK"
    elif 'Errors' in response and response['Errors'] is not None:
        return render_template('pdf_response.html', errorList=response['Errors'])

    return "OK"


def is_valid_str(param):
    return param is not None and len(param) > 0
