from core import SigningAuthority
from core import ForeignAddress
from core import USAddress

Create = {
    "BusinessNm": "Subbu LLC",
    "TradeNm": "Kodak",
    "IsEIN": True,
    "EINorSSN": "733313330",
    "Email": "subbuleaf+1@gmail.com",
    "ContactNm": "John",
    "Phone": "1234567890",
    "PhoneExtn": "12345",
    "Fax": "1234567890",
    "BusinessType": "ESTE",
    "SigningAuthority": SigningAuthority.signingAuthority,
    "KindOfEmployer": "FEDERALGOVT",
    "KindOfPayer": "REGULAR941",
    "IsBusinessTerminated": False,
    "IsForeign": True,
    "USAddress": USAddress.usAddress,
    "ForeignAddress": ForeignAddress.foreignAddress
}
