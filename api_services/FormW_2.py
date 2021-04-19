import json

import requests
from controllers.FormW_2 import save_form_w_2
from models.FormListRequest import FormListRequest
from models.TransmitFormRequest import TransmitFormRequest
from utils import HeaderUtils, Config, EndPointConfig


def save_form_w2(requestJson):
    # Create a new Form W2
    # Method: FormW2/Create (POST)
    formW2Request= save_form_w_2(requestJson)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM_W2,
                             data=json.dumps(formW2Request.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


# Returns W2 List by business_id
def get_w2_list(get_request: FormListRequest):

    # Get W2 list of specific Business Id
    # Method: FormW2/List (GET)
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.LIST_FORM_W2,
                            params={"Page": get_request.get_page(),
                                    "PageSize": get_request.get_page_size(),
                                    "FromDate": get_request.get_from_date(),
                                    "BusinessId": get_request.get_business_id(),
                                    "ToDate": get_request.get_to_date()}, headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()


# Transmits Form W2
def transmit_formw2(submissionId):
    requestModel = TransmitFormRequest()
    requestModel.set_SubmissionId(submissionId)

    # Transmits a particular Form W2
    # Method: FormW2/Transmit (POST)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.TRANSMIT_FORM_W2,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


def get_w2_pdf(SubmissionId, TINMaskType):

    # Get Form W2 PDF of particular submission Id and its Record Id
    # Method: FormW2/GetPDF
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.FORM_W2_GET_PDF,
                            params={"SubmissionId": SubmissionId,
                                    "TINMaskType": TINMaskType}, headers=HeaderUtils.getheaders())

    return response.json()