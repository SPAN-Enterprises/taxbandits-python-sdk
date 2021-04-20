![TaxBandits Logo](/static/logo.png)
​

# TaxBandits Python Sample SDK

***
This is a sample based on Python, Flask, ngrok, mongodb and JWT to show how to authenticate and handshake with
TaxBandits API. This sample includes:
​

- Create Business
- View Businesses
- Create Form 1099-NEC
- View Form 1099-NEC
- Transmit Form 1099-NEC
- Create Form 1099-MISC
- View Form 1099-MISC
- Transmit Form 1099-MISC
- Create Form W2
- View Form W2
- Transmit Form W2 ​

## Configuration

​ You need to signup with TaxBandits Sandbox Developer Console at https://sandbox.taxbandits.com to get the keys to run
the SDK. See below for more directions:

### To get the sandbox keys:

- Go to Sandbox Developer console: https://sandbox.taxbandits.com. ​
- Signup or signin to Sandbox ​
- Navigate to Settings and then to API Credentials. Copy Client Id, Client Secret and User Token. ​ ​

### The sandbox urls: (Please make sure to use the right versions)

​ ​ Sandbox Auth Server: https://testoauth.expressauth.net/v2/tbsauth
​

​ API Server: https://testapi.taxbandits.com/v1.6.1
​

​ Sandbox Application URL: https://testapp.taxbandits.com
​

## Requirements

Ensure you have Python 3.8.5 and above and pip version 21.0.1 and above

Install the packages into the pipenv virtual environment from Pipfile:
> pipenv install

Activate the Pipenv shell:
​
> pipenv shell


​ Under utils folder in Config.py add your client secret, client id, user token and auth/api endpoints. The file should
look like this ​

```
userCredential = {
    "CLIENT_ID": "Your client id",
    "SECRET_ID": "Your Secret id",
    "USER_TOKEN": "Your User Token"
}
​
apiBaseUrls = {
 "O_AUTH_BASE_URL": "https://testoauth.expressauth.net/v2/tbsauth",
 "TBS_API_BASE_URL": "https://testapi.taxbandits.com/v1.6.1/"
}
```

## To view form transmitted to IRS

Once the IRS accepts or rejects your Form, you will be notified using webhook. In order to configure webhook there are
several libraries available in Python. Some of them are,

1. ngrok
2. webhooks
3. Thorn and so on

In this project we have used __ngrok__ for configuring webhook.

1. Configure ngrok
2. Add webhook URL to your Sandbox account

### Configure ngrok

Setup ngrok for webhook url and routing callback to localhost Follow procedure in ngrok site to Install
and [setup ngrok](https://ngrok.com/download)

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

### Project Package Details

* controllers:
    - The users input data's are parsed and request models are constructed here.
    - All API response validations are also done here.
    
* api_services:
    - All TaxBandits API invocations and logics are done here
    - Includes JWS generation and TaxBandits JWT Authentication too
    - UI rendering logics is a part of it
    
* models:
    - This package holds the request and response models of all End Points
    
* static:
    - This package contains static image files that are used in this project.
    - Also holds CSS styling files that are used in our UI.
    
* templates:
    - All our HTML pages are placed under this package.
    
* utils:
    - Config.py:
        - Client Id, Secret Id and User Tokens of the TaxBandits User credentials are stored here.
        - EndPoints Base URLs are saved here
    - EndPointConfig.py:
        - All the EndPoints accessed in this project are saved in this file.
    - HeaderUtils.py:
        - Header details for invoking TaxBandits APIs are generated and processed here.
        - These header details will be passed in each EndPoint invocation.
    - SignatureValidation.py:
        - Webhook signature validations are done here in order to authorize if the webhook is triggered by TaxBandits or not.
