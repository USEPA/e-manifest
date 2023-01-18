import os
import unittest
import zipfile

from emanifest import new_client


class TestEmanifestClient(unittest.TestCase):
    rcra_client = new_client('preprod')

    def setUp(self) -> None:
        api_id = os.getenv('RCRAINFO_API_ID')
        api_key = os.getenv('RCRAINFO_API_KEY')
        if not api_id:
            self.fail('API ID not found to test integration')
        elif not api_key:
            self.fail('API Key not found to test integration')
        self.rcra_client.auth(api_id, api_key)

    def test_initial_zip_state(self):
        rcra_response = self.rcra_client.get_site_details('VATESTGEN001')
        self.assertIsNone(rcra_response.zip)

    def test_if_token_is_string(self):
        self.assertEqual(type("string"), type(self.rcra_client.token))

    # RcrainfoResponse test
    def test_extracted_response_json_matches(self):
        resp = self.rcra_client.get_site_details('VATESTGEN001')
        self.assertEqual(resp.response.json(), resp.json, "response.json() and json do not match")

    def test_decode_multipart_string(self):
        manifest_response = self.rcra_client.get_attachments("000012345GBF")
        self.assertEqual(type(manifest_response.json), str)

    def test_decode_multipart_zipfile(self):
        manifest_response = self.rcra_client.get_attachments("000012345GBF")
        self.assertEqual(type(manifest_response.zip), zipfile.ZipFile)

    # Specific method related testing
    def test_site_import(self):
        rcra_response = self.rcra_client.get_site_details('VATESTGEN001')
        site_details = rcra_response.response.json()
        self.assertEqual(site_details['epaSiteId'], "VATESTGEN001")

    def test_check_mtn_exits(self):
        mtn = "100032934ELC"
        self.assertEqual(self.rcra_client.check_mtn_exists(mtn).response.json()["manifestTrackingNumber"], mtn)

    def test_shipping_names(self):
        self.assertIn("Acetal", self.rcra_client.get_shipping_names().response.json())

    def test_dot_numbers(self):
        self.assertIn("UN1088", self.rcra_client.get_id_nums().response.json())

    def test_get_attachments(self):
        manifest_response = self.rcra_client.get_attachments("000012345GBF")
        self.assertTrue(manifest_response.ok)


class BadClient(unittest.TestCase):
    rcra_client = new_client('preprod')

    # test of initial state
    def test_bad_auth(self):
        self.rcra_client.auth(os.getenv('RCRAINFO_API_ID'), 'a_bad_api_key')
        self.assertIsNone(self.rcra_client.token)

    def test_client_token_state(self):
        unauthorized_client = new_client('preprod')
        self.assertIsNone(unauthorized_client.token)


if __name__ == '__main__':
    unittest.main()
