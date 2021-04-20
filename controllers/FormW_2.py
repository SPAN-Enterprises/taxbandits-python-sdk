import json

from flask import render_template

from models.Business import Business
from models.Employee import Employee
from models.Form1099NecList import Form1099NecList
from models.FormW2Request import FormW2Request
from models.ReturnDataFormW2 import ReturnDataFormW2
from models.ReturnHeader import ReturnHeader
from models.SubmissionManifest import SubmissionManifest
from models.USAddress import USAddress
from models.W2FormData import W2FormData


def save_form_w_2(requestJson):
    createFormW2Request = FormW2Request()
    submissionManifest = SubmissionManifest()
    submissionManifest.set_TaxYear(2020)
    submissionManifest.set_IsFederalFiling(True)
    submissionManifest.set_IsStateFiling(False)
    submissionManifest.set_IsPostal(True)
    submissionManifest.set_IsOnlineAccess(False)
    submissionManifest.set_IsTinMatching(False)
    submissionManifest.set_IsScheduleFiling(False)
    scheduleFiling = SubmissionManifest()
    scheduleFiling.set_EfileDate("05/21/2021")
    submissionManifest.set_ScheduleFiling(None)

    createFormW2Request.set_SubmissionManifest(submissionManifest.__dict__)

    returnHeader = ReturnHeader()

    business = Business()
    business.set_BusinessNm(requestJson['W2Forms[0].Business.BusinessNm'][0])
    business.set_EINorSSN(requestJson['W2Forms[0].Business.EINorSSN'][0])
    business.set_ContactNm(requestJson['W2Forms[0].Business.ContactNm'][0])
    business.set_Phone(requestJson['W2Forms[0].Business.Phone'][0])
    business.set_Email(requestJson['W2Forms[0].Business.Email'][0])
    business.set_Email(requestJson['W2Forms[0].Business.Email'][0])
    business.set_KindOfPayer(requestJson['W2Forms[0].Business.KindOfPayer'][0])
    business.set_KindOfEmployer(requestJson['W2Forms[0].Business.KindOfEmployer'][0])
    business.set_IsEIN(True)
    business.set_IsForeign(False)
    usAddress = USAddress()
    usAddress.set_Address1("1751 Kinsey Rd")
    usAddress.set_Address2("Main St")
    usAddress.set_City("Dothan")
    usAddress.set_State("AL")
    usAddress.set_ZipCd("36303")
    business.set_USAddress(usAddress.__dict__)

    returnHeader.set_Business(business.__dict__)

    createFormW2Request.set_ReturnHeader(returnHeader.__dict__)

    returnDataList = []

    returnData = ReturnDataFormW2()

    returnData.set_RecordId(None)
    returnData.set_SequenceId(1)
    employee = Employee()
    employee.set_FirstNm(requestJson['W2Forms[0].Employee.FirstNm'][0])
    employee.set_LastNm(requestJson['W2Forms[0].Employee.LastNm'][0])
    employee.set_MiddleNm(requestJson['W2Forms[0].Employee.MiddleNm'][0])
    employee.set_MiddleNm(requestJson['W2Forms[0].Employee.Suffix'][0])
    employee.set_SSN(requestJson['W2Forms[0].Employee.SSN'][0])
    employee.set_Phone(requestJson['W2Forms[0].Employee.Phone'][0])
    employee.set_Email(requestJson['W2Forms[0].Employee.Email'][0])

    usAddress = USAddress()
    usAddress.set_Address1("1751 Kinsey Rd")
    usAddress.set_Address2("Main St")
    usAddress.set_City("Dothan")
    usAddress.set_State("NC")
    usAddress.set_ZipCd("28201")
    employee.set_USAddress(usAddress.__dict__)
    returnData.set_Employee(employee.__dict__)

    formDetails = W2FormData()
    formDetails.set_B1Wages(requestJson['W2Forms[0].FormDetails.Box1'][0])
    formDetails.set_B2FedTaxWH(requestJson['W2Forms[0].FormDetails.Box2'][0])
    formDetails.set_B3SocSecWages(requestJson['W2Forms[0].FormDetails.Box3'][0])
    formDetails.set_B4SocSecTaxWH(requestJson['W2Forms[0].FormDetails.Box4'][0])
    returnData.set_W2FormData(formDetails.__dict__)

    returnDataList.append(returnData.__dict__)
    createFormW2Request.set_ReturnData(returnDataList)
    return createFormW2Request


def form_w2_save_reponse_validation(response):
    print(response)
    if 'StatusCode' in response:
        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='StatusMessage=' + response['StatusMessage'] + '<br>RecordId =' +
                                            response['FormW2Records']['SuccessRecords'][0][
                                                'RecordId'] + '<br>EmployeeId =' +
                                            response['FormW2Records']['SuccessRecords'][0]['EmployeeId'],
                                   ErrorMessage=' Form W2 Created Successfully', ButtonText="Form W2", FormType="W2")

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(
                                       response['StatusMessage']))
        else:

            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))

    else:
        return render_template('success.html', response='StatusMessage=' + str(response['status']),
                               ErrorMessage='Message=' + json.dumps(response))


def form_w2_list_response_validation(response):
    formW2List = []
    if response is not None:
        if 'FormW2Records' in response:
            if response['FormW2Records'] is not None:
                for records in response['FormW2Records']:
                    recipientData = Form1099NecList()
                    if 'EmployeeName' in records['Employee']:
                        recipientData.set_RecipientNm(
                            records['Employee']['EmployeeName'])

                    recipientData.set_TIN(records['Employee']['SSN'])
                    recipientData.set_RecipientId(
                        records['Employee']['EmployeeId'])
                    recipientData.set_SubmissionId(records['SubmissionId'])
                    recipientData.set_BusinessNm(records['BusinessNm'])
                    recipientData.set_Status(records['Employee']['Status'])
                    formW2List.append(recipientData.__dict__)

    return json.dumps(formW2List)


def form_w2_transmit_response_validation(response):
    print(response)
    if response is not None:

        if response['StatusCode'] == 200:

            return render_template('success.html',
                                   response='Status Timestamp=' + response['FormW2Records']['SuccessRecords'][0][
                                       'StatusTs'],
                                   ErrorMessage='Status= ' + response['FormW2Records']['SuccessRecords'][0]['Status'],
                                   ButtonText="Form W2", FormType="W2")

        elif 'Errors' in response and response['Errors'] is not None:

            return render_template('error_list.html', errorList=response['Errors'],
                                   status=str(response['StatusCode']) + " - " + str(
                                       response['StatusName']) + " - " + str(response['StatusMessage']))
        else:
            return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                                   ErrorMessage='Message=' + json.dumps(response))


def form_w2_get_pdf_response_validation(response):
    if 'FormW2Records' in response and response['FormW2Records'] is not None:
        if 'Message' in response['FormW2Records'][0]:
            return render_template('pdf_response.html', errorList=response['FormW2Records'],
                                   FormType="Form W2")
        else:
            return "OK"
    elif 'Errors' in response and response['Errors'] is not None:
        return render_template('pdf_response.html', errorList=response['Errors'])

    return "OK"
