# signingAuthority = {
#     "Name": "John",
#     "Phone": "1234567890",
#     "BusinessMemberType": "ADMINISTRATOR"
#
#  }

class SigningAuthority:
    def get_SAName(self):
        return self.Name

    def set_SAName(self, name):
        self.Name = name

    def get_SAPhone(self):
        return self.Phone

    def set_SAPhone(self,phone):
        self.Phone = phone

    def get_SABusinessMemberType(self):
        return self.BusinessMemberType

    def set_SABusinessMemberType(self, type):
        self.BusinessMemberType = type
