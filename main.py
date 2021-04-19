import json

from flask import render_template, Flask, request

from api_services import Form1099NEC, Business, Form1099MISC, FormW_2
from api_services.Form1099MISC import get_misc_list, save_form_1099_misc
from api_services.FormW_2 import save_form_w2, transmit_formw2, get_w_2_list
from controllers import Business
from controllers.Business import get_recipient_list
from controllers.Form1099MISC import save_form_1099misc
from controllers.Form1099NEC import save_form_nec
from models.Form1099NecList import Form1099NecList
from models.Recipient import Recipient
from controllers.Form1099MISC import save_form_1099misc

appInstance = Flask(__name__)


# Index Page
@appInstance.route('/')
def index():
    return render_template('index.html')


# Create Business - Get
@appInstance.route('/create_business', methods=['GET'])
def create_business():
    return render_template('create_business.html')


# Get Business List
@appInstance.route('/business_list/', methods=['GET'])
def get_business_list():
    businesses = Business.get_all_business_list()
    return render_template('business_list.html', businesses=businesses)


# Create Business - Post
@appInstance.route('/success', methods=['POST'])
def save_business():
    input_request_json = request.form.to_dict(flat=False)

    response = Business.create_business(input_request_json)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' +
                                        response[
                                            'BusinessId'], ErrorMessage=' Business Created Successfully',
                               formtype="Businesses")

    elif 'Errors' in response and response['Errors'] is not None:

        return render_template('error_list.html', errorList=response['Errors'],
                               status=str(response['StatusCode']) + " - " + str(response['StatusName']) + " - " + str(
                                   response['StatusMessage']))

    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))


# View Business
@appInstance.route('/business_detail', methods=['GET'])
def get_business():
    business_id = request.args.get('business_id')
    ein = request.args.get('ein')
    response = Business.get_business_detail_api(business_id, ein)
    return render_template('business_detail.html', response=response)


# FORM 1099 NEC


# Get Business list for form 1099 NEC
@appInstance.route('/render_template_create_form_1099_nec', methods=['GET'])
def get_business_list_for_dropdown():
    businesses = Business.get_all_business_list()
    return render_template('create_form_1099_nec.html', businesses=businesses)


# on selecting business from drop down this method gets invoked
@appInstance.route('/get_recipient_by_business_id', methods=['POST'])
def get_recipients_list():
    response = Business.get_recipient_list("NEC", request.form['BusinessId'])

    recipientNameList = []

    if response is not None:

        if 'Form1099Records' in response:

            if response['Form1099Records'] is not None:

                for records in response['Form1099Records']:
                    recipientData = Recipient()
                    recipientData.set_RecipientId(
                        records['Recipient']['RecipientId'])
                    if 'RecipientNm' in records['Recipient']:
                        recipientData.set_FirstPayeeNm(
                            records['Recipient']['RecipientNm'])
                    elif 'RecipientName' in records['Recipient']:
                        recipientData.set_FirstPayeeNm(
                            records['Recipient']['RecipientName'])
                    recipientData.set_TIN(records['Recipient']['TIN'])
                    recipientNameList.append(recipientData.__dict__)

    return json.dumps(recipientNameList)


# Save Form 1099 NEC
@appInstance.route('/save_form_1099_nec', methods=['POST'])
def save_form_1099_nec():
    input_request_json = request.form.to_dict(flat=False)

    requestModel = save_form_nec(input_request_json)

    response = Form1099NEC.save_form_1099_nec(requestModel)

    print(response)

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


# 1099-NEC List - Render
@appInstance.route('/render_template_nec_list', methods=['GET'])
def get_nec_list():
    businesses = Business.get_all_business_list()

    return render_template('form_1099_nec_list.html', businesses=businesses)


# 1099-NEC List By BusinessId
@appInstance.route('/form_1099_nec_list', methods=['POST'])
def form_1099_nec_list():
    response = Business.get_recipient_list("NEC", request.form['BusinessId'])

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


# 1099-NEC Transmit
@appInstance.route('/transmit_form_1099_nec', methods=['GET'])
def transmit_form1099_nec():
    print(request.args.get('submissionId'))
    response = Form1099NEC.transmit_form_1099_nec(request.args.get('submissionId'))
    print(response)
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


# 1099-NEC get pdf Webhook response
@appInstance.route('/form_1099_nec/get_pdf', methods=['GET'])
def get_pdf():
    response = Form1099NEC.get_pdf(request.args.get('submissionId'), request.args.get('RecordIds'), "MASKED")
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


# Get Business list for form 1099 MISC
@appInstance.route('/render_template_create_form_1099_misc', methods=['GET'])
def get_form_business_list():
    businesses = Business.get_all_business_list()
    return render_template('create_form_1099_misc.html', businesses=businesses)


# on selecting business from drop down this method gets invoked
@appInstance.route('/get_recipient_by_business_id_misc', methods=['POST'])
def get_recipients_list_misc():
    response = Business.get_recipient_list("MISC", request.form['BusinessId'])
    print(response)
    recipientNameList = []

    if response is not None:

        if 'Form1099Records' in response:

            if response['Form1099Records'] is not None:

                for records in response['Form1099Records']:
                    recipientData = Recipient()
                    recipientData.set_RecipientId(
                        records['Recipient']['RecipientId'])
                    if 'RecipientNm' in records['Recipient']:
                        recipientData.set_FirstPayeeNm(
                            records['Recipient']['RecipientNm'])
                    elif 'RecipientName' in records['Recipient']:
                        recipientData.set_FirstPayeeNm(
                            records['Recipient']['RecipientName'])
                    recipientData.set_TIN(records['Recipient']['TIN'])
                    recipientNameList.append(recipientData.__dict__)

    return json.dumps(recipientNameList)


# Save Form 1099-MISC
@appInstance.route('/save_form_1099_misc', methods=['POST'])
def form_1099_misc():
    input_request_json = request.form.to_dict(flat=False)

    requestModel = save_form_1099misc(input_request_json)

    response = Form1099MISC.save_form_1099_misc(requestModel)

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


# Get Business list for form 1099 NEC
@appInstance.route('/render_template_1099_misc_list', methods=['GET'])
def get_business_list_for_1099misc_dropdown():
    businesses = Business.get_all_business_list()
    return render_template('form_1099_misc_list.html', businesses=businesses)


# Get 1099-MISC list by BusinessId
@appInstance.route('/form_1099_misc_list', methods=['POST'])
def form_1099_misc_list():
    response = Business.get_recipient_list("MISC", request.form['BusinessId'])
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


# Transmit Form 1099-MISC
@appInstance.route('/transmit_form1099_misc', methods=['GET'])
def transmit_form1099_misc():
    response = Form1099MISC.transmit_form_1099_misc(request.args.get('submissionId'))

    print(response)

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


# Form 1099-MISC Get PDF
@appInstance.route('/form_1099_misc/get_pdf', methods=['GET'])
def get_misc_pdf():
    response = Form1099MISC.get_misc_pdf(request.args.get('submissionId'), "MASKED")
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


# Form W2 Crete
@appInstance.route('/render_template_create_form_w2', methods=['GET'])
def form_w2():
    return render_template('create_form_w2.html')


# Save Form W-2
@appInstance.route('/form_w2_success', methods=['POST'])
def save_form_w2():
    input_request_json = request.form.to_dict(flat=False)

    response = save_form_w2(input_request_json)

    print(response)
    if 'StatusCode' in response:
        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='StatusMessage=' + response['StatusMessage'] + '<br>RecordId =' +
                                            response['FormW2Records']['SuccessRecords'][0][
                                                'RecordId'] + '<br>EmployeeId =' +
                                            response['FormW2Records']['SuccessRecords'][0]['EmployeeId'],
                                   ErrorMessage=' Form W2 Created Successfully', ButtonText="Form W2", FormType="W2")

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(
                                       response['StatusMessage']))
        else:

            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))

    else:
        return render_template('success.html', response='StatusMessage=' + str(response['status']),
                               ErrorMessage='Message=' + json.dumps(response))


# Get Business List for Form W-2
@appInstance.route('/render_template_w2_list', methods=['GET'])
def get_w2_list():
    businesses = Business.get_all_business_list()

    return render_template('form_w2_list.html', businesses=businesses)


# Form W-2 List
@appInstance.route('/form_w2_list', methods=['POST'])
def form_w2_list():
    response = get_recipient_list("W2", request.form['BusinessId'])

    formW2List = []

    if response is not None:

        if 'FormW2Records' in response:

            if response['FormW2Records'] is not None:

                for records in response['FormW2Records']:
                    recipientData = Form1099NecList()
                    if 'EmployeeName' in records['Employee']:
                        recipientData.set_RecipientNm(
                            records['Employee']['EmployeeName'])

                    recipientData.set_TIN(records['Employee']['SSN'])
                    recipientData.set_RecipientId(
                        records['Employee']['EmployeeId'])
                    recipientData.set_SubmissionId(records['SubmissionId'])
                    recipientData.set_BusinessNm(records['BusinessNm'])
                    recipientData.set_Status(records['Employee']['Status'])
                    formW2List.append(recipientData.__dict__)

    return json.dumps(formW2List)


# Form W-2 Transmit
@appInstance.route('/transmit_form_w2', methods=['GET'])
def transmit_form_w2():
    response = transmit_formw2(request.args.get('submissionId'))

    print(response)

    if response is not None:

        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='Status Timestamp=' + response['FormW2Records']['SuccessRecords'][0][
                                       'StatusTs'],
                                   ErrorMessage='Status= ' + response['FormW2Records']['SuccessRecords'][0]['Status'],
                                   ButtonText="Form W2", FormType="W2")

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(response['StatusMessage']))
        else:
            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))


# Form W-2 Get Pdf
@appInstance.route('/form_w2/get_pdf', methods=['GET'])
def get_w2_pdf():
    SubmissionId = request.args.get('submissionId')
    TINMaskType = "MASKED"
    response = FormW_2.get_w2_pdf(SubmissionId, TINMaskType)

    if 'FormW2Records' in response and response['FormW2Records'] is not None:
        if 'Message' in response['FormW2Records'][0]:
            return render_template('pdf_response.html', errorList=response['FormW2Records'],
                                   FormType="Form W2")
        else:
            return "OK"
    elif 'Errors' in response and response['Errors'] is not None:
        return render_template('pdf_response.html', errorList=response['Errors'])

    return "OK"


@appInstance.route('/redirect_form_list', methods=['GET'])
def redirect_to_form_list_pages():
    formType = request.args.get('formtype')

    if formType is not None:
        if formType == 'NEC':
            return get_nec_list()
        elif formType == 'MISC':
            return get_business_list_for_1099misc_dropdown()
        elif formType == 'W2':
            return get_w2_list()


if __name__ == '__main__':
    appInstance.run()
