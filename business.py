from api_services import Business
from flask import Flask, render_template, request

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
    EINOrSSN = request.form['einorssn']
    print(BusinessName, EINOrSSN)

    if BusinessName == '' or EINOrSSN == '':
        return render_template('index.html', message='Please enter required fields')

    elif len(EINOrSSN) < 9:
        return render_template('index.html', message='Please enter valid input')

    else:
        response = create_business(request)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' + response[
                                   'BusinessId'], ErrorMessage=' Business Created Successfully')

    else:

        return render_template('success.html', response='StatusMessage=' + response['Message'],
                               ErrorMessage='Message=' + response['Message'])


@business.route('/detail', methods=['GET'])
def get_business():
    business_id = request.args['business_id_get']
    ein = request.args['ein_get']
    response = get_business_detail_api(business_id, ein)
    return render_template('success.html', response=response)


def create_business(request):
    response = Business.create(request)
    return response


def get_business_detail_api(businessId, einOrSSN):
    return Business.get_business_detail(businessId, einOrSSN)


if __name__ == '__main__':
    business.debug = True
    business.run()
