import requests

def createFunction(*args, **kwargs):
    def function_template(*args, **kwargs):
        response = requests.get(
            self.chosen_endpoint + "/rest/catalog/products",
            params={"_format": "json"},
            headers={"Authorization": self.api_key},
        )
        return response.json()

    return function_template
