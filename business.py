
from flask import Flask, render_template, request

business = Flask(__name__)


@business.route('/')
def index():
    return render_template('index.html')


@business.route('/success', methods=['POST'])
def submit():
    if request.method=='POST':
        BusinessName =request.form['business_name']
        EINOrSSN =request.form['einorssn']
        print(BusinessName ,EINOrSSN)

        if BusinessName == '' or EINOrSSN == '':
            return render_template('index.html', message='Please enter required fields')

        elif len(EINOrSSN) <=8:
            return render_template('index.html', message='Please enter valid inut')

        return render_template('success.html')


if __name__ == '__main__':
 business.debug =True
 business.run()
