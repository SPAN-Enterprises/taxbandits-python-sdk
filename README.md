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
- Transmit Form W2 ​

## Configuration

​ You need to signup with TaxBandits Sandbox Developer Console at https://sandbox.taxbandits.com to get the keys to run
the SDK. See below for more directions:

### To get the sandbox keys:

- Go to Sandbox Developer console: https://sandbox.taxbandits.com. ​
- Signup or signin to Sandbox ​
- Navigate to Settings and then to API Credentials. Copy Client Id, Client Secret and User Token. ​ ​

### The sandbox URLs: (Please make sure to use the right versions)

- Sandbox Auth Server: https://testoauth.expressauth.net/v2/tbsauth ​
- API Server: https://testapi.taxbandits.com/v1.6.1 ​
- Sandbox Application URL: https://testapp.taxbandits.com ​
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

### Project Folder Structure

* controllers:
    - The users input data are parsed and request models are constructed here.
    - All API response validations are also done here.
    - UI rendering logics (example, the dropdown values and default value mappings) are also included in the controllers.
    

* api_services:
    - All TaxBandits API invocations and logics are done here.
    - Included the JWS generation and Authentication is done here.
    

* models:
    - This folder contains the request and response models of all the API end points.
    

* static:
    - This folder contains static files (images and css) that are used in this project.
    

* templates:
    - All our HTML pages are placed under this folder. 
    

* utils:
    - Config.py:
        - Client Id, Secret Id and User Token of the TaxBandits User credentials are stored here.
        - API base URLs are maintained here.
    - EndPointConfig.py:
        - All the EndPoints accessed in this project are saved in this file.
    - HeaderUtils.py:
        - Header details for invoking TaxBandits APIs are generated and processed here.
        - These header details will be passed during each EndPoint invocation.
    - SignatureValidation.py:
        - Webhook signature validations are done here to check if the webhook is triggered by TaxBandits.

### Complete Documentation

​ Please refer the following link for the complete API documentation that covers all the API methods with their sample request and response.

​ https://developer.taxbandits.com/docs/

​ Also refer our medium articles for more help.

​ https://taxbanditsdev.medium.com/


### Contact Details

​ Email: developer@taxbandits.com  
​ Phone: 704.684.4751
