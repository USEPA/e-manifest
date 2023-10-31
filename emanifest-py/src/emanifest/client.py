"""
e-Manifest library for using the e-Manifest API
see https://github.com/USEPA/e-manifest
"""
import io
import json
import zipfile
from datetime import datetime, timezone

from requests import Request, Response, Session
from requests_toolbelt.multipart import decoder, encoder

RCRAINFO_PROD = "https://rcrainfo.epa.gov/rcrainfoprod/rest/api/"
RCRAINFO_PREPROD = "https://rcrainfopreprod.epa.gov/rcrainfo/rest/api/"


class RcrainfoResponse:
    """
    RcrainfoResponse wraps around the requests library's Response object.
    The complete Response object can be accessed as self.response

    Attributes:
        response (Response) the request library response object.
    """

    def __init__(self, response: Response):
        self.response = response
        self._multipart_json = None
        self._multipart_zip = None

    def json(self):
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
    __expiration_fmt = "%Y-%m-%dT%H:%M:%S.%f%z"
    __default_headers = {"Accept": "application/json"}
    __default_timeout = 10

    def __init__(
        self, base_url: str, *, api_id=None, api_key=None, timeout=10, auto_renew=True
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.__token = None
        self.__token_expiration_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.__api_key = api_key
        self.__api_id = api_id
        self.headers.update(self.__default_headers)
        self.auto_renew = auto_renew

    @property
    def base_url(self):
        """RCRAInfo base URL, either for Production ('prod') or Preproduction ('preprod') for testing."""
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
            self.__token_expiration_utc = datetime.utcnow().replace(tzinfo=timezone.utc)

    @property
    def token(self):
        """Session token from Rcrainfo. Read Only."""
        return self.__token

    @property
    def is_authenticated(self) -> bool:
        """Returns True if the RcrainfoClient token exists and has not expired."""
        try:
            if (
                self.token_expiration > datetime.utcnow().replace(tzinfo=timezone.utc)
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
        return RcrainfoResponse(
            self.send(prepared_req, timeout=self.timeout, stream=stream)
        )

    def __get_token(self):
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
        zip_bytes: bytes = None,
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

    # The following methods are exposed so users can hook into our client and customize its behavior
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
        elif self.__api_id is None and api_id is None:
            #  pass an empty string so, if user's fail to provide a string, it will not try to use None as
            #  the API credential in the URL
            return ""

    def retrieve_key(self, api_key=None) -> str:
        """
        Getter method used internally to retrieve the desired RCRAInfo API key. Can be overridden
        to automatically support retrieving an API Key from an external location.

        Args:
            api_key:

        Returns:
            string of the user's RCRAInfo API Key
        """
        if api_key:
            return api_key
        elif self.__api_key:
            return self.__api_key
        elif self.__api_key is None and api_key is None:
            return ""

    # Below this line are the high level methods to request RCRAInfo/e-Manifest
    def authenticate(self, api_id=None, api_key=None) -> None:
        """
        Authenticate user's RCRAInfo API ID and Key to generate token for use by other functions

        Args:
            api_id (str): API ID of RCRAInfo User with Site Manager level permission.
            api_key (str): User's RCRAInfo API key. Generated alongside the api_id in RCRAInfo

        Returns:
            token (client): Authentication token for use by other emanifest functions. Expires after 20 minutes
        """
        # if api credentials are passed, set the client's attributes
        if api_id is not None:
            self.__api_id = str(api_id)
        if api_key is not None:
            self.__api_key = str(api_key)
        self.__get_token()

    def get_site(self, epa_id) -> RcrainfoResponse:
        """
        Retrieve site details for a given Site ID

        Args:
            epa_id (str): EPA site ID

        Returns:
            dict: object with EPA ID site details
        """
        endpoint = f"{self.base_url}v1/site-details/{epa_id}"
        return self.__rcra_request("GET", endpoint)

    def get_hazard_classes(self) -> RcrainfoResponse:
        """
        Retrieve all DOT Hazard Classes

        Returns:
            dict: object with DOT hazard classes
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/hazard-classes"
        return self.__rcra_request("GET", endpoint)

    def get_packing_groups(self) -> RcrainfoResponse:
        """
        Retrieve all DOT Packing Groups

        Returns:
            dict: object with DOT packing groups
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/packing-groups"
        return self.__rcra_request("GET", endpoint)

    def get_haz_class_sn_id(self, ship_name, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number

        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number

        Returns:
            dict: object with DOT hazard classes
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/"
            f"{ship_name}/{id_num}"
        )
        return self.__rcra_request("GET", endpoint)

    def get_pack_groups_sn_id(self, ship_name, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Packing Groups by DOT Proper Shipping name and ID Number

        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number

        Returns:
            dict: object with DOT packing groups
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/"
            f"{ship_name}/{id_num}"
        )
        return self.__rcra_request("GET", endpoint)

    def get_id_by_ship_name(self, ship_name) -> RcrainfoResponse:
        """
        Retrieve DOT ID number by DOT Proper Shipping name

        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)

        Returns:
            dict: object with DOT ID number
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/id-numbers-by-shipping-name/{ship_name}"
        return self.__rcra_request("GET", endpoint)

    def get_ship_name_by_id(self, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Proper Shipping name by DOT ID number

        Args:
            id_num (str): DOT ID number

        Returns:
            dict: object with DOT Proper Shipping name
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/proper-shipping-names-by-id-number/{id_num}"
        return self.__rcra_request("GET", endpoint)

    def get_mtn_suffix(self) -> RcrainfoResponse:
        """
        Retrieve Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with allowable MTN suffixes
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/lookup/printed-tracking-number-suffixes"
        )
        return self.__rcra_request("GET", endpoint)

    def get_mtn_suffix_all(self) -> RcrainfoResponse:
        """
        Retrieve ALL Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with all allowable MTN suffixes
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/lookup/printed-tracking-number-suffixes-ALL"
        )
        return self.__rcra_request("GET", endpoint)

    def get_container_types(self) -> RcrainfoResponse:
        """
        Retrieve Container Types

        Returns:
            dict: object with container types
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/container-types"
        return self.__rcra_request("GET", endpoint)

    def get_quantity_uom(self) -> RcrainfoResponse:
        """
        Retrieve Quantity Units of Measure (UOM)

        Returns:
            dict: object with quantity UOM
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/quantity-uom"
        return self.__rcra_request("GET", endpoint)

    def get_load_types(self) -> RcrainfoResponse:
        """
        Retrieve PCB Load Types

        Returns:
            dict: object with load types
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/load-types"
        return self.__rcra_request("GET", endpoint)

    def get_shipping_names(self) -> RcrainfoResponse:
        """
        Retrieve DOT Proper Shipping Names

        Returns:
            dict: object with DOT Proper Shipping names
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/proper-shipping-names"
        return self.__rcra_request("GET", endpoint)

    def get_id_numbers(self) -> RcrainfoResponse:
        """
        Retrieve DOT Shipping ID numbers

        Returns:
            dict: object with DOT Shipping ID numbers
        """
        endpoint = f"{self.base_url}v1/emanifest/lookup/id-numbers"
        return self.__rcra_request("GET", endpoint)

    def get_density_uom(self) -> RcrainfoResponse:
        """
        Retrieve Density Units of Measure (UOM)

        Returns:
            dict: object with density UOM
        """
        endpoint = f"{self.base_url}v1/lookup/density-uom"
        return self.__rcra_request("GET", endpoint)

    def get_form_codes(self) -> RcrainfoResponse:
        """
        Retrieve Form Codes

        Returns:
            dict: object with form codes
        """
        endpoint = f"{self.base_url}v1/lookup/form-codes"
        return self.__rcra_request("GET", endpoint)

    def get_source_codes(self) -> RcrainfoResponse:
        """
        Retrieve Source Codes

        Returns:
            dict: object with source codes
        """
        endpoint = f"{self.base_url}v1/lookup/source-codes"
        return self.__rcra_request("GET", endpoint)

    def get_state_waste_codes(self, state_code: str) -> RcrainfoResponse:
        """
        Retrieve State Waste Codes for a given state (besides Texas)

        Args:
            state_code: (str) Two-letter state code (e.g., CA, MA)

        Returns:
            dict: object with state waste codes
        """
        endpoint = f"{self.base_url}v1/lookup/state-waste-codes/{state_code}"
        return self.__rcra_request("GET", endpoint)

    def get_fed_waste_codes(self) -> RcrainfoResponse:
        """
        Retrieve Federal Waste Codes

        Returns:
            dict: object with federal waste codes
        """
        endpoint = f"{self.base_url}v1/lookup/federal-waste-codes"
        return self.__rcra_request("GET", endpoint)

    def get_man_method_codes(self) -> RcrainfoResponse:
        """
        Retrieve Management Method Codes

        Returns:
            dict: object with management method codes
        """
        endpoint = f"{self.base_url}v1/lookup/management-method-codes"
        return self.__rcra_request("GET", endpoint)

    def get_waste_min_codes(self) -> RcrainfoResponse:
        """
        Retrieve Waste Minimization Codes

        Returns:
            dict: object with waste minimization codes
        """
        endpoint = f"{self.base_url}v1/lookup/waste-minimization-codes"
        return self.__rcra_request("GET", endpoint)

    def get_entry_ports(self) -> RcrainfoResponse:
        """
        Retrieve Ports of Entry

        Returns:
            dict: object with ports of entry
        """
        endpoint = f"{self.base_url}v1/lookup/ports-of-entry"
        return self.__rcra_request("GET", endpoint)

    def check_site_exists(self, site_id: str) -> RcrainfoResponse:
        """
        Check if provided Site ID exists

        Args:
            site_id (str): EPA site ID

        Returns:
            result (boolean): true/false confirmation if site exists
        """
        endpoint = f"{self.base_url}v1/site-exists/{site_id}"
        return self.__rcra_request("GET", endpoint)

    def search_sites(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve sites based on some or all of the provided criteria


        Keyword Args:
            epaSiteId (str): EPA site ID
            name (str): Site name (e.g. The White House)
            streetNumber (str): Street number (e.g. 1600)
            address1 (str): Street name (e.g. Pennsylvania Avenue NW)
            city (str): City name (e.g. Washington)
            state (str): US two-letter postal state abbreviation (e.g. DC)
            zip (str): US zip code (e.g. 20500)
            siteType (str): Case-sensitive: Generator, Tsdf, Transporter, or Broker
            pageNumber (number): must be greater than 0

        Returns:
            dict: object containing list of sites matching criteria and details about each site
        """
        endpoint = f"{self.base_url}v1/site-search"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def search_users(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve users based on some or all of the provided criteria. Only users of sites accessible
        to the API keyholder will be visible

        Keyword Args:
            userId (str) : A RCRAInfo username
            siteIds (array of strings) : One or more EPA site IDs
            pageNumber (number): must be greater than 0

        Returns:
            dict: object containing list of users matching criteria and details about each user
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

    def search_bill(self, **kwargs) -> RcrainfoResponse:
        """
        Search and retrieve bills using all or some of the provided criteria

        Keyword Args:
            billingAccount (str): EPA Site ID
            billStatus (str): Active, Paid, Unpaid, ReadyForPayment, Credit, InProgress, SendToCollections, ZeroBalance.
            startDate(date): Beginning of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            endDate (date): End of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            amountChanged (boolean): True or false
            pageNumber (number): Must be greater than 0

        Returns:
            dict: object with bills matching criteria
        """
        endpoint = f"{self.base_url}v1/emanifest/billing/bill-search"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_manifest_attachments(self, mtn: str, reg: bool = False) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)

        Args:
            mtn (str): Manifest tracking number
            reg (bool): use endpoint for regulators, defaults to False

        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans
            or electronic copies) for the given MTN
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

    def search_mtn(self, reg: bool = False, **kwargs) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers based on all or some of provided search criteria

        Args:
            reg (bool): Use the Regulator endpoint, defaults to False

        Keyword Args:
            stateCode (str): Two-letter US postal state code
            siteId (str): EPA Site ID
            status (str): Pending, Scheduled, InTransit, Received, ReadyForSignature, Signed, SignedComplete,
            UnderCorrection, Corrected. Case-sensitive
            dateType (str): CertifiedDate, ReceivedDate, ShippedDate, UpdatedDate. Case-sensitive
            siteType (str): Generator, Tsdf, Transporter, RejectionInfo_AlternateTsdf. Case-sensitive
            startDate (date): Start date for search period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            endDate (date): End date for search period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)

        Returns:
            dict: object containing manifest tracking numbers matching criteria
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/search"
        else:
            endpoint = f"{self.base_url}v1/emanifest/search"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_correction(self, mtn: str, reg: bool = False) -> RcrainfoResponse:
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)

        Args:
            mtn (str): Manifest tracking number
            reg (bool): use endpoint for regulators, defaults to False

        Returns:
            dict: object containing correction details for given MTN
        """
        if reg:
            endpoint = (
                f"{self.base_url}v1/state/emanifest/manifest/correction-details/{mtn}"
            )
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest/correction-details/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def get_correction_version(self, reg: bool = False, **kwargs) -> RcrainfoResponse:
        """
        Retrieve details of manifest correction version based on all or some of the provided search criteria

        Keyword Args:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest version number

        Returns:
            dict: object containing correction details
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/manifest/correction-version"
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest/correction-version"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_correction_attachments(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve attachments of corrected manifests based all or some of the provided search criteria.
        See also **get_correction** and **get_correction_version**


        Keyword Args:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest version number

        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional
            manifest information (such as scans or
            electronic copies) for the given MTN
            print: message of success or failure
        """
        endpoint = (
            f"{self.base_url}v1/emanifest/manifest/correction-version/attachments"
        )
        resp = self.__rcra_request("POST", endpoint, **kwargs)
        if resp.response:
            resp.decode()
        return resp

    def get_site_mtn(self, site_id: str, reg: bool = False) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers for a given Site ID

        Args:
            site_id (str): EPA Site ID
            reg (bool): use endpoint for regulators, defaults to False

        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        if reg:
            endpoint = (
                f"{self.base_url}v1/state/emanifest/manifest-tracking-numbers/{site_id}"
            )
        else:
            endpoint = (
                f"{self.base_url}v1/emanifest/manifest-tracking-numbers/{site_id}"
            )
        return self.__rcra_request("GET", endpoint)

    def get_manifest(self, mtn: str, reg: bool = False) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)

        Args:
            mtn (str): Manifest tracking number
            reg (bool): use endpoint for regulators, defaults to False

        Returns:
            dict: object containing e-Manifest details
        """
        if reg:
            endpoint = f"{self.base_url}v1/state/emanifest/manifest/{mtn}"
        else:
            endpoint = f"{self.base_url}v1/emanifest/manifest/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def get_sites(
        self, state_code: str, site_type: str, reg: bool = False
    ) -> RcrainfoResponse:
        """
        Retrieve site ids for provided criteria

        Args:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
            reg (bool): use endpoint for regulators, defaults to False

        Returns:
            dict: object containing site ID numbers
        """
        if reg:
            endpoint = (
                f"{self.base_url}v1/state/emanifest/site-ids/{state_code}/{site_type}"
            )
        else:
            endpoint = f"{self.base_url}v1/emanifest/site-ids/{state_code}/{site_type}"
        return self.__rcra_request("GET", endpoint)

    def correct_manifest(
        self, manifest_json: dict, zip_file: bytes = None
    ) -> RcrainfoResponse:
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

    def revert_manifest(self, mtn: str) -> RcrainfoResponse:
        """
        Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version

        Args:
            mtn (str): Manifest tracking number

        Returns:
            dict: object containing confirmation of correction
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/revert/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def patch_update_manifest(self, mtn: str, body: dict) -> RcrainfoResponse:
        """
        Update a portion of a manifest via the patch process

        Args:
            mtn (str): Manifest tracking number
            body (dict): Dictionary containing manifest portion details

        Returns:
            dict: message of success or failure
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/patch-update/{mtn}"
        return self.__rcra_request("PATCH", endpoint)

    def patch_correct_manifest(self, mtn: str, body: dict) -> RcrainfoResponse:
        """
        Update a portion of a manifest via the patch process

        Args:
            mtn (str): Manifest tracking number
            body (dict): Dictionary containing manifest portion details

        Returns:
            dict: message of success or failure
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/patch-correct/{mtn}"
        return self.__rcra_request("PATCH", endpoint)

    def update_manifest(
        self, manifest_json: dict, zip_file: bytes = None
    ) -> RcrainfoResponse:
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

    def delete_manifest(self, mtn: str) -> RcrainfoResponse:
        """
        Delete selected manifest

        Args:
            mtn (str): Manifest tracking number

        Returns:
            dict: message of success or failure
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/delete/{mtn}"
        return self.__rcra_request("DELETE", endpoint)

    def sign_manifest(self, **kwargs) -> RcrainfoResponse:
        """
        Quicker sign selected manifests

        Keyword Args:
            manifestTrackingNumbers (array) : An array of manifest tracking numbers to sign
            siteId (str) : The EPA ID for the site that signs
            siteType (str) : The site on the manifest that is signing (Generator, Tsdf, Transporter, RejectionInfo_AlternateTsdf). Case-sensitive
            printedSignatureName (str) : The name of the person who signed the manifest
            printedSignatureDate (date) : The date the person signed the manifest
            transporterOrder (int) : If the site is a transporter, the order of that transporter on the manifest

        Returns:
            dict: message of success or failure
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/quicker-sign"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def save_manifest(
        self, manifest_json: dict, zip_file: bytes = None
    ) -> RcrainfoResponse:
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

    def check_mtn_exists(self, mtn: str) -> RcrainfoResponse:
        """
        Check if Manifest Tracking Number (MTN) exists and return basic details

        Args:
            mtn (str): Manifest tracking number

        Returns:
            dict: object containing MTN details and confirmation if site exists
        """
        endpoint = f"{self.base_url}v1/emanifest/manifest/mtn-exists/{mtn}"
        return self.__rcra_request("GET", endpoint)

    def get_ui_link(self, **kwargs) -> RcrainfoResponse:
        """
        Generate link to the user interface (UI) of the RCRAInfo e-Manifest module

        Keyword Args:
            page (str): Dashboard, BulkSign, BulkQuickSign, Edit, View, Sign. Case-sensitive
            epaSiteId (Str): EPA Site ID
            manifestTrackingNumber (str): Manifest tracking number (optional)
            filter (list): List of MTNs (optional)

        Returns:
            dict: object containing link to UI
        """
        endpoint = f"{self.base_url}v1/links/emanifest"
        return self.__rcra_request("POST", endpoint, **kwargs)

    def get_cme_lookup(
        self, activity_location: str, agency_code: str, nrr_flag: bool = True
    ) -> RcrainfoResponse:
        """
        Retrieve all lookups for specific activity location and agency code, including staff,
        focus area and sub-organization. For use by Regulator users only.

        Args:
            activity_location (str): Two-letter US postal state code
            agency_code (str): One-letter code. B (State Contractor/Grantee),
                                                C (EPA Contractor/Grantee),
                                                E (EPA),
                                                L (Local),
                                                N (Native American),
                                                S (State),
                                                T (State-Initiated Oversight/Observation/Training Actions),
                                                X (EPA-Initiated Oversight/Observation/Training Actions),
                                                J (Joint State),
                                                P (Joint EPA)
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
            details (boolean): True/false to request additional details. Optional; defaults to False

        Returns:
            dict: object containing handler source records (and optional details)
        """
        endpoint = f"v1/state/handler/sources/{handler_id}/{str(details)}"
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


def new_client(
    base_url: str = None,
    api_id: str = None,
    api_key: str = None,
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
    return RcrainfoClient(
        base_url, api_id=api_id, api_key=api_key, auto_renew=auto_renew
    )
