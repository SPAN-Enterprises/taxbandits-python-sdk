import json

from flask import render_template

from models.Business import Business
from models.Form1099NECCreateRequest import Form1099NECCreateRequest
from models.Form1099NecList import Form1099NecList
from models.NECFormData import NECFormData
from models.Recipient import Recipient
from models.ReturnData import ReturnData
from models.ReturnHeader import ReturnHeader
from models.ScheduleFiling import ScheduleFiling
from models.States import States
from models.SubmissionManifest import SubmissionManifest
from models.USAddress import USAddress


def save_form_nec(input_request_json):
    businessId = ''
    if 'business_list' in input_request_json:
        businessId = input_request_json['business_list'][0]

    rName = ''
    if 'rName' in input_request_json:
        rName = input_request_json['rName'][0]

    rTIN = ''
    if 'rTIN' in input_request_json:
        rTIN = input_request_json['rTIN'][0]

    amount = ''
    if 'amount' in input_request_json:
        amount = input_request_json['amount'][0]

    recipientId = None

    if 'recipientsDropDown' in input_request_json:
        recipientId = input_request_json['recipientsDropDown'][0]

    requestModel = Form1099NECCreateRequest()

    returnHeader = ReturnHeader()

    business = Business()
    business.set_BusinessId(businessId)
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

    return requestModel


def nec_save_response_validation(response):
    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>SubmissionId =' + response[
                                   'SubmissionId'], ErrorMessage=' Form 1099-NEC Created Successfully',
                               ButtonText="Form 1099-NEC", FormType="NEC")

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
                               status=str(response['StatusCode']) + " - " + str(response['StatusName']) + " - " + str(
                                   response['StatusMessage']))
    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))


def form_nec_list_response_validation(response):
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


def form_1099_nec_transmit_response_validation(response):
    if response is not None:

        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='Status Timestamp=' + response['Form1099Records']['SuccessRecords'][0][
                                       'StatusTs'],
                                   ErrorMessage='Status= ' + response['Form1099Records']['SuccessRecords'][0]['Status'],
                                   ButtonText="Form 1099-NEC", FormType="NEC")

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(response['StatusMessage']))

        else:
            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))


def form_1099_nec_get_pdf_response_validation(response):
    if 'Form1099NecRecords' in response and response['Form1099NecRecords'] is not None:
        if 'Message' in response['Form1099NecRecords'][0]:
            return render_template('pdf_response.html', errorList=response['Form1099NecRecords'],
                                   FormType="Form 1099-NEC")
        else:
            return "OK"
    elif 'Errors' in response and response['Errors'] is not None:
        return render_template('pdf_response.html', errorList=response['Errors'])

    return "OK"
