![TaxBandits Logo](/static/logo.png)
​
# TaxBandits Python Sample SDK
***
This is a sample based on Python, Flask, ngrok, mongodb and JWT to show how to authenticate and handshake with TaxBandits API. This sample includes:
​
- Create Business
- View Businesses
- Create Form 1099-NEC
- View Form 1099-NEC
- Transmit Form 1099-NEC
​
## Configuration
​
You need to signup with TaxBandits Sandbox Developer Console at https://sandbox.taxbandits.com to get the keys to run the SDK. See below for more directions:
### To get the sandbox keys:
​
- Go to Sandbox Developer console: https://sandbox.taxbandits.com.
  ​
- Signup or signin to Sandbox
  ​
- Navigate to Settings and then to API Credentials. Copy Client Id, Client Secret and User Token.
  ​
​
### The sandbox urls: (Please make sure to use the right versions)
​
​
Sandbox Auth Server: https://testoauth.expressauth.net/v2/tbsauth
​

​
API Server: https://testapi.taxbandits.com/v1.6.1
​

​
Sandbox Application URL: https://testapp.taxbandits.com
​
## Requirements
Ensure you have Python 3.8.5 and above and pip version 21.0.1 and above



Install the packages into the pipenv virtual environment from Pipfile:
> pipenv install

Activate the Pipenv shell:
​
> pipenv shell


​
Under utils folder in Config.py add your client secret, client id, user token and auth/api endpoints. The file should look like this
​
```
userCredential = {
    "CLIENT_ID": "Your client id",
    "SECRET_ID": "Your Secret id",
    "USER_TOKEN": "Your User Token"
}
​
apiBaseUrls = {
 "O_AUTH_BASE_URL": "https://testoauth.expressauth.net/v1/tbsauth",
 "TBS_API_BASE_URL": "https://testapi.taxbandits.com/v1.6.0/"
}
```
## To view form transmitted to IRS
1. Configure ngrok
2. Add webhook URL to your Sandbox account
### Configure ngrok 
setup ngrok for webhook url and routing callback to localhost
Follow procedure in ngrok site to Install and [setup ngrok](https://ngrok.com/download)
### Add webhook URL to Sandbox account
1. Sign-in to your [TaxBandits Sandbox](https://sandbox.taxbandits.com/) account 
2. After successful sign-in go to settings 
3. Select Webhook option
4. Click Add Webhook
5. In Add Webhook dialog Select Event Type as __"PDF Complete"__
6. In Callback URL enter URL obtained via running ngrok utility

## Usage
```javascript {highlight=[1, 7]}
 > python main.py
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
