from api_services.FormW2 import generate_form_w2_request


def create_form_w2(requestJson):
    response = generate_form_w2_request(requestJson)
    return response

