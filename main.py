from flask import render_template

from api_services import Business, Form1099NEC, Form1099MISC
from controller.business import create_business, create_form1099_nec, create_form1099_misc, get_business_detail_api, \
    get_all_business_list, get_form_list_request, create_form_w2
from core.Form1099NecList import Form1099NecList
from core.GetBusinssList import BusinessListRequest
from core.RecipientModel import RecipientModel
import json
from flask import Flask, request
from utils.SignatureValidation import validate

appInstance = Flask(__name__)


@appInstance.route('/')
def index():
    return render_template('index.html')


@appInstance.route('/createbusiness', methods=['get'])
def load_create_business():
    return render_template('createbusiness.html')


@appInstance.route('/success', methods=['POST'])
def submit():
    input_request_json = request.form.to_dict(flat=False)

    response = create_business(input_request_json)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' +
                                        response[
                                            'BusinessId'], ErrorMessage=' Business Created Successfully')

    elif 'Errors' in response and response['Errors'] is not None:

        return render_template('error_list.html', errorList=response['Errors'],
                               status=str(response['StatusCode']) + " - " + str(response['StatusName']) + " - " + str(
                                   response['StatusMessage']))
    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))


@appInstance.route('/createForm1099NEC', methods=['POST'])
def submit_form_1099_nec():
    input_request_json = request.form.to_dict(flat=False)

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

    response = create_form1099_nec(businessId, rName, rTIN, amount, recipientId)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>SubmissionId =' + response[
                                   'SubmissionId'], ErrorMessage=' Form 1099-NEC Created Successfully')

    elif 'Form1099Records' in response and response['Form1099Records'] is not None and 'ErrorRecords' in response[
        'Form1099Records'] and response['Form1099Records']['ErrorRecords'][0] is not None and 'Errors' in \
            response['Form1099Records']['ErrorRecords'][0] and response['Form1099Records']['ErrorRecords'][0]['Errors'] is not None:

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


@appInstance.route('/createForm1099MISC', methods=['POST'])
def submit_form_1099_misc():
    input_request_json = request.form.to_dict(flat=False)

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

    response = create_form1099_misc(businessId, rName, rTIN, amount, recipientId)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>SubmissionId =' +
                                        response['SubmissionId'], ErrorMessage='Form 1099-MISC Created Successfully')

    elif 'Form1099Records' in response and response['Form1099Records'] is not None and 'ErrorRecords' in response[
        'Form1099Records'] and response['Form1099Records']['ErrorRecords'][0] is not None and 'Errors' in \
            response['Form1099Records']['ErrorRecords'][0] and response['Form1099Records']['ErrorRecords'][0]['Errors'] is not None:

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


@appInstance.route('/detail', methods=['GET'])
def get_business():
    business_id = request.args.get('business_id')
    ein = request.args.get('ein')
    response = get_business_detail_api(business_id, ein)
    return render_template('detail.html', response=response)


@appInstance.route('/businesslist/', methods=['GET'])
def business_list():
    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(20)

    get_business_request.set_from_date('03/20/2021')

    get_business_request.set_to_date('04/31/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']

    return render_template('business_list.html', businesses=businesses)


@appInstance.route('/ReadBusinessList', methods=['GET'])
def get_business_list():
    businesses = get_all_business_list()

    return render_template('create_form_1099_nec.html', businesses=businesses)


@appInstance.route('/ReadFormBusinessList', methods=['GET'])
def get_form_business_list():
    businesses = get_all_business_list()

    return render_template('create_form_1099_misc.html', businesses=businesses)


# on selecting business from drop down this method gets invoked
@appInstance.route('/readRecipientsList', methods=['POST'])
def read_recipients_list():
    selectedBusiness = request.form['BusinessId']

    response = Form1099NEC.getForm1099NECList(selectedBusiness)

    recipientNameList = []

    if response is not None:

        if 'Form1099Records' in response:

            if response['Form1099Records'] is not None:

                for records in response['Form1099Records']:
                    recipientData = RecipientModel()
                    recipientData.set_RecipientId(
                        records['Recipient']['RecipientId'])
                    # recipientData.set_FirstPayeeNm(records['Recipient']['RecipientNm'])
                    if 'RecipientNm' in records['Recipient']:
                        recipientData.set_FirstPayeeNm(
                            records['Recipient']['RecipientNm'])
                    elif 'RecipientName' in records['Recipient']:
                        recipientData.set_FirstPayeeNm(
                            records['Recipient']['RecipientName'])
                    recipientData.set_TIN(records['Recipient']['TIN'])
                    recipientNameList.append(recipientData.__dict__)

    return json.dumps(recipientNameList)


@appInstance.route('/FormNecList', methods=['GET'])
def get_nec_list():
    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(100)

    get_business_request.set_from_date('03/01/2021')

    get_business_request.set_to_date('04/31/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']

    return render_template('form_1099_nec_list.html', businesses=businesses)


@appInstance.route('/Form1099MISCList', methods=['GET'])
def get_misc_list():
    businesses = get_all_business_list()

    return render_template('form_1099_misc_list.html', businesses=businesses)


@appInstance.route('/nec_list', methods=['POST'])
def form_1099_nec_list():
    response = get_form_list_request("NEC")

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


@appInstance.route('/misc_list', methods=['POST'])
def form_1099_misc_list():
    response = get_form_list_request("MISC")

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


@appInstance.route('/transmitForm1099NEC', methods=['GET'])
def transmit_form1099_nec():
    split_Ids = request.args.get('submissionId').split("_")

    recordList = [split_Ids[1]]

    response = Form1099NEC.transmitForm1099NEC(split_Ids[0], recordList)

    if response is not None:

        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='Status Timestamp=' + response['Form1099Records']['SuccessRecords'][0][
                                       'StatusTs'],
                                   ErrorMessage='Status= ' + response['Form1099Records']['SuccessRecords'][0]['Status'])

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(response['StatusMessage']))
        else:
            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))


@appInstance.route('/transmitForm1099MISC', methods=['GET'])
def transmit_form1099_misc():
    splitted_Ids = request.args.get('submissionId').split("_")

    recordList = [splitted_Ids[1]]

    response = Form1099MISC.transmitForm1099MISC(splitted_Ids[0], recordList)

    print(response)

    if response is not None:

        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='Status Timestamp=' + response['Form1099Records']['SuccessRecords'][0][
                                       'StatusTs'],
                                   ErrorMessage='Status= ' + response['Form1099Records']['SuccessRecords'][0]['Status'])

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(response['StatusMessage']))
        else:
            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))


@appInstance.route("/pdf_webhook", methods=['POST'])
def get_web_hook():
    if request.method == 'POST':
        Timestamp = request.headers.get('Timestamp')

        Signature = request.headers.get('Signature')

        isSignatureValid = validate(Timestamp, Signature)

        print("Signature Valid = "+isSignatureValid)

        return "OK"


@appInstance.route("/status_webhook", methods=['POST'])
def get_status_web_hook():
    if request.method == 'POST':
        Timestamp = request.headers.get('Timestamp')

        Signature = request.headers.get('Signature')

        isSignatureValid = validate(Timestamp, Signature)

        print("Signature Valid = "+isSignatureValid)

        # if isSignatureValid:
        # save_response_in_mongodb(response)

        return "OK"


@appInstance.route('/GetPDF', methods=['GET'])
def get_pdf():
    SubmissionId = request.args.get('submissionId')
    RecordIds = request.args.get('RecordIds')
    TINMaskType = "MASKED"
    response = Business.get_pdf(SubmissionId, RecordIds, TINMaskType)
    print(response)

    if 'Form1099NecRecords' in response and response['Form1099NecRecords'] is not None:
        if 'Message' in response['Form1099NecRecords'][0]:
            return render_template('pdf_response.html', errorList=response['Form1099NecRecords'])
        else:
            return "OK"
    elif 'Errors' in response and response['Errors'] is not None:
        return render_template('pdf_response.html', errorList=response['Errors'])

    return "OK"


@appInstance.route('/create_form_w2', methods=['GET'])
def form_w2():
    return render_template('create_form_w2.html')


@appInstance.route('/form_w2_success', methods=['POST'])
def submit_form_w2():
    input_request_json = request.form.to_dict(flat=False)

    response = create_form_w2(input_request_json)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' +
                                        response[
                                            'BusinessId'], ErrorMessage=' Business Created Successfully')

    elif 'Errors' in response and response['Errors'] is not None:

        return render_template('error_list.html', errorList=response['Errors'],
                               status=str(response['StatusCode']) + " - " + str(response['StatusName']) + " - " + str(
                                   response['StatusMessage']))
    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))


if __name__ == '__main__':
    appInstance.run()
