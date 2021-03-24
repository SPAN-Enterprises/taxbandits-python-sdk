import re


def isValidBusinessId(businessId):
    pattern = re.compile('[^a-zA-Z\s\-\']')
    return pattern.match(businessId)


def isValidEIN(ein):
    data = str(ein)
    return 0 < len(data) < 9
