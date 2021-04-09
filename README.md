![TaxBandits Logo](/static/logo.png)

#TaxBandits Python Sample SDK
***
This is a sample based on Python, Flask and JWT to show how to authenticate and handshake with TaxBandits API. This sample includes:

- An endpoint which returns the businesses
- Create Buisness
- View Businesses
- Create Form 1099-NEC
- View Form 1099-NEC
- Transmit Form 1099-NEC
## Requirements
Ensure you have Python 3.6 and above and pip version 21.0.1 and above

1. pip install pipenv

2. pip install flask

3. pip install pyjwt

4. pip install requests

5. pip install time

> In case of any error in import statement run the following command

> pip install --upgrade werkzeug==0.12.2

## Usage

```javascript {highlight=[1, 10]}
 > python business.py
 * Serving Flask app "business" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 291-359-924
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
## Configuration

You need to signup with TaxBandits Sandbox Developer Console at https://sandbox.taxbandits.com to get the keys to run the SDK. See below for more directions:
### To get the sandbox keys:
​

- Go to Sandbox Developer console: https://sandbox.taxbandits.com.
  ​
- Signup or signin to Sandbox
  ​
- Navigate to Settings and then to API Credentials. Copy Client Id, Client Secret and User Token.
  ​

### The sandbox urls: (Please make sure to use the right versions)

​
Sandbox Auth Server: https://testoauth.expressauth.net/v2/tbsauth
​

API Server: https://testapi.taxbandits.com/v1.6.1
​

Sandbox Application URL: https://testapp.taxbandits.com 