import json

import requests
from controllers.Form1099MISC import transmit
from models import FormListRequest
from utils import HeaderUtils, Config, EndPointConfig


def save_form_1099_misc(requestModel):
    # Create a new Form 1099-MISC
    # Method: Form1099MISC/Create (POST)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM1099_MISC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


# Transmits Form 1099-MISC
def transmit_form_1099_misc(submissionId, recordId):
    # Transmits a particular Form 1099-MISC
    # Method: Form1099MISC/Transmit (POST)
    requestModel = transmit(submissionId, recordId)
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.TRANSMIT_FORM_1099MISC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    return response.json()


# Returns MISC List of specific business Id
def get_misc_list(get_list_request: FormListRequest):
    # Get MISC list of specific Business Id
    # Method: Form1099MISC/List (GET)
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_FORM_1099MISC_LIST,
                            params={"Page": get_list_request.get_page(),
                                    "PageSize": get_list_request.get_page_size(),
                                    "FromDate": get_list_request.get_from_date(),
                                    "BusinessId": get_list_request.get_business_id(),
                                    "ToDate": get_list_request.get_to_date()},
                            headers=HeaderUtils.getheaders())

    return response.json()


def get_misc_pdf(SubmissionId, RecordIds, TINMaskType):
    # Get Form-1099 MISC PDF of particular submission Id and its Record Id
    # Method: Form1099MISC/GetPDF
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_MISC_PDF,
                            params={"SubmissionId": SubmissionId,
                                    "RecordIds": RecordIds,
                                    "TINMaskType": TINMaskType}, headers=HeaderUtils.getheaders())

    return response.json()
