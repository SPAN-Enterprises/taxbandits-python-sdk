from flask import request
from api_services import Business, Form1099NEC, Form1099MISC, FormW2
from api_services.FormW2 import  generate_form_w2_request,get_w2_list
from core.GetBusinssList import BusinessListRequest
from core.GetFormListRequest import GetFormListRequest


def create_business(requestJson):
    response = Business.create(requestJson)
    return response


def create_form1099_nec(businessId, rName, rTIN, amount, recipientId):
    response = Form1099NEC.create(businessId, rName, rTIN, amount, recipientId)
    return response.json()


def create_form1099_misc(formRequest):
    response = Form1099MISC.create(formRequest)
    return response.json()


def get_business_detail_api(businessId, einOrSSN):
    return Business.get_business_detail(businessId, einOrSSN)


def get_all_business_list():
    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(100)

    get_business_request.set_from_date('03/01/2021')

    get_business_request.set_to_date('04/31/2021')

    response = Business.get_business_list(get_business_request)

    if response is not None and 'Businesses' in response and response['Businesses'] is not None:
        return response['Businesses']


def get_form_list_request(formType: str):

    get_request = GetFormListRequest()

    get_request.set_business_id(request.form['BusinessId'])

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


def create_form_w2(requestJson):
    response = generate_form_w2_request(requestJson)
    return response

