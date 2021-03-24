from api_services import Business, JwtGeneration

from flask import Flask, render_template, request


business = Flask(__name__)
global jwtToken

@business.route('/')
def index():
    return render_template('index.html')


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
            response = callAPI(BusinessName, EINOrSSN)

        if response['StatusCode']==200:

            return render_template('success.html', response='StatusMessage='+response['StatusMessage']+'<br>BusinessId ='+response['BusinessId'],ErrorMessage=' Business Created Successfully')

        else:

            return render_template('success.html', response='StatusMessage='+response['Message'],ErrorMessage='Message='+response['Message'])



@business.route('/list', methods=['GET'])
def getbusiness():
        businessId = request.args['business_id_get']
        ein = request.args['ein_get']
        response=  getBusinessAPI(businessId, ein)
        return render_template('success.html',response=response)



def callAPI(businessName, einOrSSN):
    jwtToken = JwtGeneration.get_jwt_token()
    print(jwtToken)
    access_token = JwtGeneration.get_access_token_by_jwt_token(jwtToken)
    response = Business.create(businessName, einOrSSN)
    return response

def getBusinessAPI(businessId, einOrSSN):
    jwtToken = JwtGeneration.get_jwt_token()
    print(jwtToken)
    access_token = JwtGeneration.get_access_token_by_jwt_token(jwtToken)
    return Business.get_business(businessId, einOrSSN)


if __name__ == '__main__':
    business.debug = True
    business.run()
