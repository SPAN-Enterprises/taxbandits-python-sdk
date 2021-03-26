import json


class CreateBusinessRequest:

    def __init__(self):
        self.BusinessNm = ''

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    # def __repr__(self):
    #     return f'<CreateBusinessRequest {self.first_name}>'

    def get_BusinessNm(self):
        return self.BusinessNm

    def set_BusinessNm(self, businessNm):
        self.BusinessNm = businessNm

    def get_TradeNm(self):
        return self.TradeNm

    def set_TradeNm(self, tradeNm):
        self.TradeNm = tradeNm

    def get_IsEIN(self):
        return self.IsEIN

    def set_IsEIN(self, isEIN):
        self.IsEIN = isEIN

    def get_EINorSSN(self):
        return self.EINorSSN

    def set_EINorSSN(self, einorssn):
        self.EINorSSN = einorssn

    def get_Email(self):
        return self.Email

    def set_Email(self, email):
        self.Email = email

    def get_ContactNm(self):
        return self.ContactNm

    def set_ContactNm(self, contactNm):
        self.ContactNm = contactNm

    def get_Phone(self):
        return self.Phone

    def set_Phone(self, phone):
        self.Phone = phone

    def get_PhoneExtn(self):
        return self.PhoneExtn

    def set_PhoneExtn(self, phoneExtn):
        self.PhoneExtn = phoneExtn

    def get_Fax(self):
        return self.Fax

    def set_Fax(self, fax):
        self.Fax = fax

    def get_BusinessType(self):
        return self.BusinessType

    def set_BusinessType(self, type):
        self.BusinessType = type

    def get_SigningAuthority(self):
        return self.SigningAuthority

    def set_SigningAuthority(self, signingAuthority):
        self.SigningAuthority = signingAuthority

    def get_KindOfEmployer(self):
        return self.KindOfEmployer

    def set_KindOfEmployer(self, kindOfEmployer):
        self.KindOfEmployer = kindOfEmployer

    def get_KindOfPayer(self):
        return self.KindOfPayer

    def set_KindOfPayer(self, kindOfPayer):
        self.KindOfPayer = kindOfPayer

    def get_IsBusinessTerminated(self):
        return self.IsBusinessTerminated

    def set_IsBusinessTerminated(self, isTerminated):
        self.IsBusinessTerminated = isTerminated

    def get_IsForeign(self):
        return self.IsForeign

    def set_IsForeign(self, isForign):
        self.IsForeign = isForign

    def get_USAddress(self):
        return self.USAddress

    def set_USAddress(self, usAddress):
        self.USAddress = usAddress

    def get_ForeignAddress(self):
        return self.ForeignAddress

    def set_ForeignAddress(self, foreignAddress):
        self.ForeignAddress = foreignAddress

        # "BusinessNm": businessName,
        #         "TradeNm": "Kodak",
        #         "IsEIN": True,
        #         "EINorSSN": einOrSSN,
        #         "Email": "subbuleaf+1@gmail.com",
        #         "ContactNm": "John",
        #         "Phone": "1234567890",
        #         "PhoneExtn": "12345",
        #         "Fax": "1234567890",
        #         "BusinessType": "ESTE",
        #         "SigningAuthority": SigningAuthority.signingAuthority,
        #         "KindOfEmployer": "FEDERALGOVT",
        #         "KindOfPayer": "REGULAR941",
        #         "IsBusinessTerminated": False,
        #         "IsForeign": True,
        #         "USAddress": USAddress.usAddress,
        #         "ForeignAddress": ForeignAddress.foreignAddress
