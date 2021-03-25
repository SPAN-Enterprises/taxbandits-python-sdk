from api_services import Business

from flask import Flask, render_template, request

business = Flask(__name__)
global jwtToken


@business.route('/')
def index():
    return render_template('index.html')


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
    business_id = request.args['business_id_get']
    ein = request.args['ein_get']
    response = get_business_detail_api(business_id, ein)
    return render_template('success.html', response=response)

@business.route('/users/')
def users():
    users = ['maateen', 'nabin', 'shadd']
    return render_template('business_list.html', users=users)


def create_business(businessName, einOrSSN):
    response = Business.create(businessName, einOrSSN)
    return response


def get_business_detail_api(businessId, einOrSSN):
    return Business.get_business_detail(businessId, einOrSSN)


if __name__ == '__main__':
    business.debug = True
    business.run()
