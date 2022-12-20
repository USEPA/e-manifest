"""
e-Manifest library for using the e-Manifest API
see https://github.com/USEPA/e-manifest
"""
import io
import logging
import os
import json
import sys
import zipfile
from requests_toolbelt.multipart import decoder, encoder
import requests
import datetime


class RcrainfoResponse:

    def __init__(self, response: requests.Response):
        self.response = response
        self.ok = response.ok
        self.json = None
        self.zip = None

    def __repr__(self):
        return f'Object: RcrainfoResponse with status {self.ok}'

    def ExtractAttributes(self):
        if self.response:
            self.ok = self.response.ok
            self.json = self.response.json()

    def DecodeMultipart(self):
        multipart_data = decoder.MultipartDecoder.from_response(self.response)
        for part in multipart_data.parts:
            if part.headers[b'Content-Type'] == b'application/json':
                self.json = part.text
            else:
                zip_contents = zipfile.ZipFile(io.BytesIO(part.content))
                self.zip = zip_contents


# noinspection PyIncorrectDocstring
class RcrainfoClient:
    def __init__(self, base_url: str, timeout=10) -> None:
        self.base_url = base_url
        self.token = None
        self.token_expiration = None
        self.timeout = timeout

    def __repr__(self) -> str:
        return f'Object: RcrainfoClient with base url {self.base_url}'

    def Auth(self, api_id, api_key) -> None:
        """
        Authenticate user's RCRAInfo API ID and Key to generate token for use by other functions
        
        Args:
            api_id (str): API ID of RCRAInfo User with Site Manager level permission.
            api_key (str): User's RCRAInfo API key. Generated alongside the api_id in RCRAInfo
        
        Returns:
            token (client): Authentication token for use by other emanifest functions. Expires after 20 minutes 
        """
        auth_url = f'{self.base_url}api/v1/auth/{api_id}/{api_key}'
        resp = requests.get(auth_url, timeout=self.timeout)
        if resp.ok:
            self.token = resp.json()['token']
            expire = resp.json()['expiration']
            # see datetime docs https://docs.python.org/3.7/library/datetime.html#strftime-strptime-behavior
            expire_format = '%Y-%m-%dT%H:%M:%S.%f%z'
            self.token_expiration = datetime.datetime.strptime(expire, expire_format)

    def __RCRAGet(self, endpoint) -> RcrainfoResponse:
        resp = RcrainfoResponse(requests.get(endpoint, timeout=self.timeout,
                                             headers={'Accept': 'application/json',
                                                      'Authorization': 'Bearer ' + self.token}))
        resp.ExtractAttributes()
        return resp

    def __RCRAPost(self, endpoint, **kwargs) -> RcrainfoResponse:
        resp = RcrainfoResponse(requests.post(endpoint, timeout=self.timeout,
                                              headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                                       'Authorization': 'Bearer ' + self.token},
                                              data=json.dumps(dict(**kwargs))))
        resp.ExtractAttributes()
        return resp

    def __RCRADelete(self, endpoint) -> RcrainfoResponse:
        resp = RcrainfoResponse(requests.delete(endpoint, timeout=self.timeout,
                                                headers={'Accept': 'application/json',
                                                         'Authorization': 'Bearer ' + self.token}))
        resp.ExtractAttributes()
        return resp

    def __RCRAPut(self, endpoint, m) -> RcrainfoResponse:
        resp = RcrainfoResponse(requests.put(endpoint, timeout=self.timeout,
                                             headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                                      'Authorization': 'Bearer ' + self.token}, data=m))
        resp.ExtractAttributes()
        return resp

    def GetSiteDetails(self, epa_id) -> RcrainfoResponse:
        """
        Retrieve site details for a given Site ID
        
        Args:
            epa_id (str): EPA site ID
        
        Returns:
            dict: object with EPA ID site details
        """
        endpoint = self.base_url + '/api/v1/site-details/' + epa_id
        return self.__RCRAGet(endpoint)

    def GetHazardClasses(self) -> RcrainfoResponse:
        """
        Retrieve all DOT Hazard Classes
        
        Returns:
            dict: object with DOT hazard classes
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/hazard-classes'
        return self.__RCRAGet(endpoint)

    def GetPackingGroups(self) -> RcrainfoResponse:
        """
        Retrieve all DOT Packing Groups
        
        Returns:
            dict: object with DOT packing groups
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/packing-groups'
        return self.__RCRAGet(endpoint)

    def GetHazClass_SN_ID(self, ship_name, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number 
        
        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT hazard classes
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/' + ship_name + '/' + id_num
        return self.__RCRAGet(endpoint)

    def GetPackGroups_SN_ID(self, ship_name, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Packing Groups by DOT Proper Shipping name and ID Number 
        
        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT packing groups
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/' + ship_name + '/' + id_num
        return self.__RCRAGet(endpoint)

    def GetIDByShipName(self, ship_name) -> RcrainfoResponse:
        """
        Retrieve DOT ID number by DOT Proper Shipping name
        
        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            
        Returns:
            dict: object with DOT ID number
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/id-numbers-by-shipping-name/' + ship_name
        return self.__RCRAGet(endpoint)

    def GetShipNameByID(self, id_num) -> RcrainfoResponse:
        """
        Retrieve DOT Proper Shipping name by DOT ID number
        
        Args:
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT Proper Shipping name 
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/proper-shipping-names-by-id-number/' + id_num
        return self.__RCRAGet(endpoint)

    def GetTNSuffix(self) -> RcrainfoResponse:
        """
        Retrieve Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with allowable MTN suffixes
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes'
        return self.__RCRAGet(endpoint)

    def GetTNSuffixALL(self) -> RcrainfoResponse:
        """
        Retrieve ALL Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with all allowable MTN suffixes
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes-ALL'
        return self.__RCRAGet(endpoint)

    def GetContainerTypes(self) -> RcrainfoResponse:
        """
        Retrieve Container Types

        Returns:
            dict: object with container types
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/container-types'
        return self.__RCRAGet(endpoint)

    def GetQuantityUOM(self) -> RcrainfoResponse:
        """
        Retrieve Quantity Units of Measure (UOM)

        Returns:
            dict: object with quantity UOM
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/quantity-uom'
        return self.__RCRAGet(endpoint)

    def GetLoadTypes(self) -> RcrainfoResponse:
        """
        Retrieve PCB Load Types

        Returns:
            dict: object with load types
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/load-types'
        return self.__RCRAGet(endpoint)

    def GetShippingNames(self) -> RcrainfoResponse:
        """
        Retrieve DOT Proper Shipping Names

        Returns:
            dict: object with DOT Proper Shipping names
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/proper-shipping-names'
        return self.__RCRAGet(endpoint)

    def GetIDNums(self) -> RcrainfoResponse:
        """
        Retrieve DOT Shipping ID numbers

        Returns:
            dict: object with DOT Shipping ID numbers
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/id-numbers'
        return self.__RCRAGet(endpoint)

    def GetDensityUOM(self) -> RcrainfoResponse:
        """
        Retrieve Density Units of Measure (UOM)

        Returns:
            dict: object with density UOM
        """
        endpoint = self.base_url + '/api/v1/lookup/density-uom'
        return self.__RCRAGet(endpoint)

    def GetFormCodes(self) -> RcrainfoResponse:
        """
        Retrieve Form Codes

        Returns:
            dict: object with form codes
        """
        endpoint = self.base_url + '/api/v1/lookup/form-codes'
        return self.__RCRAGet(endpoint)

    def GetSourceCodes(self) -> RcrainfoResponse:
        """
        Retrieve Source Codes

        Returns:
            dict: object with source codes
        """
        endpoint = self.base_url + '/api/v1/lookup/source-codes'
        return self.__RCRAGet(endpoint)

    def GetStateWasteCodes(self, state_code) -> RcrainfoResponse:
        """
        Retrieve State Waste Codes

        Returns:
            dict: object with state waste codes
        """
        endpoint = self.base_url + '/api/v1/lookup/state-waste-codes/' + state_code
        return self.__RCRAGet(endpoint)

    def GetFedWasteCodes(self) -> RcrainfoResponse:
        """
        Retrieve Federal Waste Codes

        Returns:
            dict: object with federal waste codes
        """
        endpoint = self.base_url + '/api/v1/lookup/federal-waste-codes'
        return self.__RCRAGet(endpoint)

    def GetManMethodCodes(self) -> RcrainfoResponse:
        """
        Retrieve Management Method Codes

        Returns:
            dict: object with management method codes
        """
        endpoint = self.base_url + '/api/v1/lookup/management-method-codes'
        return self.__RCRAGet(endpoint)

    def GetWasteMinCodes(self) -> RcrainfoResponse:
        """
        Retrieve Waste Minimization Codes

        Returns:
            dict: object with waste minimization codes
        """
        endpoint = self.base_url + '/api/v1/lookup/waste-minimization-codes'
        return self.__RCRAGet(endpoint)

    def GetPortsOfEntry(self) -> RcrainfoResponse:
        """
        Retrieve Ports of Entry

        Returns:
            dict: object with ports of entry
        """
        endpoint = self.base_url + '/api/v1/lookup/ports-of-entry'
        return self.__RCRAGet(endpoint)

    def CheckSiteExists(self, site_id) -> RcrainfoResponse:
        """
        Check if provided Site ID exists
                
        Args:
            site_id (str): EPA site ID
        
        Returns:
            result (boolean): true/false confirmation if site exists
        """
        endpoint = self.base_url + '/api/v1/site-exists/' + site_id
        return self.__RCRAGet(endpoint)

    def SiteSearch(self, **kwargs) -> RcrainfoResponse:
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
        endpoint = self.base_url + '/api/v1/site-search'
        return self.__RCRAPost(endpoint, **kwargs)

    def UserSearch(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve users based on some or all of the provided criteria. Only users of sites accessible to the API key holder will be visible
        
        Args:
            userId (str) : A RCRAInfo username
            siteIds (array of strings) : One or more EPA site IDs
            pageNumber (number): must be greater than 0
        
        Returns:
            dict: object containing list of users matching criteria and details about each user
        """
        endpoint = self.base_url + '/api/v1/user/user-search'
        return self.__RCRAPost(endpoint, **kwargs)
    
    def GetBillingHistory(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve billing history for a given billing account ID
        
        Args:
            billing_account (str): EPA Site ID
            start_month_year (date): First bill to be included (MM/YYYY format)
            end_month_year (date): Final bill to be included (MM/YYYY format)
            
        Returns:
            dict: object containing billing history for the specified site and period
        """
        endpoint = self.base_url + '/api/v1/emanifest/billing/bill-history'
        return self.__RCRAPost(endpoint, **kwargs)

    def GetBill(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve bill information for a given bill ID and account ID
        
        Args:
            billId (str): Bill ID
            billingAccount (str): EPA Site ID
            monthYear (date): Billing month (as MM/YYYY). Optional if billId is provided
        
        Returns:
            dict: object containing bill information for the specified ID and account
        """
        endpoint = self.base_url + '/api/v1/emanifest/billing/bill'
        return self.__RCRAPost(endpoint, **kwargs)

    def SearchBill(self, **kwargs) -> RcrainfoResponse:
        """
        Search and retrieve bills using all or some of the provided criteria
        
        Args:
            billingAccount (str): EPA Site ID
            billStatus (str): Active, Paid, Unpaid, ReadyForPayment, Credit, InProgress, SendToCollections, ZeroBalance. Case-sensitive
            startDate(date): Beginning of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            endDate (date): End of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            amountChanged (boolean): True or false
            pageNumber (number): Must be greater than 0
            
        Returns:
            dict: object with bills matching criteria
        """
        endpoint = self.base_url + '/api/v1/emanifest/billing/bill-search'
        return self.__RCRAPost(endpoint, **kwargs)

    def GetAttachments(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
        """
        resp = RcrainfoResponse(requests.get(self.base_url + '/api/v1/emanifest/manifest/' + mtn + '/attachments',
                                             headers={'Accept': 'multipart/mixed',
                                                      'Authorization': 'Bearer ' + self.token},
                                             stream=True))
        if resp.response:
            resp.DecodeMultipart()
        else:
            resp.ok = False
        return resp

    def SearchMTN(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers based on all or some of provided search criteria
        
        Args:
            stateCode (str): Two-letter US postal state code
            siteId (str): EPA Site ID
            status (str): Pending, Scheduled, InTransit, Received, ReadyForSignature, Signed, SignedComplete, UnderCorrection, Corrected. Case-sensitive
            dateType (str): CertifiedDate, ReceivedDate, ShippedDate, UpdatedDate. Case-sensitive
            siteType (str): Generator, Tsdf, Transporter, RejectionInfo_AlternateTsdf. Case-sensitive
            startDate (date): Start date for search period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            endDate (date): End date for search period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        
        Returns:
            dict: object containing manifest tracking numbers matching criteria
        """
        endpoint = self.base_url + '/api/v1/emanifest/search'
        return self.__RCRAPost(endpoint, **kwargs)

    def GetCorrectionDetails(self, mtn) -> RcrainfoResponse:
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/correction-details/' + mtn
        return self.__RCRAGet(endpoint)

    def GetCorrectionVersion(self, **kwargs) -> RcrainfoResponse:
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
        endpoint = self.base_url + '/api/v1/emanifest/manifest/correction-version'
        return self.__RCRAPost(endpoint, **kwargs)

    def GetMTNBySite(self, site_id) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Args:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest-tracking-numbers/' + site_id
        return self.__RCRAGet(endpoint)

    def GetManByMTN(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/' + mtn
        return self.__RCRAGet(endpoint)

    def GetSites(self, state_code, site_type) -> RcrainfoResponse:
        """
        Retrieve site ids for provided criteria
        
        Args:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
        
        Returns:
            dict: object containing site ID numbers
        """
        endpoint = self.base_url + '/api/v1/emanifest/site-ids/' + state_code + '/' + site_type
        return self.__RCRAGet(endpoint)

    def Correct(self, manifest_json, zip_file=None) -> RcrainfoResponse:
        """
        Correct Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        m = encode_manifest(manifest_json, zip_file)
        endpoint = self.base_url + '/api/v1/emanifest/manifest/correct'
        return self.__RCRAPut(endpoint, m)

    def Revert(self, mtn) -> RcrainfoResponse:
        """
        Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing confirmation of correction
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/revert/' + mtn
        return self.__RCRAGet(endpoint)

    def GetCorrectionAttachments(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve attachments of corrected manifests based all or some of the provided search criteria

        Args:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest version number
            
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
            print: message of success or failure
        """
        resp = RcrainfoResponse(
            requests.post(self.base_url + '/api/v1/emanifest/manifest/correction-version/attachments',
                          headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                   'Authorization': 'Bearer ' + self.token},
                          data=json.dumps(dict(**kwargs))))
        if resp.response:
            resp.DecodeMultipart()
        else:
            resp.ok = False
        return resp

    def CheckMTNExists(self, mtn) -> RcrainfoResponse:
        """
        Check if Manifest Tracking Number (MTN) exists and return basic details
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing MTN details and confirmation if site exists
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/mtn-exists/' + mtn
        return self.__RCRAGet(endpoint)

    def Update(self, manifest_json, zip_file=None) -> RcrainfoResponse:
        """
        Update Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        m = encode_manifest(manifest_json, zip_file)

        endpoint = self.base_url + '/api/v1/emanifest/manifest/update'
        return self.__RCRAPut(endpoint, m)

    def Delete(self, mtn) -> RcrainfoResponse:
        """
        Delete selected manifest
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: message of success or failure
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/delete/' + mtn
        return self.__RCRADelete(endpoint)

    def Save(self, manifest_json, zip_file=None) -> RcrainfoResponse:
        """
        Save Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        m = encode_manifest(manifest_json, zip_file)
        resp = RcrainfoResponse(requests.post(self.base_url + '/api/v1/emanifest/manifest/save',
                                              headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                                       'Authorization': 'Bearer ' + self.token},
                                              data=m))
        return resp

    def GenerateUILink(self, **kwargs) -> RcrainfoResponse:
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
        endpoint = self.base_url + '/api/v1/links/emanifest'
        return self.__RCRAPost(endpoint, **kwargs)

    def CMELookup(self, activity_location, agency_code, nrr_flag=True) -> RcrainfoResponse:
        """
        Retrieve all lookups for specific activity location and agency code, including staff, focus area and sub-organization
        
        Args:
            activity_location (str): Two-letter US postal state code
            agency_code (str): One-letter code. B (State Contractor/Grantee), C (EPA Contractor/Grantee), E (EPA), L (Local), N (Native American), S (State),
                                                T (State-Initiated Oversight/Observation/Training Actions), X (EPA-Initiated Oversight/Observation/Training Actions),
                                                J (Joint State), P (Joint EPA)
            nrr_flag (boolean): True/False if Non-Financial Record Review
        
        Returns:
            dict: object containing CME lookups
        """
        endpoint = self.base_url + '/api/v1/state/cme/evaluation/lookups/' + activity_location + '/' + agency_code + '/' + str(
            nrr_flag)
        return self.__RCRAGet(endpoint)

    def CMEIndicators(self):
        """
        Retrieve all evaluation indicators

        Returns:
            dict: object containing all evaluation indicators
        """
        endpoint = self.base_url + '/api/v1/state/cme/evaluation/evaluation-indicators'
        return self.__RCRAGet(endpoint)

    def CMETypes(self) -> RcrainfoResponse:
        """
        Retrieve all evaluation types

        Returns:
            dict: object containing all evaluation types
        """
        endpoint = self.base_url + '/api/v1/state/cme/evaluation/evaluation-types'
        return self.__RCRAGet(endpoint)

    def GetAttachmentsReg(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
              message of success or failure
        """
        resp = RcrainfoResponse(requests.get(self.base_url + '/api/v1/state/emanifest/manifest/' + mtn + '/attachments',
                                             headers={'Accept': 'multipart/mixed',
                                                      'Authorization': 'Bearer ' + self.token},
                                             stream=True))
        if resp.response:
            resp.DecodeMultipart()
        else:
            resp.ok = False
        return resp

    def SearchMTNReg(self, **kwargs) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers based on all or some of provided search criteria
        
        Args:
            stateCode (str): Two-letter US postal state code
            siteId (str): EPA Site ID
            status (str): Pending, Scheduled, InTransit, Received, ReadyForSignature, Signed, SignedComplete, UnderCorrection, Corrected. Case-sensitive
            dateType (str): CertifiedDate, ReceivedDate, ShippedDate, UpdatedDate. Case-sensitive
            siteType (str): Generator, Tsdf, Transporter, RejectionInfo_AlternateTsdf. Case-sensitive
            startDate (date): Start date for search period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            endDate (date): End date for search period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        
        Returns:
            dict: object containing manifest tracking numbers matching criteria
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/search'
        return self.__RCRAPost(endpoint, **kwargs)

    def GetCorrectionDetailsReg(self, mtn) -> RcrainfoResponse:
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/manifest/correction-details/' + mtn
        return self.__RCRAGet(endpoint)

    def GetCorrectionVersionReg(self, **kwargs) -> RcrainfoResponse:
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
        endpoint = self.base_url + '/api/v1/state/emanifest/manifest/correction-version'
        return self.__RCRAPost(endpoint, **kwargs)

    def GetMTNBySiteReg(self, site_id) -> RcrainfoResponse:
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Args:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/manifest-tracking-numbers/' + site_id
        return self.__RCRAGet(endpoint)

    def GetManByMTNReg(self, mtn) -> RcrainfoResponse:
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/manifest/' + mtn
        return self.__RCRAGet(endpoint)

    def GetSitesReg(self, state_code, site_type) -> RcrainfoResponse:
        """
        Retrieve site ids for provided criteria
        
        Args:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
        
        Returns:
            dict: object containing site ID numbers
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/site-ids/' + state_code + '/' + site_type
        return self.__RCRAGet(endpoint)

    def GetHandlerReg(self, handler_id, details=False) -> RcrainfoResponse:
        """
        Retrieve a list of handler source records (and optional details) for a specific handler ID
        
        Args:
            handler_id (str): EPA Site ID number
            details (boolean): True/false to request additional details. Optional; defaults to False
            
        Returns:
            dict: object containing handler source records (and optional details)
        """
        endpoint = '/api/v1/state/handler/sources/' + handler_id + '/' + str(details)
        return self.__RCRAGet(endpoint)


def new_client(base_url) -> RcrainfoClient:
    """
    Create instance of RCRAInfoClient

    Args:
        base_url (str): either 'prod', 'preprod' or url up to '/api/

    Returns:
        client: Instance of RCRAInfo service and emanifest module functions
    """
    if "https" not in base_url:
        urls = {
            "PROD": "https://rcrainfo.epa.gov/rcrainfoprod/rest/",
            "PREPROD": "https://rcrainfopreprod.epa.gov/rcrainfo/rest/"
        }
        if base_url.upper() in urls:
            base_url = urls[base_url.upper()]
        else:
            logging.warning("Base url not recognized, you can use the argument "
                            "'preprod' or 'prod' to target their respective environments")
    client = RcrainfoClient(base_url)
    return client


# TODO: accept file paths and string/byte stream as arguments
#  A db probably won't store in filesystem
#  this function is just asking for problems for the time being
def encode_manifest(manifest_json, zip_file=None):
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
