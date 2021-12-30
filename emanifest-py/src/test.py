import os
import unittest
from emanifest import client

cl = client.new_client('preprod')
cl.Auth(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))


class EManTest(unittest.TestCase):
    def test_if_token_is_string(self):
        self.assertEqual(type("string"), type(cl.token))

    def test_site_import(self):
        site_details = cl.GetSiteDetails('VATESTGEN001')
        print(type(site_details))
        self.assertEqual(site_details['epaSiteId'], "VATESTGEN001")


if __name__ == '__main__':
    unittest.main()
