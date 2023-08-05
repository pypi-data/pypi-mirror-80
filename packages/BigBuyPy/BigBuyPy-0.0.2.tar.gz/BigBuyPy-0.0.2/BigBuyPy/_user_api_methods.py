import requests


class UserMixin:
    def __init__(self):
        raise NotImplementedError("This Class is not supposed to be instantiated")

    def getPurseMoney(self):
        response = requests.get(self.chosen_endpoint + "/rest/user/purse",
                                params={"_format": 'json'},
                                headers={"Authorization": self.api_key})
        return response
