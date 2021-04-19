import json

import requests

from models.GetFormListRequest import GetFormListRequest
from models.TransmitFormRequest import TransmitFormRequest
from utils import HeaderUtils, Config, EndPointConfig


def save_form_1099_nec(requestModel):
    # Create a new Form 1099-NEC
    # Method: Form1099NEC/Create (POST)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM1099_NEC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


# Transmits Form 1099-NEC
def transmit_form_1099_nec(submissionId):
    requestModel = TransmitFormRequest()
    requestModel.set_SubmissionId(submissionId)
    # Transmits a particular Form 1099-NEC
    # Method: Form1099NEC/Transmit (POST)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.TRANSMIT_FORM_1099NEC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


# Returns NEC List of specific business Id
def get_nec_list(get_list_request: GetFormListRequest):
    # Get NEC list of specific Business Id
    # Method: Form1099NEC/List (GET)
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_FORM1099_NEC_LIST,
                            params={"Page": get_list_request.get_page(),
                                    "PageSize": get_list_request.get_page_size(),
                                    "FromDate": get_list_request.get_from_date(),
                                    "BusinessId": get_list_request.get_business_id(),
                                    "ToDate": get_list_request.get_to_date()}, headers=HeaderUtils.getheaders())
    return response.json()


def get_pdf(SubmissionId, RecordIds, TINMaskType):
    # Get Form-1099 NEC PDF of particular submission Id and its Record Id
    # Method: Form1099NEC/GetPDF
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_PDF,
                            params={"SubmissionId": SubmissionId,
                                    "RecordIds": RecordIds,
                                    "TINMaskType": TINMaskType}, headers=HeaderUtils.getheaders())

    return response.json()
