import requests
import json
from utils import HeaderUtils, Config, EndPointConfig
from api_services import JwtGeneration
from core import CreateForm1099NECModel, SubmissionManifestModel, StatesModel, ReturnHeaderModel, ReturnDataModel, \
    NECFormDataModel, RecipientModel


def create():
    returnHeader = ReturnHeaderModel()


    ReturnHeader = {"Business": {"BusinessId": "0fd6e0a3-f122-4cdc-a4da-25cb155010e1"}}

    SubmissionManifest = {"SubmissionId": "null", "TaxYear": "2020", "IsFederalFiling": "true", "IsStateFiling": "true",
                          "IsPostal": "true", "IsOnlineAccess": "true", "IsTinMatching": "true",
                          "IsScheduleFiling": "true"}  # "ScheduleFiling": {"EfileDate": "03/31/2021"}

    USAddress = {"Address1": "1751 Kinsey Rd", "Address2": "Main St", "City": "Dothan", "State": "AL",
                 "ZipCd": "36303"},

    NECFormData = {
        "B1NEC": 100,
        "B4FedTaxWH": 40.55,
        "IsFATCA": "true",
        "Is2ndTINnot": "true",
        "AccountNum": "20123130000009000001",
        "States": [{"StateCd": "PA", "StateWH": 15, "StateIdNum": "99999999", "StateIncome": 16},
                   {"StateCd": "AZ", "StateWH": 17, "StateIdNum": "99-9999999", "StateIncome": 18}]}

    ReturnData = [{
        "RecordId": "null", "SequenceId": "1",
        "Recipient": {"RecipientId": "null", "TINType": "EIN", "TIN": "393814579", "FirstPayeeNm": "Marken",
                      "SecondPayeeNm": "Davis", "IsForeign": "false", "USAddress": USAddress, "Email": "john@gmail.com",
                      "Fax": "1234567890", "Phone": "1234567890"},
        "NECFormData": NECFormData}]

    requestData = {"ReturnHeader": ReturnHeader, "SubmissionManifest": SubmissionManifest, "ReturnData": ReturnData}

    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM1099_NEC,
                             data=json.dumps(requestData),
                             headers=HeaderUtils.getheaders())

    return response
