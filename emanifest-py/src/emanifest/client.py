"""
e-Manifest library for using the e-Manifest API
see https://github.com/USEPA/e-manifest
"""

import io
import json
import zipfile
from datetime import datetime, timezone
from typing import (
    Generic,
    List,
    Literal,
    Optional,
    TypeVar,
)

from requests import Request, Response, Session
from requests_toolbelt.multipart import decoder, encoder  # type: ignore
from typing_extensions import Unpack

from .types import (
    AgencyCode,
    CorrectionRevertResponse,
    CorrectionVersionSearchArgs,
    Manifest,
    ManifestExistsResponse,
    ManifestOperationResponse,
    ManifestSignatureResponse,
    MtnSearchArgs,
    PortOfEntry,
    RcraCodeDescription,
    RcraSite,
    SearchBillArgs,
    SignManifestArgs,
    SiteExistsResponse,
    SiteSearchArgs,
    UILinkArgs,
    UserSearchArgs,
    UserSearchResponse,
)

RCRAINFO_PROD = "https://rcrainfo.epa.gov/rcrainfoprod/rest/api/"
RCRAINFO_PREPROD = "https://rcrainfopreprod.epa.gov/rcrainfo/rest/api/"

T = TypeVar("T")


class RcrainfoResponse(Generic[T]):
    """
    RcrainfoResponse wraps around the requests library's Response object.
    The complete Response object can be accessed as self.response

    Attributes:
        response (Response) the request library response object.
    """

    def __init__(self, response: Response):
        self.response: Response = response
        self._multipart_json: T | None = None
        self._multipart_zip: Optional[zipfile.ZipFile] = None

    def json(self) -> T:
        if self._multipart_json:
            return self._multipart_json
        else:
            return self.response.json()

    @property
    def ok(self):
        if self.response.ok:
            return self.response.ok
        else:
            return False

    @property
    def status_code(self):
        if self.response.status_code is not None:
            return self.response.status_code
        else:
            return None

    @property
    def zip(self):
        if self._multipart_zip:
            return self._multipart_zip
        else:
            return None

    def __str__(self):
        return f"{self.__class__.__name__}: status {self.response.status_code}"

    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.status_code}]>"

    def __bool__(self):
        """returns True if status code < 400"""
        return self.ok

    def decode(self):
        multipart_data = decoder.MultipartDecoder.from_response(self.response)
        for part in multipart_data.parts:
            if part.headers[b"Content-Type"] == b"application/json":
                self._multipart_json = part.text
            else:
                zip_contents = zipfile.ZipFile(io.BytesIO(part.content))
                self._multipart_zip = zip_contents


class RcrainfoClient(Session):
    """
    A http client for using the RCRAInfo (e-Manifest) Restful web services.
    """

    # see datetime docs https://docs.python.org/3.11/library/datetime.html#strftime-strptime-behavior
    # acceptable date format(s) [yyyy-MM-dd'T'HH:mm:ssZ,yyyy-MM-dd'T'HH:mm:ss.SSSZ]
    __expiration_fmt = "%Y-%m-%dT%H:%M:%S.%f%z"
    __signature_date_fmt = "%Y-%m-%dT%H:%M:%SZ"
    __default_headers = {"Accept": "application/json"}
    __default_timeout = 10

    def __init__(
        self, base_url: str, *, api_id=None, api_key=None, timeout=10, auto_renew=True
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.__token = None
        self.__token_expiration_utc = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        self.__api_key = api_key
        self.__api_id = api_id
        self.headers.update(self.__default_headers)
        self.auto_renew = auto_renew

    @property
    def base_url(self):
        """RCRAInfo base URL, either for Production ('prod') or Preproduction ('preprod')"""
        return self.__base_url

    @base_url.setter
    def base_url(self, value):
        self.__base_url = _parse_url(value)

    @property
    def timeout(self):
        """Http request timeout"""
        return self.__timeout

    @timeout.setter
    def timeout(self, value) -> None:
        if isinstance(value, (int, float)):
            self.__timeout = value
        else:
            self.__timeout = self.__default_timeout

    @property
    def token_expiration(self) -> datetime:
        """Token expiration datetime object. Read only."""
        return self.__token_expiration_utc

    def __set_token_expiration(self, expiration: str) -> None:
        try:
            self.__token_expiration_utc = datetime.strptime(
                expiration, self.__expiration_fmt
            ).replace(tzinfo=timezone.utc)
        except ValueError:
            self.__token_expiration_utc = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

    @property
    def token(self):
        """Session token from Rcrainfo. Read Only."""
        return self.__token

    @property
    def is_authenticated(self) -> bool:
        """Returns True if the RcrainfoClient token exists and has not expired."""
        try:
            if (
                self.token_expiration > datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
                and self.token is not None
            ):
                return True
            else:
                return False
        except TypeError:
            return False

    @property
    def expiration_format(self) -> str:
        """Datetime format used by RCRAInfo for token expiration. Read only."""
        return self.__expiration_fmt

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}('{self.base_url}', auto_renew={self.auto_renew}, "
            f"api_id={self.__api_id}, api_key={self.__api_key})>"
        )

    def __rcra_request(
        self, method, endpoint, *, headers=None, multipart=None, stream=False, **kwargs
    ) -> RcrainfoResponse:
        """Client internal method for making requests to RCRAInfo"""

        # If auto_renew is True, check if the token is expired and, if needed, re-authenticate.
        if self.auto_renew and not self.is_authenticated:
            self.__get_token()

        # decide if, and what, we need to put into the body of our request.
        if method in ("POST", "PUT", "PATCH"):
            if multipart is not None:
                data = multipart
            else:
                data = json.dumps(dict(**kwargs))
        else:
            data = None

        # Initiate the http request object
        request = Request(method, url=endpoint, data=data)

        # If additional headers are passed, attach and/or overwrite
        if headers is not None:
            request.headers = {**request.headers, **headers}

        prepared_req = self.prepare_request(request)
        return RcrainfoResponse(self.send(prepared_req, timeout=self.timeout, stream=stream))

    def __get_token(self) -> None:
        """
        used to retrieve a session token from RCRAInfo, only request that (intentionally) does
        not use __rcra_request
        """
        self.__api_id = self.retrieve_id()
        self.__api_key = self.retrieve_key()
        auth_url = f"{self.base_url}v1/auth/{self.__api_id}/{self.__api_key}"
        resp = self.get(auth_url, timeout=self.timeout)
        # ToDo: TypeError exception handling
        if resp.ok:
            self.__token = resp.json()["token"]
            self.headers.update({"Authorization": f"Bearer {self.token}"})
            self.__set_token_expiration(resp.json()["expiration"])

    @staticmethod
    def __encode_manifest(
        manifest_json: dict,
        zip_bytes: bytes | None = None,
        *,
        json_name: str = "manifest.json",
        zip_name="attachments.zip",
    ):
        """emanifest-py internal helper function to encode json and zip file for upload"""
        if zip_bytes:
            return encoder.MultipartEncoder(
                fields={
                    "manifest": (
                        json_name,
                        json.dumps(manifest_json),
                        "application/json",
                    ),
                    "attachment": (zip_name, zip_bytes, "application/zip"),
                }
            )
        else:
            return encoder.MultipartEncoder(
                fields={
                    "manifest": (
                        json_name,
                        json.dumps(manifest_json),
                        "application/json",
                    ),
                }
            )

    def retrieve_id(self, api_id=None) -> str:
        """
        Getter method used internally to retrieve the desired RCRAInfo API ID. Can be overridden
        to automatically support retrieving an API ID from an external location.
        Args:
            api_id:

        Returns:
            string of the user's RCRAInfo API ID
        """
        if api_id:
            return api_id
        elif self.__api_id:
            return self.__api_id
        else:
            return ""

    def retrieve_key(self, api_key: str | None = None) -> str:
        """
        Getter method used internally to retrieve the desired RCRAInfo API key. Can be overridden
        to support retrieving an API Key from an external location.
        """
        if api_key:
            return api_key
        elif self.__api_key:
            return self.__api_key
        else:
            return ""

    # Below this line are the high level methods to request RCRAInfo/e-Manifest
    def authenticate(self, api_id=None, api_key=None) -> None:
        """
        Authenticate user's RCRAInfo API ID and Key to generate token for use by other functions

        Args:
            api_id (str): API ID of RCRAInfo User with Site Manager level permission.
            api_key (str): User's RCRAInfo API key. Generated alongside the api_id in RCRAInfo
        """
        # if api credentials are passed, set the client's attributes
        if api_id is not None:
            self.__api_id = str(api_id)
        if api_key is not None:
            self.__api_key = str(api_key)
        self.__get_token()

    def get_site(self, epa_id: str) -> RcrainfoResponse[RcraSite]:
        """
        Retrieve site details for a given Site ID

        Args:
            epa_id (str): EPA site ID
        """
        endpoint = f"{self.base_url}v1/site-details/{epa_id}"
        return self.__rcra_request("GET", endpoint)

    def get_hazard_classes(self) -> RcrainfoResponse[List[str]]:
        """Retrieve all DOT Hazard Classes"""
        endpoint = f"{self.base_url}v1/emanifest/lookup/hazard-classes"
        return self.__rcra_request("GET", endpoint)

    def get_packing_groups(self) -> RcrainfoResponse[List[str]]:
        """Retrieve all DOT Packing Groups"""
        endpoint = f"{self.base_url}v1/emanifest/lookup/packing-groups"
        return self.__rcra_request("GET", endpoint)

    def get_haz_class_sn_id(self, ship_name: str, id_num: str) -> RcrainfoResponse[List[str]]:
        """
        Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number

        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/"
            f"{ship_name}/{id_num}"
        )
        return self.__rcra_request("GET", endpoint)

    def get_pack_groups_sn_id(self, ship_name: str, id_num: str) -> RcrainfoResponse[List[str]]:
        """
        Retrieve DOT Packing Groups by DOT Proper Shipping name and ID Number

        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/"
            f"{ship_name}/{id_num}"
        )
        return self.__rcra_request("GET", endpoint)

    def get_id_by_ship_name(self, ship_name: str) -> RcrainfoResponse[List[str]]:
        """
        Retrieve DOT ID number by DOT Proper Shipping name

        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/id-numbers-by-shipping-name/{ship_name}"
        return self.__rcra_request("GET", endpoint)

    def get_ship_name_by_id(self, id_num: str) -> RcrainfoResponse[List[str]]:
        """
        Retrieve DOT Proper Shipping name by DOT ID number

        Args:
            id_num (str): DOT ID number
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/lookup/proper-shipping-names-by-id-number/{id_num}"
        )
        return self.__rcra_request("GET", endpoint)

    def get_mtn_suffix(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """Retrieve Allowable Manifest Tracking Number (MTN) Suffixes"""
        endpoint = f"{self.base_url}v1/emanifest/lookup/printed-tracking-number-suffixes"
        return self.__rcra_request("GET", endpoint)

    def get_mtn_suffix_all(self) -> RcrainfoResponse:
        """
        Retrieve ALL Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with all allowable MTN suffixes
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/printed-tracking-number-suffixes-ALL"
        return self.__rcra_request("GET", endpoint)

    def get_container_types(self) -> RcrainfoResponse:
        """Retrieve Container Types"""
        endpoint = f"{self.base_url}v1/emanifest/lookup/container-types"
        return self.__rcra_request("GET", endpoint)

    def get_quantity_uom(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """
        Retrieve Quantity Units of Measure (UOM)
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/quantity-uom"
        return self.__rcra_request("GET", endpoint)

    def get_load_types(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """Retrieve PCB Load Types"""
        endpoint = f"{self.base_url}v1/emanifest/lookup/load-types"
        return self.__rcra_request("GET", endpoint)

    def get_shipping_names(self) -> RcrainfoResponse[List[str]]:
        """
        Retrieve DOT Proper Shipping Names

        Returns:
            dict: object with DOT Proper Shipping names
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/proper-shipping-names"
        return self.__rcra_request("GET", endpoint)

    def get_id_numbers(self) -> RcrainfoResponse[List[str]]:
        """Retrieve DOT Shipping ID numbers"""
        endpoint = f"{self.base_url}v1/emanifest/lookup/id-numbers"
        return self.__rcra_request("GET", endpoint)

    def get_density_uom(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """Retrieve Density Units of Measure (UOM)"""
        endpoint = f"{self.base_url}v1/lookup/density-uom"
        return self.__rcra_request("GET", endpoint)

    def get_form_codes(self) -> RcrainfoResponse[list[RcraCodeDescription]]:
        """Retrieve Form Codes"""
        endpoint = f"{self.base_url}v1/lookup/form-codes"
        return self.__rcra_request("GET", endpoint)

    def get_source_codes(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """Retrieve Source Codes"""
        endpoint = f"{self.base_url}v1/lookup/source-codes"
        return self.__rcra_request("GET", endpoint)

    def get_state_waste_codes(
        self, state_code: str
    ) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """
        Retrieve State Waste Codes for a given state (besides Texas)

        Args:
            state_code: (str) Two-letter state code (e.g., CA, MA)
        """
        endpoint = f"{self.base_url}v1/lookup/state-waste-codes/{state_code}"
        return self.__rcra_request("GET", endpoint)

    def get_fed_waste_codes(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """Retrieve Federal Waste Codes"""
        endpoint = f"{self.base_url}v1/lookup/federal-waste-codes"
        return self.__rcra_request("GET", endpoint)

    def get_man_method_codes(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """Retrieve Management Method Codes"""
        endpoint = f"{self.base_url}v1/lookup/management-method-codes"
        return self.__rcra_request("GET", endpoint)

    def get_waste_min_codes(self) -> RcrainfoResponse[List[RcraCodeDescription]]:
        """Retrieve Waste Minimization Codes"""
        endpoint = f"{self.base_url}v1/lookup/waste-minimization-codes"
        return self.__rcra_request("GET", endpoint)

    def get_entry_ports(self) -> RcrainfoResponse[List[PortOfEntry]]:
        """Retrieve Ports of Entry"""
        endpoint = f"{self.base_url}v1/lookup/ports-of-entry"
        return self.__rcra_request("GET", endpoint)

    def check_site_exists(self, site_id: str) -> RcrainfoResponse[SiteExistsResponse]:
        """
        Check if provided Site ID exists

        Args:
            site_id (str): EPA site ID
        """
        endpoint = f"{self.base_url}v1/site-exists/{site_id}"
        return self.__rcra_request("GET", endpoint)

    def search_sites(self, **kwargs: Unpack[SiteSearchArgs]) -> RcrainfoResponse[List[RcraSite]]:
        """Retrieve sites based on some or all of the provided criteria"""
        endpoint = f"{self.base_url}v1/site-search"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def search_users(
        self, **kwargs: Unpack[UserSearchArgs]
    ) -> RcrainfoResponse[UserSearchResponse]:
        """
        Search for users by user ID and site.
        Only users of sites accessible to the API keyholder will be visible
        """
        endpoint = f"{self.base_url}v1/user/user-search"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_billing_history(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve billing history for a given billing account ID

        Keyword Args:
            billing_account (str): EPA Site ID
            start_month_year (date): First bill to be included (MM/YYYY format)
            end_month_year (date): Final bill to be included (MM/YYYY format)

        Returns:
            dict: object containing billing history for the specified site and period
        """
        endpoint = f"{self.base_url}v1/emanifest/billing/bill-history"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_bill(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve bill information for a given bill ID and account ID

        Keyword Args:
            billId (str): Bill ID
            billingAccount (str): EPA Site ID
            monthYear (date): Billing month (as MM/YYYY). Optional if billId is provided

        Returns:
            dict: object containing bill information for the specified ID and account
        """
        endpoint = f"{self.base_url}v1/emanifest/billing/bill"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def search_bill(self, **kwargs: Unpack[SearchBillArgs]) -> RcrainfoResponse:
        """Search and retrieve bills using all or some of the provided criteria"""
        endpoint = f"{self.base_url}v1/emanifest/billing/bill-search"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_manifest_attachments(self, mtn: str, reg: bool = False) -> RcrainfoResponse[Manifest]:
        """
        Retrieve manifest data (JSON) and attachments

        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files (such as scans or electronic copies)
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/manifest/{mtn}/attachments"
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest/{mtn}/attachments"
        resp = self.__rcra_request(
            "GET", endpoint, headers={"Accept": "multipart/mixed"}, stream=True
        )
        if resp.response:
            resp.decode()
        return resp

    def search_mtn(
        self, reg: bool = False, **kwargs: Unpack[MtnSearchArgs]
    ) -> RcrainfoResponse[List[str]]:
        """
        Retrieve manifest tracking numbers based on all or some of provided search criteria

        Returns:
            list: list of manifest tracking numbers
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/search"
        else:
            endpoint = f"{self.base_url}v1/emanifest/search"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_correction(self, mtn: str, reg: bool = False) -> RcrainfoResponse[Manifest]:
        """
        Retrieve manifest correction version details by manifest tracking number (MTN)

        Returns:
            dict: object containing correction details for given MTN
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/manifest/correction-details/{mtn}"
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest/correction-details/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def get_correction_version(
        self, reg: bool = False, **kwargs: Unpack[CorrectionVersionSearchArgs]
    ) -> RcrainfoResponse[Manifest]:
        """
        Retrieve details of manifest correction version based the provided search criteria

        Returns:
            dict: object containing correction details
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/manifest/correction-version"
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest/correction-version"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_correction_attachments(self, **kwargs) -> RcrainfoResponse[Manifest]:
        """
        Retrieve corrected manifests attachment by search criteria.
        See also **get_correction** and **get_correction_version**


        Keyword Args:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted)
            versionNumber (str): Manifest version number

        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional
            manifest information (such as scans or copies) for the given MTN
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/correction-version/attachments"
        resp = self.__rcra_request("POST", endpoint, **kwargs)
        if resp.response:
            resp.decode()
        return resp

    def get_site_mtn(self, site_id: str, reg: bool = False) -> RcrainfoResponse[List[str]]:
        """Retrieve manifest tracking numbers for a given Site ID"""
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/manifest-tracking-numbers/{site_id}"
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest-tracking-numbers/{site_id}"
        return self.__rcra_request("GET", endpoint)

    def get_manifest(self, mtn: str, reg: bool = False) -> RcrainfoResponse[Manifest]:
        """Retrieve e-Manifest details by Manifest Tracking Number (MTN)"""
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/manifest/{mtn}"
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def get_sites(
        self, state_code: str, site_type: str, reg: bool = False
    ) -> RcrainfoResponse[List[str]]:
        """
        Retrieve site ids for provided criteria

        Args:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
            reg (bool): use endpoint for regulators, defaults to False
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/site-ids/{state_code}/{site_type}"
        else:
            endpoint = f"{self.base_url}v1/emanifest/site-ids/{state_code}/{site_type}"
        return self.__rcra_request("GET", endpoint)

    def correct_manifest(
        self, manifest_json: dict, zip_file: bytes | None = None
    ) -> RcrainfoResponse[ManifestOperationResponse]:
        """
        Correct Manifest by providing e-Manifest JSON and optional Zip attachment

        Args:
            manifest_json (dict): Dictionary containing manifest details
            zip_file (bytearray): bytes of zip file containing manifest attachments. Optional

        Returns:
            dict: message of success or failure
        """
        if zip_file:
            multipart = self.__encode_manifest(manifest_json, zip_file)
        else:
            multipart = self.__encode_manifest(manifest_json)
        endpoint = f"{self.base_url}v1/emanifest/manifest/correct"
        return self.__rcra_request("PUT", endpoint, multipart=multipart)

    def revert_manifest(self, mtn: str) -> RcrainfoResponse[CorrectionRevertResponse]:
        """
        Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version

        Returns:
            dict: object containing confirmation of correction
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/revert/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def patch_update_manifest(
        self, mtn: str, data: dict
    ) -> RcrainfoResponse[ManifestOperationResponse]:
        """
        Update a portion of a manifest via the patch process

        Args:
            mtn (str): Manifest tracking number
            data (dict): Partial manifest to be applied to the existing manifest

        Returns:
            dict: message of success or failure
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/patch-update/{mtn}"
        return self.__rcra_request(
            "PATCH", endpoint, headers={"Content-Type": "application/json-patch+json"}, **data
        )

    def patch_correct_manifest(
        self, mtn: str, data: dict
    ) -> RcrainfoResponse[ManifestOperationResponse]:
        """
        Update a portion of a manifest via the patch process

        Args:
            mtn (str): Manifest tracking number
            data (dict): Partial manifest to be applied as a correction

        Returns:
            dict: message of success or failure
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/patch-correct/{mtn}"
        return self.__rcra_request(
            "PATCH", endpoint, headers={"Content-Type": "application/json-patch+json"}, **data
        )

    def update_manifest(
        self, manifest_json: dict, zip_file: bytes | None = None
    ) -> RcrainfoResponse[ManifestOperationResponse]:
        """
        Update Manifest by providing e-Manifest JSON and optional Zip attachment

        Args:
            manifest_json (dict): Dictionary containing manifest details
            zip_file (bytearray): bytes of zip file containing manifest attachments. Optional

        Returns:
            dict: message of success or failure
        """
        if zip_file:
            multipart = self.__encode_manifest(manifest_json, zip_file)
        else:
            multipart = self.__encode_manifest(manifest_json)
        endpoint = f"{self.base_url}v1/emanifest/manifest/update"
        return self.__rcra_request(
            "PUT",
            endpoint,
            headers={
                "Content-Type": multipart.content_type,
                "Accept": "application/json",
            },
            multipart=multipart,
        )

    def delete_manifest(self, mtn: str) -> RcrainfoResponse[ManifestOperationResponse]:
        """
        Delete selected manifest

        Returns:
            dict: message of success or failure
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/delete/{mtn}"
        return self.__rcra_request("DELETE", endpoint)

    def sign_manifest(
        self, **kwargs: Unpack[SignManifestArgs]
    ) -> RcrainfoResponse[ManifestSignatureResponse]:
        """Quicker sign selected manifests"""
        sign_date = kwargs.get("printedSignatureDate", None)
        if not sign_date:
            kwargs["printedSignatureDate"] = datetime.now(timezone.utc).strftime(
                self.__signature_date_fmt
            )
        if isinstance(sign_date, datetime):
            kwargs["printedSignatureDate"] = sign_date.strftime(self.__signature_date_fmt)
        endpoint = f"{self.base_url}v1/emanifest/manifest/quicker-sign"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_available_manifests(self, mtn: str) -> RcrainfoResponse:
        """
        Returns signature-related information about manifest and respective sites

        Returns:
            dict: object containing manifest signature details
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/available-to-sign/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def save_manifest(
        self, manifest_json: dict, zip_file: bytes | None = None
    ) -> RcrainfoResponse[ManifestOperationResponse]:
        """
        Save Manifest by providing e-Manifest JSON and optional Zip attachment

        Args:
            manifest_json (dict): Dictionary containing manifest details
            zip_file (bytearray): bytes of zip file containing manifest attachments. Optional

        Returns:
            dict: message of success or failure
        """
        if zip_file:
            multipart = self.__encode_manifest(manifest_json, zip_file)
        else:
            multipart = self.__encode_manifest(manifest_json)
        endpoint = f"{self.base_url}v1/emanifest/manifest/save"
        return self.__rcra_request(
            "POST",
            endpoint,
            headers={
                "Content-Type": multipart.content_type,
                "Accept": "application/json",
            },
            multipart=multipart,
        )

    def check_mtn_exists(self, mtn: str) -> RcrainfoResponse[ManifestExistsResponse]:
        """Check if Manifest Tracking Number (MTN) exists and return basic details"""
        endpoint = f"{self.base_url}v1/emanifest/manifest/mtn-exists/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def get_ui_link(self, **kwargs: Unpack[UILinkArgs]) -> RcrainfoResponse:
        """
        Generate link to the user interface (UI) of the RCRAInfo e-Manifest module

        Returns:
            dict: object containing link to UI
        """
        endpoint = f"{self.base_url}v1/links/emanifest"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_cme_lookup(
        self, activity_location: str, agency_code: AgencyCode, nrr_flag: bool = True
    ) -> RcrainfoResponse:
        """
        Retrieve all lookups for specific activity location and agency code, including staff,
        focus area and sub-organization. For use by Regulator users only.

        Args:
            activity_location (str): Two-letter US postal state code
            agency_code (AgencyCode): One-letter code.
            nrr_flag (boolean): True/False if Non-Financial Record Review

        Returns:
            dict: object containing CME lookups
        """
        endpoint = (
            f"{self.base_url}v1/state/cme/evaluation/lookups/{activity_location}/{agency_code}/"
            f"{str(nrr_flag)}"
        )
        return self.__rcra_request("GET", endpoint)

    def get_cme_indicators(self):
        """
        Retrieve all evaluation indicators. For use by Regulator users only.

        Returns:
            dict: object containing all evaluation indicators
        """
        endpoint = f"{self.base_url}v1/state/cme/evaluation/evaluation-indicators"
        return self.__rcra_request("GET", endpoint)

    def get_cme_types(self) -> RcrainfoResponse:
        """
        Retrieve all evaluation types. For use by Regulator users only.

        Returns:
            dict: object containing all evaluation types
        """
        endpoint = f"{self.base_url}v1/state/cme/evaluation/evaluation-types"
        return self.__rcra_request("GET", endpoint)

    def get_handler(self, handler_id: str, details: bool = False) -> RcrainfoResponse:
        """
        Retrieve a list of handler source records (and optional details) for a specific handler ID
        This endpoint is restricted to regulators.

        Args:
            handler_id (str): EPA Site ID number
            details (boolean): True/false to request additional details. Optional; defaults False

        Returns:
            dict: object containing handler source records (and optional details)
        """
        endpoint = f"{self.base_url}v1/state/handler/sources/{handler_id}/{str(details)}"
        return self.__rcra_request("GET", endpoint)


def _parse_url(base_url: str | None) -> str:
    """emanifest-py internal helper function"""
    urls = {"PROD": RCRAINFO_PROD, "PREPROD": RCRAINFO_PREPROD}
    if base_url is None:
        return urls["PREPROD"]
    if "https" not in base_url:
        if base_url.upper() in urls:
            return urls[base_url.upper()]
        else:
            return urls["PREPROD"]
    else:
        return base_url


BaseUrls = Literal["prod", "preprod"]


def new_client(
    base_url: BaseUrls | str | None = None,
    api_id: str | None = None,
    api_key: str | None = None,
    auto_renew: bool = False,
) -> RcrainfoClient:
    """
    Create a new RCRAInfo client instance

    Args:
        base_url (str): Base URL of the RCRAInfo API. Defaults to 'PREPROD'
        api_id (str): RCRAInfo API ID
        api_key (str): RCRAInfo API key
        auto_renew: (bool): Automatically renew API token when expired. Defaults to False

    Returns:
        RcrainfoClient: RCRAInfo client instance
    """
    if base_url is None:
        raise ValueError("base_url is required")
    return RcrainfoClient(base_url, api_id=api_id, api_key=api_key, auto_renew=auto_renew)
