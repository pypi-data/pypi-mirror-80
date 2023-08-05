import requests


class OrderMixin:
    def __init__(self):
        raise NotImplementedError("This Class is not supposed to be instantiated")

    def getOrderShippingAddressStructure(self):
        response = requests.get(self.chosen_endpoint + "/rest/order/addresses/new",
                                params={"_format": 'json'},
                                headers={"Authorization": self.api_key})
        return response

    def getOrderCarriersStructure(self):
        response = requests.get(self.chosen_endpoint + "/rest/order/carriers/new",
                                params={"_format": 'json'},
                                headers={"Authorization": self.api_key})
        return response
