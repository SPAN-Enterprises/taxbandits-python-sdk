# Create the new Form W2
import requests
from core.CreateFormW2Request import CreateFormW2Request

def create(requestJson):
    requestModel = CreateBusinessRequest()
    requestModel.set_BusinessNm(requestJson['business_name'][0])