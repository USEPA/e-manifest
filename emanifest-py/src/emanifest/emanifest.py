"""
e-Manifest library for using the e-Manifest API
see https://github.com/USEPA/e-manifest
@author William Nicholas
"""
import pandas as pd
import requests
import json
import zipfile
import io
from requests_toolbelt.multipart import decoder, encoder

TOKEN = ""
BASE_URL = ""
DEN_UOM = ""
FORM_CODES = ""


def eManAuth(api_id, api_key, env):
    """Requests the user's RCRAInfo Swagger API ID, key, and desired environment (dev, sandbox, preprod,
    prod) for the session. Performs authentication and returns status """
    global TOKEN, BASE_URL
    urls = {
        'dev': 'https://rcrainfodev.com/rcrainfo/rest',
        'sandbox': 'https://sandbox.rcrainfodev.net/rcrainfo/rest/',
        'preprod': 'https://rcrainfopreprod.epa.gov/rcrainfo/rest/',
        'prod': 'https://rcrainfo.epa.gov/rcrainfoprod/rest/'
    }
    BASE_URL = urls[env]
    r = requests.get(BASE_URL + '/api/v1/auth/' + api_id + '/' + api_key)
    TOKEN = r.json()['TOKEN']
    if r.status_code == 200:
        print('Authentication successful.')
    else:
        print('Error: ' + str(r.status_code))


def GetHazardClasses():
    """Retrieve DOT Hazard Classes"""
    haz_class = requests.get(BASE_URL + '/api/v1/emanifest/lookup/hazard-classes',
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if haz_class.status_code == 200:
        return pd.DataFrame(haz_class.json()).rename(columns={0: 'HazClass'})
    else:
        print('Error: ' + str(haz_class.json()['message']))


def GetPackingGroups():
    """Retrieve DOT Packing Groups"""
    pack_groups = requests.get(BASE_URL + '/api/v1/emanifest/lookup/packing-groups',
                               headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if pack_groups.status_code == 200:
        return pd.DataFrame(pack_groups.json()).rename(columns={0: 'Pack Groups'})
    else:
        print('Error: ' + str(pack_groups.json()['message']))


def GetHazClass_SN_ID(ship_name, id_num):
    """Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number. ShipName is case sensitive (e.g.
    Hydrochloric acid) """
    haz_class_sn_id = requests.get(
        BASE_URL + '/api/v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/' + ship_name + '/' + id_num,
        headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if haz_class_sn_id.status_code == 200:
        return pd.DataFrame(haz_class_sn_id.json()).rename(columns={0: 'HazClass'})
    else:
        print('Error: ' + str(haz_class_sn_id.json()['message']))


def GetPackGroups_SN_ID(ship_name, id_num):
    """Retrieve DOT Packing Groups by DOT Proper Shipping name and ID Number. ShipName is case sensitive (e.g.
    Hydrochloric acid) """
    pack_group_sn_id = requests.get(
        BASE_URL + '/api/v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/' + ship_name + '/' + id_num,
        headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if pack_group_sn_id.status_code == 200:
        return pd.DataFrame(pack_group_sn_id.json()).rename(columns={0: 'Pack Groups'})
    else:
        print('Error: ' + str(pack_group_sn_id.json()['message']))


def GetIDByShipName(ship_name):
    """Retrieve DOT ID Numbers by DOT Proper Shipping name. ShipName is case sensitive (e.g. Hydrochloric acid)"""
    dot_id_sn = requests.get(BASE_URL + '/api/v1/emanifest/lookup/id-numbers-by-shipping-name/' + ship_name,
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if dot_id_sn.status_code == 200:
        return pd.DataFrame(dot_id_sn.json()).rename(columns={0: 'DOT ID'})
    else:
        print('Error: ' + str(dot_id_sn.json()['message']))


def GetShipNameByID(id_num):
    """Retrieve DOT Proper Shipping names by DOT IdDNumber"""
    dot_sn_id = requests.get(BASE_URL + '/api/v1/emanifest/lookup/proper-shipping-names-by-id-number/' + id_num,
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if dot_sn_id.status_code == 200:
        return pd.DataFrame(dot_sn_id.json()).rename(columns={0: 'DOT Name'})
    else:
        print('Error: ' + str(dot_sn_id.json()['message']))


def GetTNSuffix():
    """Retrieve Allowable Manifest Tracking Number Suffixes"""
    tns = requests.get(BASE_URL + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes',
                       headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if tns.status_code == 200:
        return pd.json_normalize(tns.json())
    else:
        print('Error: ' + str(tns.json()['message']))


def GetTNSuffixALL():
    """Retrieve ALL Allowable Manifest Tracking Number Suffixes"""
    tns_all = requests.get(BASE_URL + '/api/v1/emanifest/lookup/printed-tracking-number-suffixes-ALL',
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if tns_all.status_code == 200:
        return pd.json_normalize(tns_all.json())
    else:
        print('Error: ' + str(tns_all.json()['message']))


def GetContainerTypes():
    """Retrieve Container Types"""
    con_types = requests.get(BASE_URL + '/api/v1/emanifest/lookup/container-types',
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if con_types.status_code == 200:
        return pd.json_normalize(con_types.json())
    else:
        print('Error: ' + str(con_types.json()['message']))


def GetQuantityUOM():
    """Retrieve Quantity Units of Measure"""
    quantity_uom = requests.get(BASE_URL + '/api/v1/emanifest/lookup/quantity-uom',
                                headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if quantity_uom.status_code == 200:
        return pd.json_normalize(quantity_uom.json())
    else:
        print('Error: ' + str(quantity_uom.json()['message']))


def GetLoadTypes():
    """Retrieve PCB Load Types"""
    load_types = requests.get(BASE_URL + '/api/v1/emanifest/lookup/load-types',
                              headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if load_types.status_code == 200:
        return pd.json_normalize(load_types.json())
    else:
        print('Error: ' + str(load_types.json()['message']))


def GetShippingNames():
    """Retrieve DOT Proper Shipping Names"""
    ship_names = requests.get(BASE_URL + '/api/v1/emanifest/lookup/proper-shipping-names',
                              headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if ship_names.status_code == 200:
        return pd.DataFrame(ship_names.json()).rename(columns={0: 'DOT Name'})
    else:
        print('Error: ' + str(ship_names.json()['message']))


def GetIDNums():
    """Retrieve DOT Shipping ID Numbers"""
    id_nums = requests.get(BASE_URL + '/api/v1/emanifest/lookup/id-numbers',
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if id_nums.status_code == 200:
        return pd.DataFrame(id_nums.json()).rename(columns={0: 'DOT ID'})
    else:
        print('Error: ' + str(id_nums.json()['message']))


def GetDensityUOM():
    """Retrieve Density Units of Measure"""
    global DEN_UOM
    DEN_UOM = requests.get(BASE_URL + '/api/v1/lookup/density-uom',
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if DEN_UOM.status_code == 200:
        return pd.json_normalize(DEN_UOM.json())
    else:
        print('Error: ' + str(DEN_UOM.json()['message']))


def GetFormCodes():
    """Retrieve Form Codes"""
    global FORM_CODES
    FORM_CODES = requests.get(BASE_URL + '/api/v1/lookup/form-codes',
                              headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if FORM_CODES.status_code == 200:
        return pd.json_normalize(FORM_CODES.json())
    else:
        print('Error: ' + str(FORM_CODES.json()['message']))


def GetSourceCodes():
    """Retrieve Source Codes"""
    source_codes = requests.get(BASE_URL + '/api/v1/lookup/source-codes',
                                headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if source_codes.status_code == 200:
        return pd.json_normalize(source_codes.json())
    else:
        print('Error: ' + str(source_codes.json()['message']))


def GetStateWasteCodes(state_code):
    """Retrieve State Waste Codes"""
    sw_codes = requests.get(BASE_URL + '/api/v1/lookup/state-waste-codes/' + state_code,
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if sw_codes.status_code == 200:
        return pd.json_normalize(sw_codes.json())
    else:
        print('Error: ' + str(sw_codes.json()['message']))


def GetFedWasteCodes():
    """Retrieve Federal Waste Codes"""
    fed_codes = requests.get(BASE_URL + '/api/v1/lookup/federal-waste-codes',
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if fed_codes.status_code == 200:
        return pd.json_normalize(fed_codes.json())
    else:
        print('Error: ' + str(fed_codes.json()['message']))


def GetManMethodCodes():
    """Retrieve Management Method Codes"""
    mm_codes = requests.get(BASE_URL + '/api/v1/lookup/management-method-codes',
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if mm_codes.status_code == 200:
        return pd.json_normalize(mm_codes.json())
    else:
        print('Error: ' + str(mm_codes.json()['message']))


def GetWasteMinCodes():
    """Retrieve Waste Minimization Codes"""
    wm_codes = requests.get(BASE_URL + '/api/v1/lookup/waste-minimization-codes',
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if wm_codes.status_code == 200:
        return pd.json_normalize(wm_codes.json())
    else:
        print('Error: ' + str(wm_codes.json()['message']))


def GetPortsOfEntry():
    """Retrieve Ports of Entry"""
    poe = requests.get(BASE_URL + '/api/v1/lookup/ports-of-entry',
                       headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if poe.status_code == 200:
        return pd.json_normalize(poe.json())
    else:
        print('Error: ' + str(poe.json()['message']))


def GetSiteDetails(site_id):
    """Retrieve site details for a given Site ID"""
    details = requests.get(BASE_URL + '/api/v1/site-details/' + site_id,
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if details.status_code == 200:
        return details.json()
    else:
        print('Error: ' + str(details.json()['message']))


def CheckSiteExists(site_id):
    """Check if provided Site ID exists"""
    exists = requests.get(BASE_URL + '/api/v1/site-exists/' + site_id,
                          headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if exists.status_code == 200:
        return exists.json()['result']
    else:
        print('Error: ' + str(exists.json()['message']))


def SiteSearch(**kwargs):
    """Search for sites with the following parameters: epaSiteId, name, streetNumber, address1, city, state, sip,
    siteType, pageNumber """
    site_search = requests.post(BASE_URL + '/api/v1/site-search',
                                headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                         'Authorization': 'Bearer ' + TOKEN},
                                data=json.dumps(dict(**kwargs)))
    if site_search.status_code == 200:
        return site_search.json()
    else:
        print('Error: ' + str(site_search.json()['message']))


def GetBillingHistory(billing_account, start_month_year, end_month_year):
    """Retrieve billing history for a given billing account ID. Requires the following parameters:
    billingAccount (EPA Site ID), startMonthYear (as MM/YYYY), endMonthYear (as MM/YYYY)"""
    bill_history = requests.post(BASE_URL + '/api/v1/emanifest/billing/bill-history',
                                 headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                          'Authorization': 'Bearer ' + TOKEN},
                                 data=json.dumps(
                                     {
                                         'billingAccount': billing_account,
                                         'startMonthYear': start_month_year,
                                         'endMonthYear': end_month_year
                                     }
                                 ))
    if bill_history.status_code == 200:
        return pd.json_normalize(bill_history.json(), 'billsInfo').assign(billingAccount=billing_account,
                                                                          startMonthYear=start_month_year,
                                                                          endMonthYear=end_month_year)
    else:
        print('Error: ' + str(bill_history.json()['message']))


def GetBill(**kwargs):
    """Retrieve bill information for a given bill ID and account ID. Requires the following parameters:
    billId, billingAccount (EPA Site ID), monthYear (as MM/YYYY, optional if billId is provided)"""
    bill = requests.post(BASE_URL + '/api/v1/emanifest/billing/bill',
                         headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                  'Authorization': 'Bearer ' + TOKEN},
                         data=json.dumps(dict(**kwargs)))
    if bill.status_code == 200:
        return bill.json()
    else:
        print('Error: ' + str(bill.json()['message']))


def SearchBill(**kwargs):
    """Search for bills using the following criteria:
     billingAccount, billStatus, startDate (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ),
     endDate (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ),
     amountChanged (boolean true|false), pageNumber (number greater than 0)"""
    bill_search = requests.post(BASE_URL + '/api/v1/emanifest/billing/bill-search',
                                headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                         'Authorization': 'Bearer ' + TOKEN},
                                data=json.dumps(dict(**kwargs)))
    if bill_search.status_code == 200:
        return bill_search.json()
    else:
        print('Error: ' + str(bill_search.json()['message']))


def GetAttachments(mtn):
    """Retrieve eManifest details as json with attachments matching provided Manifest Tracking Number"""
    attach = requests.get(BASE_URL + '/api/v1/emanifest/manifest/' + mtn + '/attachments',
                          headers={'Accept': 'multipart/mixed', 'Authorization': 'Bearer ' + TOKEN}, stream=True)
    if attach.status_code == 200:
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


def SearchMTN(**kwargs):
    """Retrieve manifest tracking numbers based on provided search criteria. Requires some of the following parameters:
    stateCode, siteId (EPA Site ID),
    status (Pending|Scheduled|InTransit|Received|ReadyForSignature|Signed|SignedComplete|UnderCorrection|Corrected),
    dateType (CertifiedDate|ReceivedDate|ShippedDate|UpdatedDate),
    siteType (Generator|Tsdf|Transporter|RejectionInfo_AlternateTsdf), startDate, endDate"""
    search_mtn_resp = requests.post(BASE_URL + '/api/v1/emanifest/search',
                                    headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                             'Authorization': 'Bearer ' + TOKEN},
                                    data=json.dumps(dict(**kwargs)))
    if search_mtn_resp.status_code == 200:
        return pd.DataFrame(search_mtn_resp.json()).rename(columns={0: 'manifestTrackingNumber'})
    else:
        print('Error: ' + str(search_mtn_resp.json()['message']))


def GetCorrectionDetails(mtn):
    """Retrieve information about all manifest correction versions by manifest tracking number"""
    correct = requests.get(BASE_URL + '/api/v1/emanifest/manifest/correction-details/' + mtn,
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if correct.status_code == 200:
        return pd.json_normalize(correct.json(), 'emanifestVersions').assign(manifestTrackingNumber=mtn)
    else:
        print('Error: ' + str(correct.json()['message']))


def GetCorrectionVersion(**kwargs):
    """Retrieve details of manifest correction version based on provided search criteria.
    Requires some of the following parameters:
    manifestTrackingNumber (required), status (Signed|Corrected|UnderCorrection),
    ppcStatus (PendingDataEntry|DataQaCompleted), versionNumber"""
    cvd = requests.post(BASE_URL + '/api/v1/emanifest/manifest/correction-version',
                        headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                 'Authorization': 'Bearer ' + TOKEN},
                        data=json.dumps(dict(**kwargs)))
    if cvd.status_code == 200:
        return cvd.json()
    else:
        print('Error: ' + str(cvd.json()['message']))


def GetMTNBySite(site_id):
    """Retrieve manifest tracking numbers for a given Site ID"""
    site_mtn = requests.get(BASE_URL + '/api/v1/emanifest/manifest-tracking-numbers/' + site_id,
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if site_mtn.status_code == 200:
        return pd.DataFrame(site_mtn.json()).rename(columns={0: 'manifestTrackingNumber'})
    else:
        print('Error: ' + str(site_mtn.json()['message']))


def GetManByMTN(mtn):
    """Retrieve eManifest for a given manifest tracking number"""
    eman = requests.get(BASE_URL + '/api/v1/emanifest/manifest/' + mtn,
                        headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if eman.status_code == 200:
        return eman.json()
    else:
        print('Error: ' + str(eman.json()['message']))


def GetSites(state_code, site_type):
    """Retrieve site ids for provided state (code) and site type (i.e. Generator, TSDF, Transporter)"""
    sites = requests.get(BASE_URL + '/api/v1/emanifest/site-ids/' + state_code + '/' + site_type,
                         headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if sites.status_code == 200:
        return pd.DataFrame(sites.json()).rename(columns={0: 'SiteID'})
    else:
        print('Error: ' + str(sites.json()['message']))


def Correct(manifest_json, zip_file=None):
    """Correct Manifest by providing eManifest JSON and optional Zip attachment"""
    if zip_file is not None:
        m = encoder.MultipartEncoder(fields={
            "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
            "attachment": (zip_file, open(zip_file, 'rb'), 'application/zip')
        })
    else:
        m = encoder.MultipartEncoder(fields={
            "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
        })
    correct = requests.put(BASE_URL + '/api/v1/emanifest/manifest/correct',
                           headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                    'Authorization': 'Bearer ' + TOKEN},
                           data=m)
    print(correct.json())


def Revert(mtn):
    """Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version"""
    revert = requests.get(BASE_URL + '/api/v1/emanifest/manifest/revert/' + mtn,
                          headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    print(revert.json())


def GetCorrectionAttachments(**kwargs):
    """Retrieve attachments of corrected manifests based on provided search criteria.
    Requires some of the following parameters:
    manifestTrackingNumber (required), status (Signed|Corrected|UnderCorrection),
    ppcStatus (PendingDataEntry|DataQaCompleted), versionNumber"""
    cta = requests.post(BASE_URL + '/api/v1/emanifest/manifest/correction-version/attachments',
                        headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                 'Authorization': 'Bearer ' + TOKEN},
                        data=json.dumps(dict(**kwargs)))
    if cta.status_code == 200:
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


def CheckMTNExists(mtn):
    """Check if Manifest Tracking Number exists and return basic details"""
    check_mtn = requests.get(BASE_URL + '/api/v1/emanifest/manifest/mtn-exists/' + mtn,
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if check_mtn.status_code == 200:
        return pd.json_normalize(check_mtn.json())
    else:
        print('Error: ' + str(check_mtn.json()['message']))


def Update(manifest_json, zip_file=None):
    """Update Manifest by providing eManifest JSON and optional Zip attachment"""
    if zip_file is not None:
        m = encoder.MultipartEncoder(fields={
            "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
            "attachment": (zip_file, open(zip_file, 'rb'), 'application/zip')
        })
    else:
        m = encoder.MultipartEncoder(fields={
            "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
        })
    update = requests.put(BASE_URL + '/api/v1/emanifest/manifest/update',
                          headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                   'Authorization': 'Bearer ' + TOKEN},
                          data=m)
    print(update.json())


def Delete(mtn):
    """Delete selected manifest"""
    delete = requests.delete(BASE_URL + '/api/v1/emanifest/manifest/delete/' + mtn,
                             headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    print(delete.json())


def Save(manifest_json, zip_file=None):
    """Save Manifest by providing eManifest JSON and optional Zip attachment"""
    if zip_file is not None:
        m = encoder.MultipartEncoder(fields={
            "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
            "attachment": (zip_file, open(zip_file, 'rb'), 'application/zip')
        })
    else:
        m = encoder.MultipartEncoder(fields={
            "manifest": (manifest_json, open(manifest_json, 'rb'), 'application/json'),
        })
    save = requests.post(BASE_URL + '/api/v1/emanifest/manifest/save',
                         headers={'Content-Type': m.content_type, 'Accept': 'application/json',
                                  'Authorization': 'Bearer ' + TOKEN},
                         data=m)
    print(save.json())


def GenerateUILink(**kwargs):
    """Generate link to the UI of the eManifest module based on the following parameters:
    page, epaSiteId, manifestTrackingNumber, filter (takes list of MTNs)"""
    link = requests.post(BASE_URL + '/api/v1/links/emanifest',
                         headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                  'Authorization': 'Bearer ' + TOKEN},
                         data=json.dumps(dict(**kwargs)))
    if link.status_code == 200:
        return link.json()
    else:
        print('Error: ' + str(link.json()['errors'][0]['message']))


def CMELookup(activity_location, agency_code, nrr_flag=True):
    """Retrieve all lookups for specific activity location and agency code,
    including staff, focus area and sub-organization. Fields include activityLocation, agencyCode, and nrrFlag"""
    lookup = requests.get(
        BASE_URL + '/api/v1/state/cme/evaluation/lookups/' + activity_location + '/' + agency_code + '/' + str(nrr_flag),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if lookup.status_code == 200:
        return pd.DataFrame(lookup.json()['focusAreas'])
    else:
        print('Error: ' + str(lookup.json()['message']))


def CMEIndicators():
    """Retrieve all evaluation indicators"""
    indic = requests.get(BASE_URL + '/api/v1/state/cme/evaluation/evaluation-indicators',
                         headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                  'Authorization': 'Bearer ' + TOKEN})
    if indic.status_code == 200:
        return pd.DataFrame(indic.json())
    else:
        print('Error: ' + str(indic.json()['message']))


def CMETypes():
    """Retrieve all evaluation types"""
    types = requests.get(BASE_URL + '/api/v1/state/cme/evaluation/evaluation-types',
                         headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                  'Authorization': 'Bearer ' + TOKEN})
    if types.status_code == 200:
        return pd.DataFrame(types.json())
    else:
        print('Error: ' + str(types.json()['message']))


def GetAttachmentsReg(mtn):
    """Retrieve eManifest details as json with attachments matching provided Manifest Tracking Number"""
    attach = requests.get(BASE_URL + '/api/v1/state/emanifest/manifest/' + mtn + '/attachments',
                          headers={'Accept': 'multipart/mixed', 'Authorization': 'Bearer ' + TOKEN}, stream=True)
    if attach.status_code == 200:
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


def SearchMTNReg(**kwargs):
    """Retrieve manifest tracking numbers based on provided search criteria. Requires some of the following parameters:
    stateCode, siteId (EPA Site ID),
    status (Pending|Scheduled|InTransit|Received|ReadyForSignature|Signed|SignedComplete|UnderCorrection|Corrected),
    dateType (CertifiedDate|ReceivedDate|ShippedDate|UpdatedDate),
    siteType (Generator|Tsdf|Transporter|RejectionInfo_AlternateTsdf), startDate, endDate"""
    fmtn = requests.post(BASE_URL + '/api/v1/state/emanifest/search',
                         headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                  'Authorization': 'Bearer ' + TOKEN},
                         data=json.dumps(dict(**kwargs)))
    if fmtn.status_code == 200:
        return pd.DataFrame(fmtn.json()).rename(columns={0: 'manifestTrackingNumber'})
    else:
        print('Error: ' + str(fmtn.json()['message']))


def GetCorrectionDetailsReg(mtn):
    """Retrieve information about all manifest correction versions by manifest tracking number"""
    correct = requests.get(BASE_URL + '/api/v1/state/emanifest/manifest/correction-details/' + mtn,
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if correct.status_code == 200:
        return pd.json_normalize(correct.json(), 'emanifestVersions').assign(manifestTrackingNumber=mtn)
    else:
        print('Error: ' + str(correct.json()['message']))


def GetCorrectionVersionReg(**kwargs):
    """Retrieve details of manifest correction version based on provided search criteria.
    Requires some of the following parameters:
    manifestTrackingNumber (required), status (Signed|Corrected|UnderCorrection),
    ppcStatus (PendingDataEntry|DataQaCompleted), versionNumber"""
    cvd = requests.post(BASE_URL + '/api/v1/state/emanifest/manifest/correction-version',
                        headers={'Content-Type': 'text/plain', 'Accept': 'application/json',
                                 'Authorization': 'Bearer ' + TOKEN},
                        data=json.dumps(dict(**kwargs)))
    if cvd.status_code == 200:
        return cvd.json()
    else:
        print('Error: ' + str(cvd.json()['message']))


def GetMTNBySiteReg(site_id):
    """Retrieve manifest tracking numbers for a given Site ID"""
    site_mtn = requests.get(BASE_URL + '/api/v1/state/emanifest/manifest-tracking-numbers/' + site_id,
                            headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if site_mtn.status_code == 200:
        return pd.DataFrame(site_mtn.json()).rename(columns={0: 'SiteID'})
    else:
        print('Error: ' + str(site_mtn.json()['message']))


def GetManByMTNReg(mtn):
    """Retrieve eManifest for a given manifest tracking number"""
    eman = requests.get(BASE_URL + '/api/v1/state/emanifest/manifest/' + mtn,
                        headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if eman.status_code == 200:
        return eman.json()
    else:
        print('Error: ' + str(eman.json()['message']))


def GetSitesReg(state_code, site_type):
    """Retrieve site ids for provided state (code) and site type (i.e. Generator, TSDF, Transporter)"""
    sites = requests.get(BASE_URL + '/api/v1/state/emanifest/site-ids/' + state_code + '/' + site_type,
                         headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if sites.status_code == 200:
        return pd.DataFrame(sites.json()).rename(columns={0: 'Site ID'})
    else:
        print('Error: ' + str(sites.json()['message']))


def GetHandler(handler_id, details=False):
    """Retrieve a list of handler source records (and optionally more details) for specific handler id"""
    handler = requests.get(BASE_URL + '/api/v1/state/handler/sources/' + handler_id + '/' + str(details),
                           headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + TOKEN})
    if handler.status_code == 200:
        return pd.json_normalize(handler.json())
    else:
        print('Error: ' + str(handler.json()['message']))


def RCRAUserAuth(user_id, password):
    """Authenticates RCRAInfo V6 Users"""
    rcra_user = requests.post(BASE_URL + '/api/v1/state/user/auth',
                              headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                       'Authorization': 'Bearer ' + TOKEN},
                              data=json.dumps({'userId': user_id, 'password': password}))
    if rcra_user.status_code == 200:
        return pd.json_normalize(rcra_user.json())
    else:
        print('Error: ' + str(rcra_user.json()['message']))
