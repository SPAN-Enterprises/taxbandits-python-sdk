from api_services import Form1099MISC


def create_form1099_misc(formRequest):
    response = Form1099MISC.create(formRequest)
    return response.json()

