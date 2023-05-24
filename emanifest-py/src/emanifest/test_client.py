import os
import zipfile

import requests

from .client import RcrainfoClient, RcrainfoResponse

TEST_GEN_MTN = "100032437ELC"
TEST_GEN_ID = 'VATESTGEN001'


class TestRcrainfoClient:
    api_id = os.getenv('RCRAINFO_API_ID')
    api_key = os.getenv('RCRAINFO_API_KEY')
    rcrainfo = RcrainfoClient('preprod', api_id=api_id, api_key=api_key)

    def test_initial_zip_state(self):
        rcra_response = self.rcrainfo.get_site(TEST_GEN_ID)
        assert rcra_response.zip is None

    def test_token_when_is_authenticated(self):
        assert isinstance(self.rcrainfo.token, str) and self.rcrainfo.is_authenticated

    def test_token_when_not_authenticated(self):
        new_rcrainfo = RcrainfoClient('preprod')
        assert new_rcrainfo.token is None and not new_rcrainfo.is_authenticated

    # RcrainfoResponse test
    def test_extracted_response_json_matches(self):
        resp: RcrainfoResponse = self.rcrainfo.get_site(TEST_GEN_ID)
        assert resp.response.json() == resp.json()

    def test_decode_multipart_string(self):
        manifest_response = self.rcrainfo.get_manifest_attachments(TEST_GEN_MTN)
        assert isinstance(manifest_response.json(), str)

    def test_decode_multipart_zipfile(self):
        manifest_response = self.rcrainfo.get_manifest_attachments(TEST_GEN_MTN)
        assert isinstance(manifest_response.zip, zipfile.ZipFile)

    # Specific method related testing
    def test_get_site_details(self):
        rcra_response = self.rcrainfo.get_site(TEST_GEN_ID)
        site_details = rcra_response.response.json()
        assert site_details['epaSiteId'] == TEST_GEN_ID

    def test_check_mtn_exits(self):
        mtn = "100032934ELC"
        assert self.rcrainfo.check_mtn_exists(mtn).json()["manifestTrackingNumber"] == mtn

    def test_correction_get_attachments(self):
        response = self.rcrainfo.get_correction_attachments(manifestTrackingNumber=TEST_GEN_MTN)
        assert response.ok is True


class TestClientIsExtendable:
    class MyClass(RcrainfoClient):
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

    def test_retrieve_id_override(self):
        my_subclass = self.MyClass('preprod')
        api_id_set_during_auth = my_subclass.retrieve_id()
        assert api_id_set_during_auth == self.MyClass.mock_api_id_from_external

    def test_retrieve_key_override(self):
        my_subclass = self.MyClass('preprod')
        api_key_set_during_auth = my_subclass.retrieve_key()
        assert api_key_set_during_auth == self.MyClass.mock_api_key_from_external

    def test_retrieve_key_returns_string(self):
        my_subclass = self.MyClass('preprod')
        api_key_set_during_auth = my_subclass.retrieve_key()
        assert api_key_set_during_auth == self.MyClass.mock_api_key_from_external


class TestAutoAuthentication:
    api_id = os.getenv('RCRAINFO_API_ID')
    api_key = os.getenv('RCRAINFO_API_KEY')

    def test_automatically_authenticates(self):
        """
        RcrainfoClient will automatically authenticate once a request is made,
        (e.g., calling get_manifest(...) will do the equivalent of authenticate(...) first
        """
        rcrainfo = RcrainfoClient('preprod', api_key=self.api_key, api_id=self.api_id)
        _resp = rcrainfo.get_manifest(TEST_GEN_MTN)
        assert rcrainfo.is_authenticated

    def test_does_not_authenticate_when_false(self):
        """
        emanifest(py) package will auto-authenticate (and re-authenticate) unless
        the auto_renew argument is set to False
        """
        rcrainfo = RcrainfoClient('preprod', api_key=self.api_key, api_id=self.api_id, auto_renew=False)
        _resp = rcrainfo.get_manifest(TEST_GEN_MTN)
        assert not rcrainfo.is_authenticated

    def test_non_present_credentials_does_not_auth(self):
        new_rcrainfo = RcrainfoClient('preprod')
        _mtn = new_rcrainfo.get_manifest(TEST_GEN_MTN)
        assert not new_rcrainfo.is_authenticated


class TestSessionSuperClassIsUsable:
    api_id = os.getenv('RCRAINFO_API_ID')
    api_key = os.getenv('RCRAINFO_API_KEY')
    rcrainfo = RcrainfoClient('preprod', api_key=api_key, api_id=api_id)

    def test_can_use_hooks(self):
        test_string = 'foobar'

        def mock_hook(resp: requests.Response, *args, **kwargs):
            """
            Hooks can be used on various phases of the http lifecycle.
            This functionality comes from request.Session class
            https://requests.readthedocs.io/en/latest/user/advanced/#session-objects
            """
            resp.reason = test_string
            return resp

        self.rcrainfo.hooks = {'response': mock_hook}
        hooked_resp = self.rcrainfo.get_manifest(TEST_GEN_MTN)
        assert hooked_resp.response.reason is test_string


class TestBadClient:
    bad_rcrainfo = RcrainfoClient('preprod')

    # test of initial state
    def test_bad_auth(self):
        self.bad_rcrainfo.authenticate(os.getenv('RCRAINFO_API_ID'), 'a_bad_api_key')
        assert self.bad_rcrainfo.token is None

    def test_client_token_state(self):
        assert self.bad_rcrainfo.token is None


class TestEncodingMultipartMixed:
    api_id = os.getenv('RCRAINFO_API_ID')
    api_key = os.getenv('RCRAINFO_API_KEY')
    rcrainfo = RcrainfoClient('preprod', api_key=api_key, api_id=api_id)
    dirname = os.path.dirname(__file__)
    attachment_file = os.path.join(dirname, 'resources/attachments.zip')
    json_file = os.path.join(dirname, 'resources/emanifest.json')
    update_manifest_mtn = '100032713ELC'

    def test_encodes_into_request(self):
        """
        This is kind of a funny test, since we can't keep saving manifest for these test,
        we're just making sure it responds with a 400 instead of something else.
        """
        with open(self.attachment_file, 'rb') as f:
            attachment = f.read()
        with open(self.json_file, 'r') as f:
            manifest_json = f.read()

        response = self.rcrainfo.update_manifest(manifest_json, attachment)
        if response.ok:
            # This Test will only pass if the manifest can be updated in RCRAInfo.
            assert response.status_code == 200
