import os
import unittest
import zipfile

import emanifest
from emanifest import new_client


class TestEmanifestClient(unittest.TestCase):
    rcrainfo = new_client('preprod')

    def setUp(self) -> None:
        api_id = os.getenv('RCRAINFO_API_ID')
        api_key = os.getenv('RCRAINFO_API_KEY')
        print(api_key)
        print(api_id)
        if not api_id:
            self.fail('API ID not found to test integration')
        elif not api_key:
            self.fail('API Key not found to test integration')
        self.rcrainfo.auth(api_id, api_key)

    def test_initial_zip_state(self):
        rcra_response = self.rcrainfo.get_site_details('VATESTGEN001')
        self.assertIsNone(rcra_response.zip)

    def test_if_token_is_string(self):
        self.assertEqual(type("string"), type(self.rcrainfo.token))

    # RcrainfoResponse test
    def test_extracted_response_json_matches(self):
        resp = self.rcrainfo.get_site_details('VATESTGEN001')
        self.assertEqual(resp.response.json(), resp.json, "response.json() and json do not match")

    def test_decode_multipart_string(self):
        manifest_response = self.rcrainfo.get_attachments("000012345GBF")
        self.assertEqual(type(manifest_response.json), str)

    def test_decode_multipart_zipfile(self):
        manifest_response = self.rcrainfo.get_attachments("000012345GBF")
        self.assertEqual(type(manifest_response.zip), zipfile.ZipFile)

    # Specific method related testing
    def test_site_import(self):
        rcra_response = self.rcrainfo.get_site_details('VATESTGEN001')
        site_details = rcra_response.response.json()
        self.assertEqual(site_details['epaSiteId'], "VATESTGEN001")

    def test_check_mtn_exits(self):
        mtn = "100032934ELC"
        self.assertEqual(self.rcrainfo.check_mtn_exists(mtn).response.json()["manifestTrackingNumber"], mtn)

    def test_shipping_names(self):
        self.assertIn("Acetal", self.rcrainfo.get_shipping_names().response.json())

    def test_dot_numbers(self):
        self.assertIn("UN1088", self.rcrainfo.get_id_nums().response.json())

    def test_get_attachments(self):
        manifest_response = self.rcrainfo.get_attachments("000012345GBF")
        self.assertTrue(manifest_response.ok)


class TestRcrainfoClientIsExtendable:
    class MyClass(emanifest.RcrainfoClient):
        mock_api_id_from_external = 'an_api_id_from_someplace_else'
        mock_api_key_from_external = 'a_api_key_from_someplace_else'

        def retrieve_id(self, api_id=None) -> str:
            """
            This example method on our test subclass shows we can override the set_api_id method
            if the user wants to get their api ID from somewhere else (e.g., a service, or database)
            """
            returned_string = self.mock_api_id_from_external  # You could get this primitive value from anywhere
            return super().retrieve_id(returned_string)

        def retrieve_key(self, api_key=None) -> str:
            """
            This example method on our test subclass shows we can override the set_api_key method
            """
            returned_string = self.mock_api_key_from_external  # You could get this primitive value from anywhere
            return super().retrieve_id(returned_string)

    def test_set_api_id_override(self):
        my_subclass = self.MyClass('preprod')
        api_id_set_during_auth = my_subclass.retrieve_id()
        assert api_id_set_during_auth == self.MyClass.mock_api_id_from_external

    def test_set_api_key_override(self):
        my_subclass = self.MyClass('preprod')
        api_key_set_during_auth = my_subclass.retrieve_key()
        assert api_key_set_during_auth == self.MyClass.mock_api_key_from_external

    def test_set_api_id_method(self):
        my_subclass = self.MyClass('preprod')
        api_key_set_during_auth = my_subclass.retrieve_key()
        assert api_key_set_during_auth == self.MyClass.mock_api_key_from_external


class BadClient(unittest.TestCase):
    bad_rcrainfo = new_client('preprod')

    # test of initial state
    def test_bad_auth(self):
        self.bad_rcrainfo.auth(os.getenv('RCRAINFO_API_ID'), 'a_bad_api_key')
        self.assertIsNone(self.bad_rcrainfo.token)

    def test_client_token_state(self):
        unauthorized_client = new_client('preprod')
        self.assertIsNone(unauthorized_client.token)


if __name__ == '__main__':
    unittest.main()
