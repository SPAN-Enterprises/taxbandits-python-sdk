import json


class Form10991099CreateRequest:

    def __init__(self):
        self.BusinessNm = ''

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    # def __repr__(self):
    #     return f'<CreateBusinessRequest {self.first_name}>'

    def get_SubmissionManifest(self):
        return self.SubmissionManifest

    def set_SubmissionManifest(self, submissionManifest):
        self.SubmissionManifest = submissionManifest

    def get_ReturnHeader(self):
        return self.ReturnHeader

    def set_ReturnHeader(self, ReturnHeader):
        self.ReturnHeader = ReturnHeader

    def get_ReturnData(self):
        return self.ReturnData

    def set_ReturnData(self, ReturnData):
        self.ReturnData = ReturnData
