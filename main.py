from flask import render_template, Flask, request
from api_services import Form1099NEC, Business, Form1099MISC, FormW_2
from api_services.FormW_2 import transmit_formw2, save_formw2
from controllers import Business
from controllers.Business import get_recipient_list, recipient_list_response_validation, \
    save_business_response_validation
from controllers.Form1099MISC import save_form_1099misc, form_1099_misc_list_response_validation, \
    save_form_1099_misc_response_validation, form_1099_misc_transmit_response_validation, \
    form_1099_misc_get_pdf_response_validation
from controllers.Form1099NEC import save_form_nec, nec_save_response_validation, form_nec_list_response_validation, \
    form_1099_nec_transmit_response_validation, form_1099_nec_get_pdf_response_validation
from controllers.FormW_2 import form_w2_save_response_validation, form_w2_list_response_validation, \
    form_w2_transmit_response_validation, form_w2_get_pdf_response_validation
from utils.SignatureValidation import validate

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
    return save_business_response_validation(response)


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
    return recipient_list_response_validation(response)


# Save Form 1099 NEC
@appInstance.route('/save_form_1099_nec', methods=['POST'])
def save_form_1099_nec():
    input_request_json = request.form.to_dict(flat=False)
    requestModel = save_form_nec(input_request_json)
    response = Form1099NEC.save_form_1099_nec(requestModel)
    return nec_save_response_validation(response)


# 1099-NEC List - Render
@appInstance.route('/render_template_nec_list', methods=['GET'])
def get_nec_list():
    businesses = Business.get_all_business_list()
    return render_template('form_1099_nec_list.html', businesses=businesses)


# 1099-NEC List By BusinessId
@appInstance.route('/form_1099_nec_list', methods=['POST'])
def form_1099_nec_list():
    response = Business.get_recipient_list("NEC", request.form['BusinessId'])
    return form_nec_list_response_validation(response)


# 1099-NEC Transmit
@appInstance.route('/transmit_form_1099_nec', methods=['GET'])
def transmit_form1099_nec():
    response = Form1099NEC.transmit_form_1099_nec(request.args.get('submissionId'))
    return form_1099_nec_transmit_response_validation(response)


# 1099-NEC get pdf Webhook response
@appInstance.route('/form_1099_nec/get_pdf', methods=['GET'])
def get_pdf():
    response = Form1099NEC.get_pdf(request.args.get('submissionId'), request.args.get('RecordIds'), "MASKED")
    return form_1099_nec_get_pdf_response_validation(response)


# Get Business list for form 1099 MISC
@appInstance.route('/render_template_create_form_1099_misc', methods=['GET'])
def get_form_business_list():
    businesses = Business.get_all_business_list()
    return render_template('create_form_1099_misc.html', businesses=businesses)


# on selecting business from drop down this method gets invoked
@appInstance.route('/get_recipient_by_business_id_misc', methods=['POST'])
def get_recipients_list_misc():
    response = Business.get_recipient_list("MISC", request.form['BusinessId'])
    return recipient_list_response_validation(response)


# Save Form 1099-MISC
@appInstance.route('/save_form_1099_misc', methods=['POST'])
def form_1099_misc():
    input_request_json = request.form.to_dict(flat=False)
    requestModel = save_form_1099misc(input_request_json)
    response = Form1099MISC.save_form_1099_misc(requestModel)
    return save_form_1099_misc_response_validation(response)


# Get Business list for form 1099 NEC
@appInstance.route('/render_template_1099_misc_list', methods=['GET'])
def get_business_list_for_1099misc_dropdown():
    businesses = Business.get_all_business_list()
    return render_template('form_1099_misc_list.html', businesses=businesses)


# Get 1099-MISC list by BusinessId
@appInstance.route('/form_1099_misc_list', methods=['POST'])
def form_1099_misc_list():
    response = Business.get_recipient_list("MISC", request.form['BusinessId'])
    return form_1099_misc_list_response_validation(response)


# Transmit Form 1099-MISC
@appInstance.route('/transmit_form1099_misc', methods=['GET'])
def transmit_form1099_misc():
    response = Form1099MISC.transmit_form_1099_misc(request.args.get('submissionId'))
    return form_1099_misc_transmit_response_validation(response)


# Form 1099-MISC Get PDF
@appInstance.route('/form_1099_misc/get_pdf', methods=['GET'])
def get_misc_pdf():
    response = Form1099MISC.get_misc_pdf(request.args.get('submissionId'), "MASKED")
    return form_1099_misc_get_pdf_response_validation(response)


# Form W2 Crete
@appInstance.route('/render_template_create_form_w2', methods=['GET'])
def form_w2():
    return render_template('create_form_w2.html')


# Save Form W-2
@appInstance.route('/form_w2_success', methods=['POST'])
def save_form_w2():
    input_request_json = request.form.to_dict(flat=False)
    response = save_formw2(input_request_json)
    return form_w2_save_response_validation(response)


# Get Business List for Form W-2
@appInstance.route('/render_template_w2_list', methods=['GET'])
def get_w2_list():
    businesses = Business.get_all_business_list()
    return render_template('form_w2_list.html', businesses=businesses)


# Form W-2 List
@appInstance.route('/form_w2_list', methods=['POST'])
def form_w2_list():
    response = get_recipient_list("W2", request.form['BusinessId'])
    return form_w2_list_response_validation(response)


# Form W-2 Transmit
@appInstance.route('/transmit_form_w2', methods=['GET'])
def transmit_form_w2():
    response = transmit_formw2(request.args.get('submissionId'))
    return form_w2_transmit_response_validation(response)


# Form W-2 Get Pdf
@appInstance.route('/form_w2/get_pdf', methods=['GET'])
def get_w2_pdf():
    response = FormW_2.get_w2_pdf(request.args.get('submissionId'), "MASKED")
    return form_w2_get_pdf_response_validation(response)


# PDF Webhook response
@appInstance.route("/pdf_webhook", methods=['POST'])
def get_web_hook():
    if request.method == 'POST':
        Timestamp = request.headers.get('Timestamp')

        Signature = request.headers.get('Signature')

        isSignatureValid = validate(Timestamp, Signature)

        # if isSignatureValid:
        # save_response_in_mongodb(response)

        return "OK"


# Form Status Webhook response
@appInstance.route("/status_webhook", methods=['POST'])
def get_status_web_hook():
    if request.method == 'POST':
        Timestamp = request.headers.get('Timestamp')

        Signature = request.headers.get('Signature')

        isSignatureValid = validate(Timestamp, Signature)


# Common method for redirect to form List from form creation success page
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
