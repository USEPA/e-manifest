import os
import unittest
import zipfile

import requests

from emanifest import client


# utility function used by most of the integration tests
def new_client_and_auth():
    cl = client.new_client('preprod')
    cl.Auth(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))
    return cl


class EManTest(unittest.TestCase):

    # test of initial state
    def test_bad_auth(self):
        rcra_client = client.new_client('preprod')
        rcra_client.Auth(os.getenv('RCRAINFO_API_ID'), 'a_bad_api_key')
        self.assertIsNone(rcra_client.token)

    def test_client_token_state(self):
        unauthorized_client = client.new_client('preprod')
        self.assertIsNone(unauthorized_client.token)

    def test_initial_zip_state(self):
        cl = new_client_and_auth()
        rcra_response = cl.GetSiteDetails('VATESTGEN001')
        self.assertIsNone(rcra_response.zip)

    # Authentacious test
    def test_bad_auth(self):
        rcra_client = client.new_client('preprod')
        rcra_client.Auth(os.getenv('RCRAINFO_API_ID'), 'a_bad_api_key')
        self.assertIsNone(rcra_client.token)

    def test_if_token_is_string(self):
        cl = new_client_and_auth()
        self.assertEqual(type("string"), type(cl.token))

    # RcrainfoResponse test
    def test_extracted_response_json_matches(self):
        cl = new_client_and_auth()
        resp = cl.GetSiteDetails('VATESTGEN001')
        self.assertEqual(resp.response.json(), resp.json, "response.json() and json do not match")

    def test_decode_multipart_string(self):
        cl = new_client_and_auth()
        manifest_response = cl.GetAttachments("000012345GBF")
        self.assertEqual(type(manifest_response.json), str)

    def test_decode_multipart_zipfile(self):
        cl = new_client_and_auth()
        manifest_response = cl.GetAttachments("000012345GBF")
        self.assertEqual(type(manifest_response.zip), zipfile.ZipFile)

    # Specific method related testing
    def test_site_import(self):
        cl = new_client_and_auth()
        rcra_response = cl.GetSiteDetails('VATESTGEN001')
        site_details = rcra_response.response.json()
        self.assertEqual(site_details['epaSiteId'], "VATESTGEN001")

    def test_extracted_response_json_matches(self):
        cl = new_client_and_auth()
        resp = cl.GetSiteDetails('VATESTGEN001')
        self.assertEqual(resp.response.json(), resp.json, "response.json() and json do not match")

    def test_check_mtn_exits(self):
        cl = new_client_and_auth()
        mtn = "100032934ELC"
        self.assertEqual(cl.CheckMTNExists(mtn).response.json()["manifestTrackingNumber"], mtn)

    def test_shipping_names(self):
        cl = new_client_and_auth()
        self.assertIn("Acetal", cl.GetShippingNames().response.json())

    def test_dot_numbers(self):
        cl = new_client_and_auth()
        self.assertIn("UN1088", cl.GetIDNums().response.json())

    def test_get_attachments(self):
        cl = new_client_and_auth()
        manifest_response = cl.GetAttachments("000012345GBF")
        self.assertTrue(manifest_response.ok)

if __name__ == '__main__':
    unittest.main()
