from api_services import Business, JwtGeneration
from core import BusinessList
from core.GetBusinssList import BusinessListRequest

jwtToken = JwtGeneration.get_jwt_token()

print(jwtToken)

access_token = JwtGeneration.get_access_token_by_jwt_token(jwtToken)

get_business_request = BusinessListRequest()

get_business_request.set_page(1)

get_business_request.set_page_size(10)

get_business_request.set_from_date('03/20/2021')

get_business_request.set_to_date('03/25/2021')

response = Business.get_business_list(get_business_request)


#params={"Page": 1, "PageSize": 10, "FromDate":"03/20/2021","ToDate":"03/25/2021"}

# Business.get_business("13100881-f74a-478c-93a2-832250783cce","633313330")