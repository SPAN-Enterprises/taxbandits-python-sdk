import json

from api_services import Business, JwtGeneration,Form1099NEC
from flask import Flask, render_template, request
import json

from core.BusinessList import Businesses
from core.GetBusinssList import BusinessListRequest
from core.CreateBusinessRequest import CreateBusinessRequest

business = Flask(__name__)
global jwtToken


@business.route('/')
def index():
    return render_template('index.html')


@business.route('/createbusiness', methods=['get'])
def loadCreateBusiness():
    return render_template('createbusiness.html')

# Create Form 1099 NEC
@business.route('/createForm1099NEC', methods=['get'])
def loadCreateForm1099NEC():
    return render_template('create_form_1099_nec.html')


@business.route('/success', methods=['POST'])
def submit():
    input_request_json = request.form.to_dict(flat=False)

    print(input_request_json)

    response = create_business(input_request_json)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' +
                                        response[
                                            'BusinessId'], ErrorMessage=' Business Created Successfully')
    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))

@business.route('/create1099nec', methods=['GET'])
def submitCreateForm1099NEC():
    input_request_json = request.form.to_dict(flat=False)

    print(input_request_json)

    response = create_form1099_nec(input_request_json)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' +
                                        response[
                                            'BusinessId'], ErrorMessage=' Business Created Successfully')
    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))


@business.route('/detail', methods=['GET'])
def get_business():
    business_id = request.args.get('business_id')
    ein = request.args.get('ein')
    print(business_id)
    print(ein)
    response = get_business_detail_api(business_id, ein)
    return render_template('detail.html', response=response)


@business.route('/businesslist/', methods=['GET'])
def users():
    jwtToken = JwtGeneration.get_jwt_token()

    print(jwtToken)

    JwtGeneration.get_access_token_by_jwt_token(jwtToken)

    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(20)

    get_business_request.set_from_date('03/20/2021')

    get_business_request.set_to_date('03/31/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']

    print(businesses)

    print(businesses[0]['BusinessId'])

    return render_template('business_list.html', businesses=businesses)


def create_business(requestJson):
    jwtToken = JwtGeneration.get_jwt_token()

    print(jwtToken)

    JwtGeneration.get_access_token_by_jwt_token(jwtToken)
    response = Business.create(requestJson)
    return response

def create_form1099_nec(name, tin):
    jwtToken = JwtGeneration.get_jwt_token()

    print(jwtToken)

    JwtGeneration.get_access_token_by_jwt_token(jwtToken)
    response = Form1099NEC.create()
    return response


def get_business_detail_api(businessId, einOrSSN):
    return Business.get_business_detail(businessId, einOrSSN)


@business.route('/ReadBusinessList', methods=['GET'])
def get_businessList():
    jwtToken = JwtGeneration.get_jwt_token()

    print(jwtToken)

    JwtGeneration.get_access_token_by_jwt_token(jwtToken)

    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(20)

    get_business_request.set_from_date('03/20/2021')

    get_business_request.set_to_date('03/31/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']
    print(businesses)

    businessIdList = []

    for businessVal in businesses:
        businessIdList.append(businessVal.get('BusinessNm') + " "+businessVal.get('EINorSSN'))

    print(f"Business Id List = {businessIdList}")

    return render_template('create_form_1099_nec.html', businesses=businessIdList)

if __name__ == '__main__':
    business.debug = True
    business.run()
