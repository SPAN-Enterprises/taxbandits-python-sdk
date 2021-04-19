from api_services import Form1099NEC, Form1099MISC
from models.GetFormListRequest import GetFormListRequest
from flask import request
from api_services.FormW2 import get_w2_list


def create_form1099_nec(businessId, rName, rTIN, amount, recipientId):
    response = Form1099NEC.create(businessId, rName, rTIN, amount, recipientId)
    return response.json()


def get_form_list_request(formType: str, formRequest: request):

    get_request = GetFormListRequest()

    get_request.set_business_id(formRequest.form['BusinessId'])

    get_request.set_page(1)

    get_request.set_page_size(100)

    get_request.set_from_date('03/01/2021')

    get_request.set_to_date('04/15/2021')

    if formType == "NEC":
        response = Form1099NEC.get_nec_list(get_request)
    elif formType == "MISC":
        response = Form1099MISC.get_misc_list(get_request)
    else:
        response = get_w2_list(get_request)

    return response
