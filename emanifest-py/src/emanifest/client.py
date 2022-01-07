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
    
    Parameters:
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
        
        Parameters:
            api_id (str): User's RCRAInfo API ID. Must have Site Management permissions in RCRAInfo for at least one site
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
        
        Parameters:
            epa_id (str): EPA site ID
        
        Returns:
            dict: object with EPA ID site details
        """
        details = requests.get(self.base_url + '/api/v1/site-details/' + epa_id,
                               headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if details.ok:
            return details.json()
        else:
            print('Error: ' + str(details.json()['message']))

    def GetHazardClasses(self):
        """
        Retrieve all DOT Hazard Classes
        
        Parameters:
            none
        
        Returns
            dict: object with DOT hazard classes
        """
        haz_class = requests.get(self.base_url + '/api/v1/emanifest/lookup/hazard-classes',
                                 headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if haz_class.ok:
            return haz_class.json()
        else:
            print('Error: ' + str(haz_class.json()['message']))

    def GetPackingGroups(self):
        """
        Retrieve all DOT Packing Groups
        
        Parameters:
            none
        
        Returns
            dict: object with DOT packing groups
        """
        pack_groups = requests.get(self.base_url + '/api/v1/emanifest/lookup/packing-groups',
                                   headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if pack_groups.ok:
            return pack_groups.json()
        else:
            print('Error: ' + str(pack_groups.json()['message']))

    def GetHazClass_SN_ID(self, ship_name, id_num):
        """
        Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number 
        
        Parameters:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT hazard classes
        """
        haz_class_sn_id = requests.get(
            self.base_url + '/api/v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/' + ship_name + '/' + id_num,
            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if haz_class_sn_id.ok:
            return haz_class_sn_id.json()
        else:
            print('Error: ' + str(haz_class_sn_id.json()['message']))

    def GetPackGroups_SN_ID(self, ship_name, id_num):
        """
        Retrieve DOT Packing Groups by DOT Proper Shipping name and ID Number 
        
        Parameters:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT packing groups
        """
        pack_group_sn_id = requests.get(
            self.base_url + '/api/v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/' + ship_name + '/' + id_num,
            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if pack_group_sn_id.ok:
            return pack_group_sn_id.json()
        else:
            print('Error: ' + str(pack_group_sn_id.json()['message']))

    def GetIDByShipName(self, ship_name):
        """
        Retrieve DOT ID number by DOT Proper Shipping name
        
        Parameters:
            ship_name (str): DOT proper shipping name. Case-sensitive (e.g. Hydrochloric acid)
            
        Returns:
            dict: object with DOT ID number
        """
        dot_id_sn = requests.get(self.base_url + '/api/v1/emanifest/lookup/id-numbers-by-shipping-name/' + ship_name,
                                 headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if dot_id_sn.ok:
            return dot_id_sn.json()
        else:
            print('Error: ' + str(dot_id_sn.json()['message']))

    def GetShipNameByID(self, id_num):
        """
        Retrieve DOT Proper Shipping name by DOT ID number
        
        Parameters:
            id_num (str): DOT ID number
            
        Returns:
            dict: object with DOT Proper Shipping name 
        """
        dot_sn_id = requests.get(
            self.base_url + '/api/v1/emanifest/lookup/proper-shipping-names-by-id-number/' + id_num,
            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if dot_sn_id.ok:
            return dot_sn_id.json()
        else:
            print('Error: ' + str(dot_sn_id.json()['message']))

    def GetTNSuffix(self):
        """
        Retrieve Allowable Manifest Tracking Number (MTN) Suffixes
        
        Parameters:
            none
        
        Returns:
            dict: object with allowable MTN suffixes
        """
        tns = requests.get(self.base_url + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes',
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if tns.ok:
            return tns.json()
        else:
            print('Error: ' + str(tns.json()['message']))

    def GetTNSuffixALL(self):
        """
        Retrieve ALL Allowable Manifest Tracking Number (MTN) Suffixes
        
        Parameters:
            none
        
        Returns:
            dict: object with all allowable MTN suffixes
        """
        tns_all = requests.get(self.base_url + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes-ALL',
                               headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if tns_all.ok:
            return tns_all.json()
        else:
            print('Error: ' + str(tns_all.json()['message']))

    def GetContainerTypes(self):
        """
        Retrieve Container Types
                
        Parameters:
            none
        
        Returns:
            dict: object with container types
        """
        con_types = requests.get(self.base_url + '/api/v1/emanifest/lookup/container-types',
                                 headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if con_types.ok:
            return con_types.json()
        else:
            print('Error: ' + str(con_types.json()['message']))

    def GetQuantityUOM(self):
        """
        Retrieve Quantity Units of Measure (UOM)
                
        Parameters:
            none
        
        Returns:
            dict: object with quantity UOM
        """
        quantity_uom = requests.get(self.base_url + '/api/v1/emanifest/lookup/quantity-uom',
                                    headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if quantity_uom.ok:
            return quantity_uom.json()
        else:
            print('Error: ' + str(quantity_uom.json()['message']))

    def GetLoadTypes(self):
        """
        Retrieve PCB Load Types
                
        Parameters:
            none
        
        Returns:
            dict: object with load types
        """
        load_types = requests.get(self.base_url + '/api/v1/emanifest/lookup/load-types',
                                  headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if load_types.ok:
            return load_types.json()
        else:
            print('Error: ' + str(load_types.json()['message']))

    def GetShippingNames(self):
        """
        Retrieve DOT Proper Shipping Names
                
        Parameters:
            none
        
        Returns:
            dict: object with DOT Proper Shipping names
        """
        ship_names = requests.get(self.base_url + '/api/v1/emanifest/lookup/proper-shipping-names',
                                  headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if ship_names.ok:
            return ship_names.json()
        else:
            print('Error: ' + str(ship_names.json()['message']))

    def GetIDNums(self):
        """
        Retrieve DOT Shipping ID numbers
                
        Parameters:
            none
        
        Returns:
            dict: obeject with DOT Shipping ID numbers
        """
        id_nums = requests.get(self.base_url + '/api/v1/emanifest/lookup/id-numbers',
                               headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if id_nums.ok:
            return id_nums.json()
        else:
            print('Error: ' + str(id_nums.json()['message']))

    def GetDensityUOM(self):
        """
        Retrieve Density Units of Measure (UOM)
                
        Parameters:
            none
        
        Returns:
            dict: object with density UOM
        """
        density_uom = requests.get(self.base_url + '/api/v1/lookup/density-uom',
                                   headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if density_uom.ok:
            return density_uom.json()
        else:
            print('Error: ' + str(density_uom.json()['message']))

    def GetFormCodes(self):
        """
        Retrieve Form Codes
                
        Parameters:
            none
        
        Returns:
            dict: object with form codes
        """
        form_codes = requests.get(self.base_url + '/api/v1/lookup/form-codes',
                                  headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if form_codes.ok:
            return form_codes.json()
        else:
            print('Error: ' + str(form_codes.json()['message']))

    def GetSourceCodes(self):
        """
        Retrieve Source Codes
                
        Parameters:
            none
        
        Returns:
            dict: object with source codes
        """
        source_codes = requests.get(self.base_url + '/api/v1/lookup/source-codes',
                                    headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if source_codes.ok:
            return source_codes.json()
        else:
            print('Error: ' + str(source_codes.json()['message']))

    def GetStateWasteCodes(self, state_code):
        """
        Retrieve State Waste Codes
                
        Parameters:
            none
        
        Returns:
            dict: object with state waste codes
        """
        sw_codes = requests.get(self.base_url + '/api/v1/lookup/state-waste-codes/' + state_code,
                                headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if sw_codes.ok:
            return sw_codes.json()
        else:
            print('Error: ' + str(sw_codes.json()['message']))

    def GetFedWasteCodes(self):
        """
        Retrieve Federal Waste Codes
                
        Parameters:
            none
        
        Returns:
            dict: object with federal waste codes
        """
        fed_codes = requests.get(self.base_url + '/api/v1/lookup/federal-waste-codes',
                                 headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if fed_codes.ok:
            return fed_codes.json()
        else:
            print('Error: ' + str(fed_codes.json()['message']))

    def GetManMethodCodes(self):
        """
        Retrieve Management Method Codes
                
        Parameters:
            none
        
        Returns:
            dict: object with management method codes
        """
        mm_codes = requests.get(self.base_url + '/api/v1/lookup/management-method-codes',
                                headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if mm_codes.ok:
            return mm_codes.json()
        else:
            print('Error: ' + str(mm_codes.json()['message']))

    def GetWasteMinCodes(self):
        """
        Retrieve Waste Minimization Codes
                
        Parameters:
            none
        
        Returns:
            dict: object with waste minimization codes
        """
        wm_codes = requests.get(self.base_url + '/api/v1/lookup/waste-minimization-codes',
                                headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if wm_codes.ok:
            return wm_codes.json()
        else:
            print('Error: ' + str(wm_codes.json()['message']))

    def GetPortsOfEntry(self):
        """
        Retrieve Ports of Entry
                
        Parameters:
            none
        
        Returns:
            dict: object with ports of entry
        """
        poe = requests.get(self.base_url + '/api/v1/lookup/ports-of-entry',
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if poe.ok:
            return poe.json()
        else:
            print('Error: ' + str(poe.json()['message']))

    def CheckSiteExists(self, site_id):
        """
        Check if provided Site ID exists
                
        Parameters:
            site_id (str): EPA site ID
        
        Returns:
            result (boolean): true/false confirmation if site exists
        """
        exists = requests.get(self.base_url + '/api/v1/site-exists/' + site_id,
                              headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if exists.ok:
            return exists.json()['result']
        else:
            print('Error: ' + str(exists.json()['message']))

    def SiteSearch(self, **kwargs):
        """
        Retrieve sites based on some or all of the provided criteria
        
        Parameters:
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
        site_search = requests.post(self.base_url + '/api/v1/site-search',
                                    headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                             'Authorization': 'Bearer ' + self.token},
                                    data=json.dumps(dict(**kwargs)))
        if site_search.ok:
            return site_search.json()
        else:
            print('Error: ' + str(site_search.json()['message']))

    def GetBillingHistory(self, billing_account, start_month_year, end_month_year):
        """
        Retrieve billing history for a given billing account ID
        
        Parameters:
            billingAccount (str): EPA Site ID
            startMonthYear (date): First bill to be included (MM/YYYY format)
            endMonthYear (date): Final bill to be included (MM/YYYY format)
            
        Returns:
            dict: object containing billing history for the specified site and period
        """
        bill_history = requests.post(self.base_url + '/api/v1/emanifest/billing/bill-history',
                                     headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                              'Authorization': 'Bearer ' + self.token},
                                     data=json.dumps(
                                         {
                                             'billingAccount': billing_account,
                                             'startMonthYear': start_month_year,
                                             'endMonthYear': end_month_year
                                         }
                                     ))
        if bill_history.ok:
            return bill_history.json()
        else:
            print('Error: ' + str(bill_history.json()['message']))

    def GetBill(self, **kwargs):
        """
        Retrieve bill information for a given bill ID and account ID
        
        Parameters:
            billId (str): Bill ID
            billingAccount (str): EPA Site ID
            monthYear (date): Billing month (as MM/YYYY). Optional if billId is provided
        
        Returns:
            dict: object containing bill information for the specified ID and account
        """
        bill = requests.post(self.base_url + '/api/v1/emanifest/billing/bill',
                             headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                      'Authorization': 'Bearer ' + self.token},
                             data=json.dumps(dict(**kwargs)))
        if bill.ok:
            return bill.json()
        else:
            print('Error: ' + str(bill.json()['message']))

    def SearchBill(self, **kwargs):
        """
        Search and retrieve bills using all or some of the provided criteria
        
        Parameters:
            billingAccount (str): EPA Site ID
            billStatus (str): Active, Paid, Unpaid, ReadyForPayment, Credit, InProgress, SendToCollections, ZeroBalance. Case-sensitive
            startDate(date): Beginning of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            endDate (date): End of the billing period (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ)
            amountChanged (boolean): True or false
            pageNumber (number): Must be greater than 0
            
        Returns:
            dict: object with bills matching criteria
        """
        bill_search = requests.post(self.base_url + '/api/v1/emanifest/billing/bill-search',
                                    headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                             'Authorization': 'Bearer ' + self.token},
                                    data=json.dumps(dict(**kwargs)))
        if bill_search.ok:
            return bill_search.json()
        else:
            print('Error: ' + str(bill_search.json()['message']))

    def GetAttachments(self, mtn):
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Parameters:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
        """
        attach = requests.get(self.base_url + '/api/v1/emanifest/manifest/' + mtn + '/attachments',
                              headers={'Accept': 'multipart/mixed', 'Authorization': 'Bearer ' + self.token},
                              stream=True)
        if attach.ok:
            multipart_data = decoder.MultipartDecoder.from_response(attach)
            for part in multipart_data.parts:
                if part.headers[b'Content-Type'] == b'application/json':
                    with open('emanifest.json', 'w') as f:
                        f.write(part.text)
                else:
                    z = zipfile.ZipFile(io.BytesIO(part.content))
                    z.extractall()
        else:
            print('Error: ' + str(attach.json()['message']))

    def SearchMTN(self, **kwargs):
        """
        Retrieve manifest tracking numbers based on all or some of provided search criteria
        
        Parameters:
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
        search_mtn_resp = requests.post(self.base_url + '/api/v1/emanifest/search',
                                        headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                                 'Authorization': 'Bearer ' + self.token},
                                        data=json.dumps(dict(**kwargs)))
        if search_mtn_resp.ok:
            return search_mtn_resp.json()
        else:
            print('Error: ' + str(search_mtn_resp.json()['message']))

    def GetCorrectionDetails(self, mtn):
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Parameters:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        correct = requests.get(self.base_url + '/api/v1/emanifest/manifest/correction-details/' + mtn,
                               headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if correct.ok:
            return correct.json()
        else:
            print('Error: ' + str(correct.json()['message']))

    def GetCorrectionVersion(self, **kwargs):
        """
        Retrieve details of manifest correction version based on all or some of the provided search criteria

        Parameters:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest verion number
            
        Returns:
            dict: object containing correction details
        """
        cvd = requests.post(self.base_url + '/api/v1/emanifest/manifest/correction-version',
                            headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                     'Authorization': 'Bearer ' + self.token},
                            data=json.dumps(dict(**kwargs)))
        if cvd.ok:
            return cvd.json()
        else:
            print('Error: ' + str(cvd.json()['message']))

    def GetMTNBySite(self, site_id):
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Parameters:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        site_mtn = requests.get(self.base_url + '/api/v1/emanifest/manifest-tracking-numbers/' + site_id,
                                headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if site_mtn.ok:
            return site_mtn.json()
        else:
            print('Error: ' + str(site_mtn.json()['message']))

    def GetManByMTN(self, mtn):
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Parameters:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        eman = requests.get(self.base_url + '/api/v1/emanifest/manifest/' + mtn,
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if eman.ok:
            return eman.json()
        else:
            print('Error: ' + str(eman.json()['message']))

    def GetSites(self, state_code, site_type):
        """
        Retrieve site ids for provided criteria
        
        Parameters:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
        
        Returns:
            dict: object containing site ID numbers
        """
        sites = requests.get(self.base_url + '/api/v1/emanifest/site-ids/' + state_code + '/' + site_type,
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if sites.ok:
            return sites.json()
        else:
            print('Error: ' + str(sites.json()['message']))

    def Correct(self, manifest_json, zip_file=None):
        """
        Correct Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Parameters:
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
        correct = requests.put(self.base_url + '/api/v1/emanifest/manifest/correct',
                               headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                        'Authorization': 'Bearer ' + self.token},
                               data=m)
        print(correct.json())

    def Revert(self, mtn):
        """
        Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version
        
        Parameters:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing confirmation of correction
        """
        revert = requests.get(self.base_url + '/api/v1/emanifest/manifest/revert/' + mtn,
                              headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        return revert.json()

    def GetCorrectionAttachments(self, **kwargs):
        """
        Retrieve attachments of corrected manifests based all or some of the provided search criteria

        Parameters:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest verion number
            
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
            print: message of success or failure
        """
        cta = requests.post(self.base_url + '/api/v1/emanifest/manifest/correction-version/attachments',
                            headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                     'Authorization': 'Bearer ' + self.token},
                            data=json.dumps(dict(**kwargs)))
        if cta.ok:
            multipart_data = decoder.MultipartDecoder.from_response(cta)
            for part in multipart_data.parts:
                if part.headers[b'Content-Type'] == b'application/json':
                    with open('emanifest.json', 'w') as f:
                        f.write(part.text)
                else:
                    z = zipfile.ZipFile(io.BytesIO(part.content))
                    z.extractall()
            print('Successfully retrieved.')
        else:
            print('Error: ' + str(cta.json()['message']))

    def CheckMTNExists(self, mtn):
        """
        Check if Manifest Tracking Number (MTN) exists and return basic details
        
        Parameters:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing MTN details and confirmation if site exists
        """
        check_mtn = requests.get(self.base_url + '/api/v1/emanifest/manifest/mtn-exists/' + mtn,
                                 headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if check_mtn.ok:
            return check_mtn.json()
        else:
            print('Error: ' + str(check_mtn.json()['message']))

    def Update(self, manifest_json, zip_file=None):
        """
        Update Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Parameters:
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
        update = requests.put(self.base_url + '/api/v1/emanifest/manifest/update',
                              headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                       'Authorization': 'Bearer ' + self.token},
                              data=m)
        return update.json()

    def Delete(self, mtn):
        """
        Delete selected manifest
        
        Parameters:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: message of success or failure
        """
        delete = requests.delete(self.base_url + '/api/v1/emanifest/manifest/delete/' + mtn,
                                 headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        return delete.json()

    def Save(self, manifest_json, zip_file=None):
        """
        Save Manifest by providing e-Manifest JSON and optional Zip attachment
        
        Parameters:
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
        save = requests.post(self.base_url + '/api/v1/emanifest/manifest/save',
                             headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                      'Authorization': 'Bearer ' + self.token},
                             data=m)
        return save.json()

    def GenerateUILink(self, **kwargs):
        """
        Generate link to the user interface (UI) of the RCRAInfo e-Manifest module
        
        Parameters:
            page (str): Dashboard, BulkSign, BulkQuickSign, Edit, View, Sign. Case-sensitive
            epaSiteId (Str): EPA Site ID
            manifestTrackingNumber (str): Manifest tracking number (optional)
            filter (list): List of MTNs (optional)
            
        Returns:
            dict: object containing link to UI
        """
        link = requests.post(self.base_url + '/api/v1/links/emanifest',
                             headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                      'Authorization': 'Bearer ' + self.token},
                             data=json.dumps(dict(**kwargs)))
        if link.ok:
            return link.json()
        else:
            print('Error: ' + str(link.json()['errors'][0]['message']))

    def CMELookup(self, activity_location, agency_code, nrr_flag=True):
        """
        Retrieve all lookups for specific activity location and agency code, including staff, focus area and sub-organization
        
        Parameters:
            activityLocation (str): Two-letter US postal state code
            agencyCode (str): One-letter code. B (State Contractor/Grantee), C (EPA Contractor/Grantee), E (EPA), L (Local), N (Native American), S (State), 
                                                T (State-Initiated Oversight/Observation/Training Actions), X (EPA-Initiated Oversight/Observation/Training Actions),
                                                J (Joint State), P (Joint EPA)
            nrrFlag (boolean): True/False if Non-Financial Record Review
        
        Returns:
            dict: object containing CME lookups
        """
        lookup = requests.get(
            self.base_url + '/api/v1/state/cme/evaluation/lookups/' + activity_location + '/' + agency_code + '/' + str(
                nrr_flag),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                     'Authorization': 'Bearer ' + self.token})
        if lookup.ok:
            return lookup.json()
        else:
            print('Error: ' + str(lookup.json()['message']))

    def CMEIndicators(self):
        """
        Retrieve all evaluation indicators
        
        Parameters:
            none
        
        Returns:
            dict: object containing all evaluation indicators
        """
        indic = requests.get(self.base_url + '/api/v1/state/cme/evaluation/evaluation-indicators',
                             headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                      'Authorization': 'Bearer ' + self.token})
        if indic.ok:
            return indic.json()
        else:
            print('Error: ' + str(indic.json()['message']))

    def CMETypes(self):
        """
        Retrieve all evaluation types
        
        Parameters:
            none
        
        Returns:
            dict: object containing all evaluation types
        """
        types = requests.get(self.base_url + '/api/v1/state/cme/evaluation/evaluation-types',
                             headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                      'Authorization': 'Bearer ' + self.token})
        if types.ok:
            return types.json()
        else:
            print('Error: ' + str(types.json()['message']))

    def GetAttachmentsReg(self, mtn):
        """
        Retrieve e-Manifest details as json with attachments matching provided Manifest Tracking Number (MTN)
        
        Parameters:
            mtn (str): Manifest tracking number
        
        Returns:
            json: Downloaded file containing e-Manifest details for given MTN
            attachments: PDF and HTML files containing additional manifest information (such as scans or electronic copies) for the given MTN
              message of success or failure
        """
        attach = requests.get(self.base_url + '/api/v1/state/emanifest/manifest/' + mtn + '/attachments',
                              headers={'Accept': 'multipart/mixed', 'Authorization': 'Bearer ' + self.token},
                              stream=True)
        if attach.ok:
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
        
        Parameters:
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
        response_mtn = requests.post(self.base_url + '/api/v1/state/emanifest/search',
                                     headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                              'Authorization': 'Bearer ' + self.token},
                                     data=json.dumps(dict(**kwargs)))
        if response_mtn.ok:
            return response_mtn.json()
        else:
            print('Error: ' + str(response_mtn.json()['message']))

    def GetCorrectionDetailsReg(self, mtn):
        """
        Retrieve information about all manifest correction versions by manifest tracking number (MTN)
        
        Parameters:
            mtn (str): Manifest tracking number
            
        Returns:
            dict: object containing correction details for given MTN
        """
        correct = requests.get(self.base_url + '/api/v1/state/emanifest/manifest/correction-details/' + mtn,
                               headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if correct.ok:
            return correct.json()
        else:
            print('Error: ' + str(correct.json()['message']))

    def GetCorrectionVersionReg(self, **kwargs):
        """
        Retrieve details of manifest correction version based on all or some of the provided search criteria

        Parameters:
            manifestTrackingNumber (str): Manifest tracking number. Required
            status (str): Manifest status (Signed, Corrected, UnderCorrection). Case-sensitive
            ppcStatus (str): EPA Paper Processing Center Status (PendingDataEntry, DataQaCompleted). Case-sensitive
            versionNumber (str): Manifest verion number
            
        Returns:
            dict: object containing correction details
        """
        cvd = requests.post(self.base_url + '/api/v1/state/emanifest/manifest/correction-version',
                            headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                     'Authorization': 'Bearer ' + self.token},
                            data=json.dumps(dict(**kwargs)))
        if cvd.ok:
            return cvd.json()
        else:
            print('Error: ' + str(cvd.json()['message']))

    def GetMTNBySiteReg(self, site_id):
        """
        Retrieve manifest tracking numbers for a given Site ID
        
        Parameters:
            site_id (str): EPA Site ID
        
        Returns:
            dict: object containing manifest tracking numbers for this site
        """
        site_mtn = requests.get(self.base_url + '/api/v1/state/emanifest/manifest-tracking-numbers/' + site_id,
                                headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if site_mtn.ok:
            return site_mtn.json()
        else:
            print('Error: ' + str(site_mtn.json()['message']))

    def GetManByMTNReg(self, mtn):
        """
        Retrieve e-Manifest details matching provided Manifest Tracking Number (MTN)
        
        Parameters:
            mtn (str): Manifest tracking number
        
        Returns:
            dict: object containing e-Manifest details
        """
        eman = requests.get(self.base_url + '/api/v1/state/emanifest/manifest/' + mtn,
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if eman.ok:
            return eman.json()
        else:
            print('Error: ' + str(eman.json()['message']))

    def GetSitesReg(self, state_code, site_type):
        """
        Retrieve site ids for provided criteria
        
        Parameters:
            state_code (str): Two-letter US postal state code
            site_type (str): Site type (Generator, Tsdf, Transporter, Broker). Case-sensitive
        
        Returns:
            dict: object containing site ID numbers
        """
        sites = requests.get(self.base_url + '/api/v1/state/emanifest/site-ids/' + state_code + '/' + site_type,
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if sites.ok:
            return sites.json()
        else:
            print('Error: ' + str(sites.json()['message']))

    def GetHandler(self, handler_id, details=False):
        """
        Retrieve a list of handler source records (and optional details) for a specific handler ID
        
        Parameters:
            handler_id (str): EPA Site ID number
            details (boolean): True/false to request additional details. Optional; defaults to False
            
        Returns:
            dict: object containing handler source records (and optional details)
        """
        handler = requests.get(self.base_url + '/api/v1/state/handler/sources/' + handler_id + '/' + str(details),
                               headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + self.token})
        if handler.ok:
            return handler.json()
        else:
            print('Error: ' + str(handler.json()['message']))

    def RCRAUserAuth(self, user_id, password):
        """
        Authenticates RCRAInfo V6 regulatory users
        
        Parameters:
            user_id (str): RCRAInfo V6 user ID
            password (str): RCRAInfo V6 user password
            
        Returns:
            dict: object containing RCRAInfo V6 Regulatory user validation
        """
        rcra_user = requests.post(self.base_url + '/api/v1/state/user/auth',
                                  headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                           'Authorization': 'Bearer ' + self.token},
                                  data=json.dumps({'userId': user_id, 'password': password}))
        if rcra_user.ok:
            return rcra_user.json()
        else:
            print('Error: ' + str(rcra_user.json()['message']))
