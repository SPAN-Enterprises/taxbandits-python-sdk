import json
import requests
from core.CreateFormW2Request import CreateFormW2Request
from core.Business import Business
from core.Employee import Employee
from core.FormDetails import FormDetails
from utils import HeaderUtils, Config, EndPointConfig


def generate_form_w2_request(requestJson):

    createFormW2Request = CreateFormW2Request()
    createFormW2Request.set_TaxYear(2020)

    business = Business()
    business.set_BusinessId('3562dc82-45a1-43a7-96a1-5812736ad5f4')
    createFormW2Request.set_Business(business.__dict__)

    employee = Employee()
    employee.set_FirstNm(requestJson['W2Forms[0].Employee.FirstNm'][0])
    employee.set_LastNm(requestJson['W2Forms[0].Employee.LastNm'][0])
    employee.set_MiddleNm(requestJson['W2Forms[0].Employee.MiddleNm'][0])
    employee.set_MiddleNm(requestJson['W2Forms[0].Employee.Suffix'][0])
    employee.set_SSN(requestJson['W2Forms[0].Employee.SSN'][0])
    employee.set_Phone(requestJson['W2Forms[0].Employee.Phone'][0])
    employee.set_Email(requestJson['W2Forms[0].Employee.Email'][0])
    createFormW2Request.set_Employee(employee.__dict__)

    formDetails = FormDetails()
    formDetails.set_Box1(requestJson['W2Forms[0].FormDetails.Box1'][0])
    formDetails.set_Box2(requestJson['W2Forms[0].FormDetails.Box2'][0])
    formDetails.set_Box3(requestJson['W2Forms[0].FormDetails.Box3'][0])
    formDetails.set_Box4(requestJson['W2Forms[0].FormDetails.Box4'][0])
    createFormW2Request.set_FormDetails(formDetails.__dict__)

    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM_W2,
                            data=json.dumps(createFormW2Request.__dict__),
                            headers=HeaderUtils.getheaders())

    print(response.status_code)

    print(response.json())
    return response.json()


