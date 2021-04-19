from api_services import Business
from model.GetBusinessList import GetBusinessList


def create_business(requestJson):
    response = Business.create(requestJson)
    return response


def get_business_detail_api(businessId, einOrSSN):
    return Business.get_business_detail(businessId, einOrSSN)


def get_all_business_list():
    get_business_request = GetBusinessList()

    get_business_request.set_page(1)

    get_business_request.set_page_size(100)

    get_business_request.set_from_date('03/01/2021')

    get_business_request.set_to_date('04/31/2021')

    response = Business.get_business_list(get_business_request)

    if response is not None and 'Businesses' in response and response['Businesses'] is not None:
        return response['Businesses']
