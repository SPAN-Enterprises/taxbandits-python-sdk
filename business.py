import json

from api_services import Business,JwtGeneration
from flask import Flask, render_template, request

from core.BusinessList import Businesses
from core.GetBusinssList import BusinessListRequest


business = Flask(__name__)
global jwtToken


@business.route('/')
def index():
    return render_template('index.html')


@business.route('/createbusiness', methods=['POST'])
def loadCreateBusiness():
    return render_template('createbusiness.html')


@business.route('/success', methods=['POST'])
def submit():
    BusinessName = request.form['business_name']
    EINOrSSN = request.form['ein_or_ssn']
    print(BusinessName, EINOrSSN)

    if BusinessName == '' or EINOrSSN == '':
        return render_template('index.html', message='Please enter required fields')

    elif len(EINOrSSN) < 9:
        return render_template('index.html', message='Please enter valid input')

    else:
        response = create_business(BusinessName, EINOrSSN)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' + response[
                                   'BusinessId'], ErrorMessage=' Business Created Successfully')

    else:

        return render_template('success.html', response='StatusMessage=' + response['Message'],
                               ErrorMessage='Message=' + response['Message'])


@business.route('/detail', methods=['GET'])
def get_business():
    business_id=request.args.get('business_id')
    ein = request.args.get('ein')
    print(business_id)
    print(ein)
    response=get_business_detail_api(business_id, ein)
    return render_template('detail.html',response=response)


@business.route('/businesslist/')
def users():

    jwtToken = JwtGeneration.get_jwt_token()

    print(jwtToken)

    JwtGeneration.get_access_token_by_jwt_token(jwtToken)

    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(10)

    get_business_request.set_from_date('03/20/2021')

    get_business_request.set_to_date('03/25/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']

    print(businesses)

    print(businesses[0]['BusinessId'])

    return render_template('business_list.html', businesses=businesses)


def create_business(businessName, einOrSSN):

    jwtToken = JwtGeneration.get_jwt_token()

    print(jwtToken)

    JwtGeneration.get_access_token_by_jwt_token(jwtToken)
    response = Business.create(businessName, einOrSSN)
    return response


def get_business_detail_api(businessId, einOrSSN):
    return Business.get_business_detail(businessId, einOrSSN)


if __name__ == '__main__':
    business.debug = True
    business.run()
