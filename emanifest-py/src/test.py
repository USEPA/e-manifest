import os
import unittest

import requests

from emanifest import client

cl = client.new_client('preprod')
cl.Auth(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))

# test = cl.GetHandler('VATESTGEN001')
# print(test)


class EManTest(unittest.TestCase):
    def test_if_token_is_string(self):
        self.assertEqual(type("string"), type(cl.token))

    def test_site_import(self):
        rcra_response = cl.GetSiteDetails('VATESTGEN001')
        site_details = rcra_response.response.json()
        self.assertEqual(site_details['epaSiteId'], "VATESTGEN001")

    def test_check_mtn_exits(self):
        mtn = "100032934ELC"
        self.assertEqual(cl.CheckMTNExists(mtn).response.json()["manifestTrackingNumber"], mtn)

    def test_shipping_names(self):
        self.assertIn("Acetal", cl.GetShippingNames().response.json())

    def test_dot_numbers(self):
        self.assertIn("UN1088", cl.GetIDNums().response.json())


if __name__ == '__main__':
    unittest.main()
