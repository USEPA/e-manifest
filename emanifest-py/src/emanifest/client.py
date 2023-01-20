"""
e-Manifest library for using the e-Manifest API
see https://github.com/USEPA/e-manifest
"""
import io
import json
import logging
import os
import zipfile
from datetime import datetime, timedelta

import requests
from requests_toolbelt.multipart import decoder, encoder


class RcrainfoResponse:

    def __init__(self, response: requests.Response):
        self.response = response
        self.zip = None
        self._multipart_json = None

    @property
    def json(self):
        if self._multipart_json:
            return self._multipart_json
        else:
            return self.response.json()

    @property
    def ok(self):
        return self.response.ok

    def __str__(self):
        return f'RcrainfoResponse: status {self.response.status_code}'

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        """returns True if < 400"""
        return self.ok

    def decode(self):
        multipart_data = decoder.MultipartDecoder.from_response(self.response)
        for part in multipart_data.parts:
            if part.headers[b'Content-Type'] == b'application/json':
                self._multipart_json = part.text
            else:
                zip_contents = zipfile.ZipFile(io.BytesIO(part.content))
                self.zip = zip_contents


# noinspection PyIncorrectDocstring
class RcrainfoClient:
    def __init__(self, base_url: str, *, api_id=None, api_key=None, timeout=10) -> None:
        self.base_url = _parse_url(base_url)
        self.__api_key = api_key
        self.__api_id = api_id
        self.timeout = timeout
        self.token = None
        self._token_expiration = None

    @property
    def token_expiration(self) -> datetime:
        """
        The Token's expiration datetime. If not present will return datetime.now()
        """
        if isinstance(self._token_expiration, datetime):
            return self._token_expiration
        else:
            # we don't want to return None, but just incase people decide to use the >= operator
            return datetime.now() - timedelta(seconds=30)

    @property
    def authenticated(self) -> bool:
        try:
            if self._token_expiration < datetime.now():
                return True
            else:
                return False
        except TypeError:
            return False

    def __str__(self) -> str:
        return f'RcrainfoClient: base URL {self.base_url}'

    def __repr__(self) -> str:
        return self.__str__()

    def __rcra_get(self, endpoint) -> RcrainfoResponse:
        return RcrainfoResponse(requests.get(endpoint, timeout=self.timeout,
                                             headers={'Accept': 'application/json',
                                                      'Authorization': f'Bearer {self.token}'}))

    def __rcra_post(self, endpoint, **kwargs) -> RcrainfoResponse:
        return RcrainfoResponse(requests.post(endpoint, timeout=self.timeout,
                                              headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                                       'Authorization': f'Bearer {self.token}'},
                                              data=json.dumps(dict(**kwargs))))

    def __rcra_delete(self, endpoint) -> RcrainfoResponse:
        return RcrainfoResponse(requests.delete(endpoint, timeout=self.timeout,
                                                headers={'Accept': 'application/json',
                                                         'Authorization': f'Bearer {self.token}'}))

    def __rcra_put(self, endpoint, m) -> RcrainfoResponse:
        return RcrainfoResponse(requests.put(endpoint, timeout=self.timeout,
                                             headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                                      'Authorization': f'Bearer {self.token}'}, data=m))

    def __get_token(self):
        self.__api_id = self.retrieve_id()
        self.__api_key = self.retrieve_key()
        auth_url = f'{self.base_url}api/v1/auth/{self.__api_id}/{self.__api_key}'
        resp = requests.get(auth_url, timeout=self.timeout)
        if resp.ok:
            self.token = resp.json()['token']
            # see datetime docs https://docs.python.org/3.7/library/datetime.html#strftime-strptime-behavior
            expire_format = '%Y-%m-%dT%H:%M:%S.%f%z'
            self._token_expiration = datetime.strptime(resp.json()['expiration'], expire_format)

    def retrieve_id(self, api_id=None) -> str:
        if api_id:
            return api_id
        elif self.__api_id:
            return self.__api_id
        elif self.__api_id is None and api_id is None:
            return ''

    def retrieve_key(self, api_key=None) -> str:
        if api_key:
            return api_key
        elif self.__api_key:
            return self.__api_key
        elif self.__api_key is None and api_key is None:
            return ''

    # Below this line starts the classes methods to interact with  RCRAInfo/e-Manifest
    def auth(self, api_id=None, api_key=None) -> None:
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
            self.__api_id = api_id
        if api_key is not None:
            self.__api_key = api_key

        if None not in (self.__api_key, self.__api_id):
            self.__get_token()

    def get_site_details(self, epa_id) -> RcrainfoResponse:
        """
        Retrieve site details for a given Site ID
        
        Args:
            epa_id (str): EPA site ID
        
        Returns:
            dict: object with EPA ID site details
        """
        endpoint = f'{self.base_url}/api/v1/site-details/{epa_id}'
        return self.__rcra_get(endpoint)

    def get_hazard_classes(self) -> RcrainfoResponse:
        """
        Retrieve all DOT Hazard Classes
        
        Returns:
            dict: object with DOT hazard classes
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/hazard-classes'
        return self.__rcra_get(endpoint)

    def get_packing_groups(self) -> RcrainfoResponse:
        """
        Retrieve all DOT Packing Groups
        
        Returns:
            dict: object with DOT packing groups
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/packing-groups'
        return self.__rcra_get(endpoint)

    def get_haz_class_sn_id(self, ship_name, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number 
        
        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT hazard classes
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/' \
                   f'{ship_name}/{id_num}'
        return self.__rcra_get(endpoint)

    def get_pack_groups_sn_id(self, ship_name, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Packing Groups by DOT Proper Shipping name and ID Number 
        
        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT packing groups
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/' \
                   f'{ship_name}/{id_num}'
        return self.__rcra_get(endpoint)

    def get_id_by_ship_name(self, ship_name) -> RcrainfoResponse:
        """
        Retrieve DOT ID number by DOT Proper Shipping name
        
        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            
        Returns:
            dict: object with DOT ID number
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/id-numbers-by-shipping-name/{ship_name}'
        return self.__rcra_get(endpoint)

    def get_ship_name_by_id(self, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Proper Shipping name by DOT ID number
        
        Args:
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT Proper Shipping name 
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/proper-shipping-names-by-id-number/{id_num}'
        return self.__rcra_get(endpoint)

    def get_mtn_suffix(self) -> RcrainfoResponse:
        """
        Retrieve Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with allowable MTN suffixes
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/printed-tracking-number-suffixes'
        return self.__rcra_get(endpoint)

    def get_mtn_suffix_all(self) -> RcrainfoResponse:
        """
        Retrieve ALL Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with all allowable MTN suffixes
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/printed-tracking-number-suffixes-ALL'
        return self.__rcra_get(endpoint)

    def get_container_types(self) -> RcrainfoResponse:
        """
        Retrieve Container Types

        Returns:
            dict: object with container types
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/container-types'
        return self.__rcra_get(endpoint)

    def get_quantity_uom(self) -> RcrainfoResponse:
        """
        Retrieve Quantity Units of Measure (UOM)

        Returns:
            dict: object with quantity UOM
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/quantity-uom'
        return self.__rcra_get(endpoint)

    def get_load_types(self) -> RcrainfoResponse:
        """
        Retrieve PCB Load Types

        Returns:
            dict: object with load types
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/load-types'
        return self.__rcra_get(endpoint)

    def get_shipping_names(self) -> RcrainfoResponse:
        """
        Retrieve DOT Proper Shipping Names

        Returns:
            dict: object with DOT Proper Shipping names
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/proper-shipping-names'
        return self.__rcra_get(endpoint)

    def get_id_nums(self) -> RcrainfoResponse:
        """
        Retrieve DOT Shipping ID numbers

        Returns:
            dict: object with DOT Shipping ID numbers
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/lookup/id-numbers'
        return self.__rcra_get(endpoint)

    def get_density_uom(self) -> RcrainfoResponse:
        """
        Retrieve Density Units of Measure (UOM)

        Returns:
            dict: object with density UOM
        """
        endpoint = f'{self.base_url}/api/v1/lookup/density-uom'
        return self.__rcra_get(endpoint)

    def get_form_codes(self) -> RcrainfoResponse:
        """
        Retrieve Form Codes

        Returns:
            dict: object with form codes
        """
        endpoint = f'{self.base_url}/api/v1/lookup/form-codes'
        return self.__rcra_get(endpoint)

    def get_source_codes(self) -> RcrainfoResponse:
        """
        Retrieve Source Codes

        Returns:
            dict: object with source codes
        """
        endpoint = f'{self.base_url}/api/v1/lookup/source-codes'
        return self.__rcra_get(endpoint)

    def get_state_waste_codes(self, state_code) -> RcrainfoResponse:
        """
        Retrieve State Waste Codes

        Returns:
            dict: object with state waste codes
        """
        endpoint = f'{self.base_url}/api/v1/lookup/state-waste-codes/{state_code}'
        return self.__rcra_get(endpoint)

    def get_fed_waste_codes(self) -> RcrainfoResponse:
        """
        Retrieve Federal Waste Codes

        Returns:
            dict: object with federal waste codes
        """
        endpoint = f'{self.base_url}/api/v1/lookup/federal-waste-codes'
        return self.__rcra_get(endpoint)

    def get_man_method_codes(self) -> RcrainfoResponse:
        """
        Retrieve Management Method Codes

        Returns:
            dict: object with management method codes
        """
        endpoint = f'{self.base_url}/api/v1/lookup/management-method-codes'
        return self.__rcra_get(endpoint)

    def get_waste_min_codes(self) -> RcrainfoResponse:
        """
        Retrieve Waste Minimization Codes

        Returns:
            dict: object with waste minimization codes
        """
        endpoint = f'{self.base_url}/api/v1/lookup/waste-minimization-codes'
        return self.__rcra_get(endpoint)

    def get_ports_of_entry(self) -> RcrainfoResponse:
        """
        Retrieve Ports of Entry

        Returns:
            dict: object with ports of entry
        """
        endpoint = f'{self.base_url}/api/v1/lookup/ports-of-entry'
        return self.__rcra_get(endpoint)

    def check_site_exists(self, site_id) -> RcrainfoResponse:
        """
        Check if provided Site ID exists
                
        Args:
            site_id (str): EPA site ID
        
        Returns:
            result (boolean): true/false confirmation if site exists
        """
        endpoint = f'{self.base_url}/api/v1/site-exists/{site_id}'
        return self.__rcra_get(endpoint)

    def site_search(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve sites based on some or all of the provided criteria
        
        Args:
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
        endpoint = f'{self.base_url}/api/v1/site-search'
        return self.__rcra_post(endpoint, **kwargs)

    def user_search(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve users based on some or all of the provided criteria. Only users of sites accessible
        to the API keyholder will be visible
        
        Args:
            userId (str) : A RCRAInfo username
            siteIds (array of strings) : One or more EPA site IDs
            pageNumber (number): must be greater than 0
        
        Returns:
            dict: object containing list of users matching criteria and details about each user
        """
        endpoint = f'{self.base_url}/api/v1/user/user-search'
        return self.__rcra_post(endpoint, **kwargs)

    def get_billing_history(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve billing history for a given billing account ID
        
        Args:
            billing_account (str): EPA Site ID
            start_month_year (date): First bill to be included (MM/YYYY format)
            end_month_year (date): Final bill to be included (MM/YYYY format)
            
        Returns:
            dict: object containing billing history for the specified site and period
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/billing/bill-history'
        return self.__rcra_post(endpoint, **kwargs)

    def get_bill(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve bill information for a given bill ID and account ID
        
        Args:
            billId (str): Bill ID
            billingAccount (str): EPA Site ID
            monthYear (date): Billing month (as MM/YYYY). Optional if billId is provided
        
        Returns:
            dict: object containing bill information for the specified ID and account
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/billing/bill'
        return self.__rcra_post(endpoint, **kwargs)

    def search_bill(self, **kwargs) -> RcrainfoResponse:
        """
        Search and retrieve bills using all or some of the provided criteria
        
        Args:
            billingAccount (str): EPA Site ID
            billStatus (str): Active, Paid, Unpaid, ReadyForPayment, Credit, InProgress, SendToCollections, ZeroBalance.
            startDate(date): Beginning of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            endDate (date): End of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            amountChanged (boolean): True or false
            pageNumber (number): Must be greater than 0
            
        Returns:
            dict: object with bills matching criteria
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/billing/bill-search'
        return self.__rcra_post(endpoint, **kwargs)

    def get_attachments(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans
            or electronic copies) for the given MTN
        """
        resp = RcrainfoResponse(requests.get(f'{self.base_url}/api/v1/emanifest/manifest/{mtn}/attachments',
                                             headers={'Accept': 'multipart/mixed',
                                                      'Authorization': f'Bearer {self.token}'},
                                             stream=True))
        if resp.response:
            resp.decode()
        return resp

    def search_mtn(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers based on all or some of provided search criteria
        
        Args:
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
        endpoint = f'{self.base_url}/api/v1/emanifest/search'
        return self.__rcra_post(endpoint, **kwargs)

    def get_correction_details(self, mtn) -> RcrainfoResponse:
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/correction-details/{mtn}'
        return self.__rcra_get(endpoint)

    def get_correction_version(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve details of manifest correction version based on all or some of the provided search criteria

        Args:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest version number
            
        Returns:
            dict: object containing correction details
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/correction-version'
        return self.__rcra_post(endpoint, **kwargs)

    def get_mtn_by_site(self, site_id) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Args:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest-tracking-numbers/{site_id}'
        return self.__rcra_get(endpoint)

    def get_man_by_mtn(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/{mtn}'
        return self.__rcra_get(endpoint)

    def get_sites(self, state_code, site_type) -> RcrainfoResponse:
        """
        Retrieve site ids for provided criteria
        
        Args:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
        
        Returns:
            dict: object containing site ID numbers
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/site-ids/{state_code}/{site_type}'
        return self.__rcra_get(endpoint)

    def correct(self, manifest_json, zip_file=None) -> RcrainfoResponse:
        """
        Correct Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        m = _encode_manifest(manifest_json, zip_file)
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/correct'
        return self.__rcra_put(endpoint, m)

    def revert(self, mtn) -> RcrainfoResponse:
        """
        Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing confirmation of correction
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/revert/{mtn}'
        return self.__rcra_get(endpoint)

    def get_correction_attachments(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve attachments of corrected manifests based all or some of the provided search criteria

        Args:
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
        resp = RcrainfoResponse(
            requests.post(f'{self.base_url}/api/v1/emanifest/manifest/correction-version/attachments',
                          headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                   'Authorization': f'Bearer {self.token}'},
                          data=json.dumps(dict(**kwargs))))
        if resp.response:
            resp.decode()
        return resp

    def check_mtn_exists(self, mtn) -> RcrainfoResponse:
        """
        Check if Manifest Tracking Number (MTN) exists and return basic details
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing MTN details and confirmation if site exists
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/mtn-exists/{mtn}'
        return self.__rcra_get(endpoint)

    def update(self, manifest_json, zip_file=None) -> RcrainfoResponse:
        """
        Update Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        m = _encode_manifest(manifest_json, zip_file)

        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/update'
        return self.__rcra_put(endpoint, m)

    def delete(self, mtn) -> RcrainfoResponse:
        """
        Delete selected manifest
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: message of success or failure
        """
        endpoint = f'{self.base_url}/api/v1/emanifest/manifest/delete/{mtn}'
        return self.__rcra_delete(endpoint)

    def save(self, manifest_json, zip_file=None) -> RcrainfoResponse:
        """
        Save Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        m = _encode_manifest(manifest_json, zip_file)
        resp = RcrainfoResponse(requests.post(f'{self.base_url}/api/v1/emanifest/manifest/save',
                                              headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                                       'Authorization': f'Bearer {self.token}'},
                                              data=m))
        return resp

    def generate_ui_link(self, **kwargs) -> RcrainfoResponse:
        """
        Generate link to the user interface (UI) of the RCRAInfo e-Manifest module
        
        Args:
            page (str): Dashboard, BulkSign, BulkQuickSign, Edit, View, Sign. Case-sensitive
            epaSiteId (Str): EPA Site ID
            manifestTrackingNumber (str): Manifest tracking number (optional)
            filter (list): List of MTNs (optional)
            
        Returns:
            dict: object containing link to UI
        """
        endpoint = f'{self.base_url}/api/v1/links/emanifest'
        return self.__rcra_post(endpoint, **kwargs)

    def cme_lookup(self, activity_location, agency_code, nrr_flag=True) -> RcrainfoResponse:
        """
        Retrieve all lookups for specific activity location and agency code, including staff,
        focus area and sub-organization
        
        Args:
            activity_location (str): Two-letter US postal state code
            agency_code (str): One-letter code. B (State Contractor/Grantee),
                                                C (EPA Contractor/Grantee), E (EPA),
                                                L (Local), N (Native American), S (State),
                                                T (State-Initiated Oversight/Observation/Training Actions),
                                                X (EPA-Initiated Oversight/Observation/Training Actions),
                                                J (Joint State), P (Joint EPA)
            nrr_flag (boolean): True/False if Non-Financial Record Review
        
        Returns:
            dict: object containing CME lookups
        """
        endpoint = f'{self.base_url}/api/v1/state/cme/evaluation/lookups/{activity_location}/{agency_code}/' \
                   f'{str(nrr_flag)}'
        return self.__rcra_get(endpoint)

    def cme_indicators(self):
        """
        Retrieve all evaluation indicators

        Returns:
            dict: object containing all evaluation indicators
        """
        endpoint = f'{self.base_url}/api/v1/state/cme/evaluation/evaluation-indicators'
        return self.__rcra_get(endpoint)

    def cme_types(self) -> RcrainfoResponse:
        """
        Retrieve all evaluation types

        Returns:
            dict: object containing all evaluation types
        """
        endpoint = f'{self.base_url}/api/v1/state/cme/evaluation/evaluation-types'
        return self.__rcra_get(endpoint)

    def get_attachments_reg(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or
            electronic copies) for the given MTN
              message of success or failure
        """
        resp = RcrainfoResponse(requests.get(f'{self.base_url}/api/v1/state/emanifest/manifest/{mtn}/attachments',
                                             headers={'Accept': 'multipart/mixed',
                                                      'Authorization': f'Bearer {self.token}'},
                                             stream=True))
        if resp.response:
            resp.decode()
        return resp

    def search_mtn_reg(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers based on all or some of provided search criteria
        
        Args:
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
        endpoint = f'{self.base_url}/api/v1/state/emanifest/search'
        return self.__rcra_post(endpoint, **kwargs)

    def get_correction_details_reg(self, mtn) -> RcrainfoResponse:
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        endpoint = f'{self.base_url}/api/v1/state/emanifest/manifest/correction-details/{mtn}'
        return self.__rcra_get(endpoint)

    def get_correction_version_reg(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve details of manifest correction version based on all or some of the provided search criteria

        Args:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest version number
            
        Returns:
            dict: object containing correction details
        """
        endpoint = f'{self.base_url}/api/v1/state/emanifest/manifest/correction-version'
        return self.__rcra_post(endpoint, **kwargs)

    def get_mtn_by_site_reg(self, site_id) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Args:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        endpoint = f'{self.base_url}/api/v1/state/emanifest/manifest-tracking-numbers/{site_id}'
        return self.__rcra_get(endpoint)

    def get_man_by_mtn_reg(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        endpoint = f'{self.base_url}/api/v1/state/emanifest/manifest/{mtn}'
        return self.__rcra_get(endpoint)

    def get_sites_reg(self, state_code, site_type) -> RcrainfoResponse:
        """
        Retrieve site ids for provided criteria
        
        Args:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
        
        Returns:
            dict: object containing site ID numbers
        """
        endpoint = f'{self.base_url}/api/v1/state/emanifest/site-ids/{state_code}/{site_type}'
        return self.__rcra_get(endpoint)

    def get_handler_reg(self, handler_id, details=False) -> RcrainfoResponse:
        """
        Retrieve a list of handler source records (and optional details) for a specific handler ID
        
        Args:
            handler_id (str): EPA Site ID number
            details (boolean): True/false to request additional details. Optional; defaults to False
            
        Returns:
            dict: object containing handler source records (and optional details)
        """
        endpoint = f'/api/v1/state/handler/sources/{handler_id}/{str(details)}'
        return self.__rcra_get(endpoint)


def new_client(base_url) -> RcrainfoClient:
    """
    Create instance of RCRAInfoClient, helper function

    Args:
        base_url (str): either 'prod', 'preprod' or url up to '/api/'

    Returns:
        client: Instance of RCRAInfo service and emanifest module functions
    """
    client_url = _parse_url(base_url)
    return RcrainfoClient(client_url)


def _parse_url(base_url: str) -> str:
    """emanifest-py internal helper function"""
    if "https" not in base_url:
        urls = {
            "PROD": "https://rcrainfo.epa.gov/rcrainfoprod/rest/",
            "PREPROD": "https://rcrainfopreprod.epa.gov/rcrainfo/rest/"
        }
        if base_url.upper() in urls:
            return urls[base_url.upper()]
        else:
            logging.warning("Base url not recognized, you can use the argument "
                            "'preprod' or 'prod' to target their respective environments")
    else:
        return base_url


# TODO: accept file paths and string/byte stream as arguments
#  A db probably won't store in filesystem
#  this function is just asking for problems for the time being
def _encode_manifest(manifest_json, zip_file=None):
    """emanifest-py internal helper function"""
    multipart_attachment = None
    if zip_file:
        if os.path.isfile(manifest_json) & os.path.isfile(zip_file):
            multipart_attachment = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
                "attachment": (zip_file, open(zip_file, 'rb'), 'application/zip')
            })
    else:
        if os.path.isfile(manifest_json):
            multipart_attachment = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
            })
        else:
            multipart_attachment = encoder.MultipartEncoder(fields={
                "manifest": ('manifest', manifest_json, 'application/json'),
            })
    return multipart_attachment
