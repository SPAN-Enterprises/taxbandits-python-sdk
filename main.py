from api_services import Business, JwtGeneration

jwtToken = JwtGeneration.get_jwt_token()

print(jwtToken)

access_token = JwtGeneration.get_access_token_by_jwt_token(jwtToken)

response = Business.create()

# Business.get_business("13100881-f74a-478c-93a2-832250783cce","633313330")