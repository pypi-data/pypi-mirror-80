import unittest
import os
from BigBuyPy import BigBuyManager


class catalogTest(unittest.TestCase):

    def test_upper(self):
        api_key = os.environ.get('API_KEY', None)
        self.assertIsNot(api_key, None, "API_KEY not found")
        manager = BigBuyManager(api_key)

        response = manager.getProduct(1)
        self.assertTrue(response.ok, "Get Product not working")
