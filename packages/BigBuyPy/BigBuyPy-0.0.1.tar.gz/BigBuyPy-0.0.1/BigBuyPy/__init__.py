from ._catalog_api_methods import CatalogMixin
from ._module_api_methods import ModuleMixin
from ._order_api_methods import OrderMixin
from ._shipping_api_methods import ShippingMixin
from ._tracking_api_methods import TrackingMixin
from ._user_api_methods import UserMixin

valid_formats = ["json", "xml", "html"]


def formatIsValid(response_format: str):
    if isinstance(response_format, str) and response_format in valid_formats:
        return True
    return False


class BigBuyManager(CatalogMixin, ModuleMixin, OrderMixin,
                    ShippingMixin, TrackingMixin, UserMixin):

    def __init__(self, api_key, sandbox=False):
        self.api_key = "Bearer " + api_key
        self.chosen_endpoint = "https://api.bigbuy.eu" if sandbox is False else "https://api.sandbox.bigbuy.eu"
