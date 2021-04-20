![TaxBandits Logo](/static/logo.png)
​
# TaxBandits Python Sample SDK
***
This is a sample project written on Python with Flask framework to show how to integrate with TaxBandits API. This covers the following API endpoints:
​
- OAuth 2.0 Authentication using JWT
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
- Transmit Form W2
​
## Configuration
​
You need to signup with TaxBandits Sandbox Developer Console at https://sandbox.taxbandits.com to get the keys to run the SDK. See below for more directions:
### To get the sandbox keys:
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
 "O_AUTH_BASE_URL": "https://testoauth.expressauth.net/v2/tbsauth",
 "TBS_API_BASE_URL": "https://testapi.taxbandits.com/v1.6.1/"
}
```
