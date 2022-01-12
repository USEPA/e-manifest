"""
e-Manifest library for using the e-Manifest API
see https://github.com/USEPA/e-manifest
"""
import io
import json
import sys
import zipfile
from requests_toolbelt.multipart import decoder, encoder
import requests
import datetime


def new_client(base_url):
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
            print("base_url not recognized")
            sys.exit(1)
    client = RcrainfoClient(base_url)
    return client


class RcrainfoClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.token_expiration = None

    def Auth(self, api_id, api_key):
        """
        Authenticate user's RCRAInfo API ID and Key to generate token for use by other functions
        
        Args:
            api_id (str): API ID of RCRAInfo User with Site Manager level permission.
            api_key (str): User's RCRAInfo API key. Generated alongside the api_id in RCRAInfo
        
        Returns:
            token (client): Authentication token for use by other emanifest functions. Expires after 20 minutes 
        """
        auth_url = "{base_url}/api/v1/auth/{api_id}/{api_key}".format(
            base_url=self.base_url,
            api_id=api_id,
            api_key=api_key)
        resp = requests.get(auth_url)
        if resp.ok:
            self.token = resp.json()['token']
            expire = resp.json()['expiration']
            # see datetime docs https://docs.python.org/3.7/library/datetime.html#strftime-strptime-behavior
            expire_format = '%Y-%m-%dT%H:%M:%S.%f%z'
            self.token_expiration = datetime.datetime.strptime(expire, expire_format)

    def GetSiteDetails(self, epa_id):
        """
        Retrieve site details for a given Site ID
        
        Args:
            epa_id (str): EPA site ID
        
        Returns:
            dict: object with EPA ID site details
        """
        endpoint = self.base_url + '/api/v1/site-details/' + epa_id
        return self.__RCRAGet(endpoint)

    def GetHazardClasses(self):
        """
        Retrieve all DOT Hazard Classes
        
        Returns:
            dict: object with DOT hazard classes
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/hazard-classes'
        return self.__RCRAGet(endpoint)

    def GetPackingGroups(self):
        """
        Retrieve all DOT Packing Groups
        
        Returns:
            dict: object with DOT packing groups
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/packing-groups'
        return self.__RCRAGet(endpoint)

    def GetHazClass_SN_ID(self, ship_name, id_num):
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

    def GetPackGroups_SN_ID(self, ship_name, id_num):
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

    def GetIDByShipName(self, ship_name):
        """
        Retrieve DOT ID number by DOT Proper Shipping name
        
        Args:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            
        Returns:
            dict: object with DOT ID number
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/id-numbers-by-shipping-name/' + ship_name
        return self.__RCRAGet(endpoint)

    def GetShipNameByID(self, id_num):
        """
        Retrieve DOT Proper Shipping name by DOT ID number
        
        Args:
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT Proper Shipping name 
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/proper-shipping-names-by-id-number/' + id_num
        return self.__RCRAGet(endpoint)

    def GetTNSuffix(self):
        """
        Retrieve Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with allowable MTN suffixes
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes'
        return self.__RCRAGet(endpoint)

    def GetTNSuffixALL(self):
        """
        Retrieve ALL Allowable Manifest Tracking Number (MTN) Suffixes

        Returns:
            dict: object with all allowable MTN suffixes
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes-ALL'
        return self.__RCRAGet(endpoint)

    def GetContainerTypes(self):
        """
        Retrieve Container Types

        Returns:
            dict: object with container types
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/container-types'
        return self.__RCRAGet(endpoint)

    def GetQuantityUOM(self):
        """
        Retrieve Quantity Units of Measure (UOM)

        Returns:
            dict: object with quantity UOM
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/quantity-uom'
        return self.__RCRAGet(endpoint)

    def GetLoadTypes(self):
        """
        Retrieve PCB Load Types

        Returns:
            dict: object with load types
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/load-types'
        return self.__RCRAGet(endpoint)

    def GetShippingNames(self):
        """
        Retrieve DOT Proper Shipping Names

        Returns:
            dict: object with DOT Proper Shipping names
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/proper-shipping-names'
        return self.__RCRAGet(endpoint)

    def GetIDNums(self):
        """
        Retrieve DOT Shipping ID numbers

        Returns:
            dict: object with DOT Shipping ID numbers
        """
        endpoint = self.base_url + '/api/v1/emanifest/lookup/id-numbers'
        return self.__RCRAGet(endpoint)

    def GetDensityUOM(self):
        """
        Retrieve Density Units of Measure (UOM)

        Returns:
            dict: object with density UOM
        """
        endpoint = self.base_url + '/api/v1/lookup/density-uom'
        return self.__RCRAGet(endpoint)

    def GetFormCodes(self):
        """
        Retrieve Form Codes

        Returns:
            dict: object with form codes
        """
        endpoint = self.base_url + '/api/v1/lookup/form-codes'
        return self.__RCRAGet(endpoint)

    def GetSourceCodes(self):
        """
        Retrieve Source Codes

        Returns:
            dict: object with source codes
        """
        endpoint = self.base_url + '/api/v1/lookup/source-codes'
        return self.__RCRAGet(endpoint)

    def GetStateWasteCodes(self, state_code):
        """
        Retrieve State Waste Codes

        Returns:
            dict: object with state waste codes
        """
        endpoint = self.base_url + '/api/v1/lookup/state-waste-codes/' + state_code
        return self.__RCRAGet(endpoint)

    def GetFedWasteCodes(self):
        """
        Retrieve Federal Waste Codes

        Returns:
            dict: object with federal waste codes
        """
        endpoint = self.base_url + '/api/v1/lookup/federal-waste-codes'
        return self.__RCRAGet(endpoint)

    def GetManMethodCodes(self):
        """
        Retrieve Management Method Codes

        Returns:
            dict: object with management method codes
        """
        endpoint = self.base_url + '/api/v1/lookup/management-method-codes'
        return self.__RCRAGet(endpoint)

    def GetWasteMinCodes(self):
        """
        Retrieve Waste Minimization Codes

        Returns:
            dict: object with waste minimization codes
        """
        endpoint = self.base_url + '/api/v1/lookup/waste-minimization-codes'
        return self.__RCRAGet(endpoint)

    def GetPortsOfEntry(self):
        """
        Retrieve Ports of Entry

        Returns:
            dict: object with ports of entry
        """
        endpoint = self.base_url + '/api/v1/lookup/ports-of-entry'
        return self.__RCRAGet(endpoint)

    def CheckSiteExists(self, site_id):
        """
        Check if provided Site ID exists
                
        Args:
            site_id (str): EPA site ID
        
        Returns:
            result (boolean): true/false confirmation if site exists
        """
        endpoint = self.base_url + '/api/v1/site-exists/' + site_id
        return self.__RCRAGet(endpoint)

    def SiteSearch(self, **kwargs):
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

    def GetBillingHistory(self, **kwargs):
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

    def GetBill(self, **kwargs):
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

    def SearchBill(self, **kwargs):
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

    def GetAttachments(self, mtn):
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
        """
        resp = requests.get(self.base_url + '/api/v1/emanifest/manifest/' + mtn + '/attachments',
                              headers={'Accept': 'multipart/mixed', 'Authorization': 'Bearer ' + self.token},
                              stream=True)
        if resp.ok:
            multipart_data = decoder.MultipartDecoder.from_response(resp)
            for part in multipart_data.parts:
                if part.headers[b'Content-Type'] == b'application/json':
                    with open('emanifest.json', 'w') as f:
                        f.write(part.text)
                else:
                    z = zipfile.ZipFile(io.BytesIO(part.content))
                    z.extractall()
        else:
            print('Error: ' + str(resp.json()['message']))

    def SearchMTN(self, **kwargs):
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

    def GetCorrectionDetails(self, mtn):
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/correction-details/' + mtn
        return self.__RCRAGet(endpoint)

    def GetCorrectionVersion(self, **kwargs):
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

    def GetMTNBySite(self, site_id):
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Args:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest-tracking-numbers/' + site_id
        return self.__RCRAGet(endpoint)

    def GetManByMTN(self, mtn):
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/' + mtn
        return self.__RCRAGet(endpoint)

    def GetSites(self, state_code, site_type):
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

    def Correct(self, manifest_json, zip_file=None):
        """
        Correct Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        if zip_file is not None:
            m = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
                "attachment": (zip_file, open(zip_file, 'rb'), 'application/zip')
            })
        else:
            m = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
            })
        
        endpoint = self.base_url + '/api/v1/emanifest/manifest/correct'
        return self.__RCRAPut(endpoint, m)

    def Revert(self, mtn):
        """
        Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing confirmation of correction
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/revert/' + mtn
        return self.__RCRAGet(endpoint)

    def GetCorrectionAttachments(self, **kwargs):
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
        resp = requests.post(self.base_url + '/api/v1/emanifest/manifest/correction-version/attachments',
                            headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                     'Authorization': 'Bearer ' + self.token},
                            data=json.dumps(dict(**kwargs)))
        if resp.ok:
            multipart_data = decoder.MultipartDecoder.from_response(resp)
            for part in multipart_data.parts:
                if part.headers[b'Content-Type'] == b'application/json':
                    with open('emanifest.json', 'w') as f:
                        f.write(part.text)
                else:
                    z = zipfile.ZipFile(io.BytesIO(part.content))
                    z.extractall()
            print('Successfully retrieved.')
        else:
            print('Error: ' + str(resp.json()['message']))

    def CheckMTNExists(self, mtn):
        """
        Check if Manifest Tracking Number (MTN) exists and return basic details
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing MTN details and confirmation if site exists
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/mtn-exists/' + mtn
        return self.__RCRAGet(endpoint)

    def Update(self, manifest_json, zip_file=None):
        """
        Update Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        if zip_file is not None:
            m = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
                "attachment": (zip_file, open(zip_file, 'rb'), 'application/zip')
            })
        else:
            m = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
            })
        
        endpoint = self.base_url + '/api/v1/emanifest/manifest/update'
        return self.__RCRAPut(endpoint, m)

    def Delete(self, mtn):
        """
        Delete selected manifest
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: message of success or failure
        """
        endpoint = self.base_url + '/api/v1/emanifest/manifest/delete/' + mtn
        return self.__RCRADelete(endpoint)

    def Save(self, manifest_json, zip_file=None):
        """
        Save Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Args:
            manifest_json (.json file): Local JSON file containing manifest details
            zip_file (.zip file): Local zip file containing manifest attachments. Optional
            
        Returns:
            dict: message of success or failure
        """
        if zip_file is not None:
            m = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
                "attachment": (zip_file, open(zip_file, 'rb'), 'application/zip')
            })
        else:
            m = encoder.MultipartEncoder(fields={
                "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
            })
        resp = requests.post(self.base_url + '/api/v1/emanifest/manifest/save',
                             headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                      'Authorization': 'Bearer ' + self.token},
                             data=m)
        return resp.json()

    def GenerateUILink(self, **kwargs):
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

    def CMELookup(self, activity_location, agency_code, nrr_flag=True):
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
        endpoint = self.base_url + '/api/v1/state/cme/evaluation/lookups/' + activity_location + '/' + agency_code + '/' + str(nrr_flag)
        return self.__RCRAGet(endpoint)

    def CMEIndicators(self):
        """
        Retrieve all evaluation indicators

        Returns:
            dict: object containing all evaluation indicators
        """
        endpoint = self.base_url + '/api/v1/state/cme/evaluation/evaluation-indicators'
        return self.__RCRAGet(endpoint)

    def CMETypes(self):
        """
        Retrieve all evaluation types

        Returns:
            dict: object containing all evaluation types
        """
        endpoint = self.base_url + '/api/v1/state/cme/evaluation/evaluation-types'
        return self.__RCRAGet(endpoint)

    def GetAttachmentsReg(self, mtn):
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
              message of success or failure
        """
        resp = requests.get(self.base_url + '/api/v1/state/emanifest/manifest/' + mtn + '/attachments',
                              headers={'Accept': 'multipart/mixed', 'Authorization': 'Bearer ' + self.token},
                              stream=True)
        if resp.ok:
            multipart_data = decoder.MultipartDecoder.from_response(attach)
            for part in multipart_data.parts:
                if part.headers[b'Content-Type'] == b'application/json':
                    with open('emanifest.json', 'w') as f:
                        f.write(part.text)
                else:
                    z = zipfile.ZipFile(io.BytesIO(part.content))
                    z.extractall()
            print('Successfully retrieved.')
        else:
            print('Error: ' + str(attach.json()['message']))

    def SearchMTNReg(self, **kwargs):
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

    def GetCorrectionDetailsReg(self, mtn):
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/manifest/correction-details/' + mtn
        return self.__RCRAGet(endpoint)

    def GetCorrectionVersionReg(self, **kwargs):
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

    def GetMTNBySiteReg(self, site_id):
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Args:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/manifest-tracking-numbers/' + site_id
        return self.__RCRAGet(endpoint)

    def GetManByMTNReg(self, mtn):
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Args:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        endpoint = self.base_url + '/api/v1/state/emanifest/manifest/' + mtn
        return self.__RCRAGet(endpoint)

    def GetSitesReg(self, state_code, site_type):
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

    def GetHandler(self, handler_id, details=False):
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

    def __RCRAGet(self, endpoint):
        resp = requests.get(endpoint,
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if resp.ok:
            return resp.json()
        else:
            print('Error: ' + str(resp.json()['message']))
            
    def __RCRAPost(self, endpoint, **kwargs):
        resp = requests.post(endpoint,
                            headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                     'Authorization': 'Bearer ' + self.token},
                            data=json.dumps(dict(**kwargs)))
        if resp.ok:
            return resp.json()
        else:
            print('Error: ' + str(resp.json()['message']))
                   
    def __RCRADelete(self, endpoint):
        resp = requests.delete(endpoint,
                            headers={'Accept': 'application/json','Authorization': 'Bearer ' + self.token})
        if resp.ok:
            return resp.json()
        else:
            print('Error: ' + str(resp.json()['message']))
            
            
    def __RCRAPut(self, endpoint):
        resp = requests.put(endpoint,
                            headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                    'Authorization': 'Bearer ' + self.token},
                            data=m)
        if resp.ok:
            return resp.json()
        else:
            print('Error: ' + str(resp.json()['message']))
