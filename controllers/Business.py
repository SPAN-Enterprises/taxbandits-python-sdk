import json

from flask import render_template

from api_services.Business import get_business_list, get_business_detail, create
from api_services.Form1099MISC import get_misc_list
from api_services.Form1099NEC import get_nec_list
from api_services.FormW_2 import get_w_2_list
from models.Business import Business
from models.BusinessListRequest import BusinessListRequest
from models.ForeignAddress import ForeignAddress
from models.FormListRequest import FormListRequest
from models.Recipient import Recipient
from models.SigningAuthority import SigningAuthority


def create_business(requestJson):
    requestModel = Business()
    requestModel.set_BusinessNm(requestJson['business_name'][0])

    if 'is_ein' in requestJson:
        requestModel.set_IsEIN(True)
    else:
        requestModel.set_IsEIN(False)

    requestModel.set_EINorSSN(requestJson['ein_or_ssn'][0])

    if 'trade_nm' in requestJson:
        requestModel.set_TradeNm(requestJson['trade_nm'][0])

    requestModel.set_Email(requestJson['email'][0])

    if 'contact_nm' in requestJson:
        requestModel.set_ContactNm(requestJson['contact_nm'][0])

    requestModel.set_Phone(requestJson['phone'][0])

    if 'phone_extn' in requestJson:
        requestModel.set_PhoneExtn(requestJson['phone_extn'][0])

    if 'fax' in requestJson:
        requestModel.set_Fax(requestJson['fax'][0])

    if 'business_Type' in requestJson:
        requestModel.set_BusinessType(requestJson['business_Type'][0])
    else:
        requestModel.set_BusinessType('ESTE')

    if 'kind_of_employer' in requestJson:
        requestModel.set_KindOfEmployer(requestJson['kind_of_employer'][0])
    else:
        requestModel.set_KindOfEmployer('FEDERALGOVT')

    if 'kind_of_payer' in requestJson:
        requestModel.set_KindOfPayer(requestJson['kind_of_payer'][0])
    else:
        requestModel.set_KindOfPayer('REGULAR941')

    if 'is_business_terminated' in requestJson:
        requestModel.set_IsBusinessTerminated(True)
    else:
        requestModel.set_IsBusinessTerminated(False)

    addressModel = ForeignAddress()

    if 'is_foreign' in requestJson:
        requestModel.set_IsForeign(True)
        addressModel.set_Address1(requestJson['address1'][0])
        addressModel.set_Address2(requestJson['address2'][0])
        addressModel.set_City(requestJson['city'][0])
        addressModel.set_ProvinceOrStateNm(requestJson['state'][0])
        addressModel.set_Country(requestJson['country'][0])
        addressModel.set_PostalCd(requestJson['zip_cd'][0])
        requestModel.set_ForeignAddress(addressModel.__dict__)
    else:
        requestModel.set_IsForeign(False)
        addressModel.set_Address1(requestJson['address1'][0])
        addressModel.set_Address2(requestJson['address2'][0])
        addressModel.set_City(requestJson['city'][0])
        addressModel.set_State(requestJson['state_drop_down'][0])
        addressModel.set_ZipCd(requestJson['zip_cd'][0])
        requestModel.set_USAddress(addressModel.__dict__)

    saModel = SigningAuthority()

    if 'sa_name' in requestJson:
        saModel.set_SAName(requestJson['sa_name'][0])

    if 'sa_phone' in requestJson:
        saModel.set_SAPhone(requestJson['sa_phone'][0])

    if 'business_member_type' in requestJson:
        saModel.set_SABusinessMemberType(requestJson['business_member_type'][0])

    else:
        saModel.set_SABusinessMemberType('ADMINISTRATOR')

    requestModel.set_SigningAuthority(saModel.__dict__)
    response = create(requestModel)
    return response


def get_business_detail_api(businessId, einOrSSN):
    return get_business_detail(businessId, einOrSSN)


def get_all_business_list():
    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(100)

    get_business_request.set_from_date('03/01/2021')

    get_business_request.set_to_date('12/31/2021')

    response = get_business_list(get_business_request)

    if response is not None and 'Businesses' in response and response['Businesses'] is not None:
        return response['Businesses']


# Get NEC list of specific Business Id
# Method: Form1099NEC/List (GET)
def get_recipient_list(formType, businessId):
    get_request = FormListRequest()

    get_request.set_business_id(businessId)

    get_request.set_page(1)

    get_request.set_page_size(100)

    get_request.set_from_date('03/01/2021')

    get_request.set_to_date('12/31/2021')

    if formType == "NEC":
        response = get_nec_list(get_request)
    elif formType == "MISC":
        response = get_misc_list(get_request)
    else:
        get_request.set_to_date('04/19/2021')
        response = get_w_2_list(get_request)

    return response


# Validate recipient list response
def recipient_list_response_validation(response):
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


# Validate save business response
def save_business_response_validation(response):
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
