import requests


class ModuleMixin:
    def __init__(self):
        raise NotImplementedError("This Class is not supposed to be instantiated")

    def getAllModules(self):
        response = requests.get(self.chosen_endpoint + "/rest/module/",
                                params={"_format": 'json'},
                                headers={"Authorization": self.api_key})
        return response

    def getAllModulePlatforms(self):
        response = requests.get(self.chosen_endpoint + "/rest/module/platforms",
                                params={"_format": 'json'},
                                headers={"Authorization": self.api_key})
        return response
