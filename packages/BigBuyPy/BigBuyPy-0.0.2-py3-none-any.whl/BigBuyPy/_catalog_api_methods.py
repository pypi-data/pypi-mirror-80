import requests
import json


class CatalogMixin:
    def __init__(self):
        raise NotImplementedError("This Class is not supposed to be instantiated")

    def getStocks(self, sku_list: list):
        if not skuListIsValid(sku_list):
            raise ValueError("Invalid Sku List, must be like ['V0103138',...]")

        data = {
            "product_stock_request": {"products": [{"sku": sku} for sku in sku_list]}
        }
        data = json.dumps(data)
        response = requests.post(
            self.chosen_endpoint + "/rest/catalog/productsstockbyreference",
            data,
            headers={"Authorization": self.api_key},
        )
        return response


def skuListIsValid(sku_list: list):
    if isinstance(sku_list, list) and all(isinstance(sku, str) for sku in sku_list):
        return True
    return False


def createTemplateFunctionType1(endpoint):
    def function_template(self):
        response = requests.get(
            self.chosen_endpoint + endpoint,
            params={"_format": "json"},
            headers={"Authorization": self.api_key},
        )
        return response

    return function_template


def createTemplateFunctionType2(endpoint):
    def function_template(self, id: int):
        assert isinstance(id, int), "Invalid ID, must be an integer"
        response = requests.get(
            self.chosen_endpoint + endpoint + "/" + str(id),
            params={"_format": "json"},
            headers={"Authorization": self.api_key},
        )
        return response

    return function_template


funcs_type2 = {
    "getCategory": "/rest/catalog/category",
    "getCategoryAllLanguages": "/rest/catalog/categoryalllanguages",
    "getManufacturer": "/rest/catalog/manufacturer",
    "getProduct": "/rest/catalog/product",
    "getProductCategories": "/rest/catalog/productcategories",
    "getProductImages": "/rest/catalog/productimages",
    "getProductInformation": "/rest/catalog/productinformation",
    "getProductInformationAllLanguages": "/rest/catalog/productinformationalllanguages",
    "getProductInformationBySKU": "/rest/catalog/productinformationbysku",
    "getProductStock": "/rest/catalog/productstock",
    "getProductTags": "/rest/catalog/producttags",
    "getProductVariations": "/rest/catalog/productvariations",
    "getProductVariationsStock": "/rest/catalog/productvariationsstock",
    "getTag": "/rest/catalog/tag",
    "getTagAllLanguages": "/rest/catalog/tagalllanguages",
    "getVariation": "/rest/catalog/variation",
    "getAttribute": "/rest/catalog/attribute",
    "getAttributeAllLanguages": "/rest/catalog/attributealllanguages",
    "getAttributeGroup": "/rest/catalog/attributegroup",
    "getAttributeGroupAllLanguages": "/rest/catalog/attributegroupalllanguages",
}
funcs_type1 = {
    "getAllProducts": "/rest/catalog/products",
    "getAllStocks": "/rest/catalog/productsstock",
    "getAllAvailableStocks": "/rest/catalog/productsstockavailable",
    "getAllAttributeGroups": "/rest/catalog/attributegroups",
    "getAllAttributes": "/rest/catalog/attributes",
    "getAllCategories": "/rest/catalog/categories",
    "getAllLanguages": "/rest/catalog/languages",
    "getAllManufacturers": "/rest/catalog/manufacturers",
    "getAllProductCategories": "/rest/catalog/productsstock",
    "getAllProductImages": "/rest/catalog/productsimages",
    "getAllProductInformation": "/rest/catalog/productsinformation",
    "getAllProductTags": "/rest/catalog/productsstock",
    "getAllProductVariations": "/rest/catalog/productsvariations",
    "getAllProductVariationsStock": "/rest/catalog/productsvariationsstock",
    "getAllAvailableProductVariationsStock": "/rest/catalog/productsvariationsstockavailable",
    "getAllTags": "/rest/catalog/tags",
    "getAllVariations": "/rest/catalog/variations",
}

for func in funcs_type1:
    setattr(CatalogMixin, func, createTemplateFunctionType1(funcs_type1[func]))

for func in funcs_type2:
    setattr(CatalogMixin, func, createTemplateFunctionType2(funcs_type2[func]))
