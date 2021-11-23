import getpass as gp
import pandas as pd
import requests
import json
import zipfile
import io
from requests_toolbelt.multipart import decoder, encoder

def eManAuth(api_id, api_key, env):
    '''Requests the user's RCRAInfo Swagger API ID, key, and desired environment (dev, sandbox, preprod, prod) for the session. Performs authentication and returns status'''
    global token, base_url
    urls = {
        'dev': 'https://rcrainfodev.com/rcrainfo/rest',
        'sandbox' : 'https://sandbox.rcrainfodev.net/rcrainfo/rest/',
        'preprod' : 'https://rcrainfopreprod.epa.gov/rcrainfo/rest/',
        'prod' : 'https://rcrainfo.epa.gov/rcrainfoprod/rest/'
    }
    base_url = urls[env]
    r = requests.get(base_url+'/api/v1/auth/'+api_id+'/'+api_key)
    token = r.json()['token']
    if r.status_code == 200:
        print('Authentication successful.')
    else:
        print('Error: '+ str(r.status_code))

def GetHazardClasses():
    '''Retrieve DOT Hazard Classes'''
    hazclass = requests.get(base_url+'/api/v1/emanifest/lookup/hazard-classes', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if hazclass.status_code == 200:
        return pd.DataFrame(hazclass.json()).rename(columns={0:'HazClass'})
    else:
        print('Error: '+ str(hazclass.json()['message']))
        
def GetPackingGroups():
    '''Retrieve DOT Packing Groups'''
    packgroups = requests.get(base_url+'/api/v1/emanifest/lookup/packing-groups', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if packgroups.status_code == 200:
        return pd.DataFrame(packgroups.json()).rename(columns={0:'Pack Groups'})
    else:
        print('Error: '+ str(packgroups.json()['message']))
        
def GetHazClass_SN_ID(ShipName, ID_Num):
    '''Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number. ShipName is case sensitive (e.g. Hydrochloric acid)'''
    hazclass_sn_id = requests.get(base_url+'/api/v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/'+ShipName+'/'+ID_Num, 
                                  headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if hazclass_sn_id.status_code == 200:
        return pd.DataFrame(hazclass_sn_id.json()).rename(columns={0:'HazClass'})
    else:
        print('Error: '+ str(hazclass_sn_id.json()['message']))

def GetPackGroups_SN_ID(ShipName, ID_Num):
    '''Retrieve DOT Packing Groups by DOT Proper Shipping name and ID Number. ShipName is case sensitive (e.g. Hydrochloric acid)'''
    packgroup_sn_id = requests.get(base_url+'/api/v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/'+ShipName+'/'+ID_Num, 
                                  headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if packgroup_sn_id.status_code == 200:
        return pd.DataFrame(packgroup_sn_id.json()).rename(columns={0:'Pack Groups'})
    else:
        print('Error: '+ str(packgroup_sn_id.json()['message']))
        
def GetIDByShipName(ShipName):
    '''Retrieve DOT ID Numbers by DOT Proper Shipping name. ShipName is case sensitive (e.g. Hydrochloric acid)'''
    dotid_sn = requests.get(base_url+'/api/v1/emanifest/lookup/id-numbers-by-shipping-name/'+ShipName, 
                                  headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if dotid_sn.status_code == 200:
        return pd.DataFrame(dotid_sn.json()).rename(columns={0:'DOT ID'})
    else:
        print('Error: '+ str(dotid_sn.json()['message']))
        
def GetShipNameByID(ID_Num):
    '''Retrieve DOT Proper Shipping names by DOT IdDNumber'''
    dotsn_id = requests.get(base_url+'/api/v1/emanifest/lookup/proper-shipping-names-by-id-number/'+ID_Num, 
                                  headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if dotsn_id.status_code == 200:
        return pd.DataFrame(dotsn_id.json()).rename(columns={0:'DOT Name'})
    else:
        print('Error: '+ str(dotsn_id.json()['message']))
        
def GetTNSuffix():
    '''Retrieve Allowable Manifest Tracking Number Suffixes'''
    tns = requests.get(base_url+'/api/v1/emanifest/lookup/printed-tracking-number-suffixes', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if tns.status_code == 200:
        return pd.json_normalize(tns.json())
    else:
        print('Error: '+ str(tns.json()['message']))
        
def GetTNSuffixALL():
    '''Retrieve ALL Allowable Manifest Tracking Number Suffixes'''
    tnsALL = requests.get(base_url+'/api/v1/emanifest/lookup/printed-tracking-number-suffixes-ALL', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if tnsALL.status_code == 200:
        return pd.json_normalize(tnsALL.json())
    else:
        print('Error: '+ str(tnsALL.json()['message']))
        
def GetContainerTypes():
    '''Retrieve Container Types'''
    contypes = requests.get(base_url+'/api/v1/emanifest/lookup/container-types', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if contypes.status_code == 200:
        return pd.json_normalize(contypes.json())
    else:
        print('Error: '+ str(contypes.json()['message']))
        
def GetQuantityUOM():
    '''Retrieve Quantity Units of Measure'''
    quom = requests.get(base_url+'/api/v1/emanifest/lookup/quantity-uom', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if quom.status_code == 200:
        return pd.json_normalize(quom.json())
    else:
        print('Error: '+ str(quom.json()['message']))
        
def GetLoadTypes():
    '''Retrieve PCB Load Types'''
    loadtypes = requests.get(base_url+'/api/v1/emanifest/lookup/load-types', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if loadtypes.status_code == 200:
        return pd.json_normalize(loadtypes.json())
    else:
        print('Error: '+ str(loadtypes.json()['message']))
        
def GetShippingNames():
    '''Retrieve DOT Proper Shipping Names'''
    shipnames = requests.get(base_url+'/api/v1/emanifest/lookup/proper-shipping-names', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if shipnames.status_code == 200:
        return pd.DataFrame(shipnames.json()).rename(columns={0:'DOT Name'})
    else:
        print('Error: '+ str(shipnames.json()['message']))
        
def GetIDNums():
    '''Retrieve DOT Shipping ID Numbers'''
    id_nums = requests.get(base_url+'/api/v1/emanifest/lookup/id-numbers', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if id_nums.status_code == 200:
        return pd.DataFrame(id_nums.json()).rename(columns={0:'DOT ID'})
    else:
        print('Error: '+ str(id_nums.json()['message']))
        
def GetDensityUOM():
    '''Retrieve Density Units of Measure'''
    global duom
    duom = requests.get(base_url+'/api/v1/lookup/density-uom', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if duom.status_code == 200:
        return pd.json_normalize(duom.json())
    else:
        print('Error: '+ str(duom.json()['message']))
        
def GetFormCodes():
    '''Retrieve Form Codes'''
    global formcodes
    formcodes = requests.get(base_url+'/api/v1/lookup/form-codes', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if formcodes.status_code == 200:
        return pd.json_normalize(formcodes.json())
    else:
        print('Error: '+ str(formcodes.json()['message']))
        
def GetSourceCodes():
    '''Retrieve Source Codes'''
    sourcecodes = requests.get(base_url+'/api/v1/lookup/source-codes', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if sourcecodes.status_code == 200:
        return pd.json_normalize(sourcecodes.json())
    else:
        print('Error: '+ str(sourcecodes.json()['message']))
        
def GetStateWasteCodes(state_code):
    '''Retrieve State Waste Codes'''
    swcodes = requests.get(base_url+'/api/v1/lookup/state-waste-codes/'+state_code, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if swcodes.status_code == 200:
        return pd.json_normalize(swcodes.json())
    else:
        print('Error: '+ str(swcodes.json()['message']))
        
def GetFedWasteCodes():
    '''Retrieve Federal Waste Codes'''
    fedcodes = requests.get(base_url+'/api/v1/lookup/federal-waste-codes', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if fedcodes.status_code == 200:
        return pd.json_normalize(fedcodes.json())
    else:
        print('Error: '+ str(fedcodes.json()['message']))
        
def GetManMethodCodes():
    '''Retrieve Management Method Codes'''
    mmcodes = requests.get(base_url+'/api/v1/lookup/management-method-codes', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if mmcodes.status_code == 200:
        return pd.json_normalize(mmcodes.json())
    else:
        print('Error: '+ str(mmcodes.json()['message']))
        
def GetWasteMinCodes():
    '''Retrieve Waste Minimization Codes'''
    wmcodes = requests.get(base_url+'/api/v1/lookup/waste-minimization-codes', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if wmcodes.status_code == 200:
        return pd.json_normalize(wmcodes.json())
    else:
        print('Error: '+ str(wmcodes.json()['message']))
        
def GetPortsOfEntry():
    '''Retrieve Ports of Entry'''
    poe = requests.get(base_url+'/api/v1/lookup/ports-of-entry', headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if poe.status_code == 200:
        return pd.json_normalize(poe.json())
    else:
        print('Error: '+ str(poe.json()['message']))
        
def GetSiteDetails(SiteID):
    '''Retrieve site details for a given Site ID'''
    details = requests.get(base_url+'/api/v1/site-details/'+SiteID, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if details.status_code == 200:
        return details.json()
    else:
        print('Error: '+ str(details.json()['message']))
        
def CheckSiteExists(SiteID):
    '''Check if provided Site ID exists'''
    exists = requests.get(base_url+'/api/v1/site-exists/'+SiteID, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if exists.status_code == 200:
        return exists.json()['result']
    else:
        print('Error: '+ str(exists.json()['message']))
        
def SiteSearch(**kwargs):
    '''Search for sites with the following parameters: epaSiteId, name, streetNumber, address1, city, state, sip, siteType, pageNumber'''
    sitesearch = requests.post(base_url+'/api/v1/site-search', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if sitesearch.status_code == 200:
        return sitesearch.json()
    else:
        print('Error: '+ str(sitesearch.json()['message']))
        
def GetBillingHistory(billingAccount, startMonthYear, endMonthYear):
    '''Retrieve billing history for a given billing account ID. Requires the following parameters: 
    billingAccount (EPA Site ID), startMonthYear (as MM/YYYY), endMonthYear (as MM/YYYY)'''
    billh = requests.post(base_url+'/api/v1/emanifest/billing/bill-history', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(
                            {
                                'billingAccount' : billingAccount,
                                'startMonthYear' : startMonthYear,
                                'endMonthYear' : endMonthYear
                            }
                            ))  
    if billh.status_code == 200:
        return pd.json_normalize(billh.json(), 'billsInfo').assign(billingAccount = billingAccount, startMonthYear = startMonthYear, endMonthYear = endMonthYear)
    else:
        print('Error: '+ str(billh.json()['message']))
        
def GetBill(**kwargs):
    '''Retrieve bill information for a given bill ID and account ID. Requires the following parameters:
    billId, billingAccount (EPA Site ID), monthYear (as MM/YYYY, optional if billId is provided)'''
    bill = requests.post(base_url+'/api/v1/emanifest/billing/bill', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if bill.status_code == 200:
        return bill.json()
    else:
        print('Error: '+ str(bill.json()['message']))
        
def SearchBill(**kwargs):
    '''Search for bills using the following criteria:
     billingAccount, billStatus, startDate (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ), endDate (yyyy-MM-dd'T'HH:mm:ssZ or yyyy-MM-dd'T'HH:mm:ss.SSSZ),
     amountChanged (boolean true|false), pageNumber (number greater than 0)'''
    bsearch = requests.post(base_url+'/api/v1/emanifest/billing/bill-search', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if bsearch.status_code == 200:
        return bsearch.json()
    else:
        print('Error: '+ str(bsearch.json()['message']))
        
def GetAttachments(ManifestTrackingNumber):
    '''Retrieve eManifest details as json with attachments matching provided Manifest Tracking Number'''
    attach = requests.get(base_url+'/api/v1/emanifest/manifest/'+ManifestTrackingNumber+'/attachments', 
                          headers = {'Accept' : 'multipart/mixed', 'Authorization' : 'Bearer '+token}, stream=True)
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
        print('Error: '+ str(attach.json()['message']))
        
def SearchMTN(**kwargs):
    '''Retrieve manifest tracking numbers based on provided search criteria. Requires some of the following parameters: 
    stateCode, siteId (EPA Site ID), status (Pending|Scheduled|InTransit|Received|ReadyForSignature|Signed|SignedComplete|UnderCorrection|Corrected),
    dateType (CertifiedDate|ReceivedDate|ShippedDate|UpdatedDate),siteType (Generator|Tsdf|Transporter|RejectionInfo_AlternateTsdf), startDate, endDate'''
    fmtn = requests.post(base_url+'/api/v1/emanifest/search', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if fmtn.status_code == 200:
        return pd.DataFrame(fmtn.json()).rename(columns={0:'manifestTrackingNumber'})
    else:
        print('Error: '+ str(fmtn.json()['message']))
        
def GetCorrectionDetails(MTN):
    '''Retrieve information about all manifest correction versions by manifest tracking number'''
    correct = requests.get(base_url+'/api/v1/emanifest/manifest/correction-details/'+MTN, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if correct.status_code == 200:
        return pd.json_normalize(correct.json(), 'emanifestVersions').assign(manifestTrackingNumber = MTN)
    else:
        print('Error: '+ str(correct.json()['message']))
        
def GetCorrectionVersion(**kwargs):
    '''Retrieve details of manifest correction version based on provided search criteria. Requires some of the following parameters: 
    manifestTrackingNumber (required), status (Signed|Corrected|UnderCorrection), ppcStatus (PendingDataEntry|DataQaCompleted), versionNumber'''
    cvd = requests.post(base_url+'/api/v1/emanifest/manifest/correction-version', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if cvd.status_code == 200:
        return cvd.json()
    else:
        print('Error: '+ str(cvd.json()['message']))
        
def GetMTNBySite(SiteID):
    '''Retrieve manifest tracking numbers for a given Site ID'''
    smtn = requests.get(base_url+'/api/v1/emanifest/manifest-tracking-numbers/'+SiteID, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if smtn.status_code == 200:
        return pd.DataFrame(smtn.json()).rename(columns={0:'manifestTrackingNumber'})
    else:
        print('Error: '+ str(smtn.json()['message']))
        
def GetManByMTN(MTN):
    '''Retrieve eManifest for a given manifest tracking number'''
    eman = requests.get(base_url+'/api/v1/emanifest/manifest/'+MTN, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if eman.status_code == 200:
        return eman.json()
    else:
        print('Error: '+ str(eman.json()['message']))
        
def GetSites(StateCode, SiteType):
    '''Retrieve site ids for provided state (code) and site type (i.e. Generator, TSDF, Transporter)'''
    sites = requests.get(base_url+'/api/v1/emanifest/site-ids/'+StateCode+'/'+SiteType, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if sites.status_code == 200:
        return pd.DataFrame(sites.json()).rename(columns={0:'SiteID'})
    else:
        print('Error: '+ str(sites.json()['message']))
        
def Correct(JSON, ZIP=None):
    '''Correct Manifest by providing eManifest JSON and optional Zip attachment'''
    if ZIP != None:
        m = encoder.MultipartEncoder(fields={
            "manifest" : (JSON, open(JSON, 'rb'), 'application/json'),
            "attachment" : (ZIP, open(ZIP, 'rb'), 'application/zip')
        })
    else:
        m = encoder.MultipartEncoder(fields={
            "manifest" : (JSON, open(JSON, 'rb'), 'application/json'),
        })
    correct = requests.put(base_url+'/api/v1/emanifest/manifest/correct', 
                         headers = {'Content-Type' : m.content_type, 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token}, 
                         data = m)
    print(correct.json())
        
def Revert(MTN):
    '''Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version'''
    revert = requests.get(base_url+'/api/v1/emanifest/manifest/revert/'+MTN, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    print(revert.json())
        
def GetCorrectionAttachments(**kwargs):
    '''Retrieve attachments of corrected manifests based on provided search criteria. Requires some of the following parameters: 
    manifestTrackingNumber (required), status (Signed|Corrected|UnderCorrection), ppcStatus (PendingDataEntry|DataQaCompleted), versionNumber'''
    cta = requests.post(base_url+'/api/v1/emanifest/manifest/correction-version/attachments', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
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
        print('Error: '+ str(cta.json()['message']))
        
def CheckMTNExists(MTN):
    '''Check if Manifest Tracking Number exists and return basic details'''
    checkmtn = requests.get(base_url+'/api/v1/emanifest/manifest/mtn-exists/'+MTN, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if checkmtn.status_code == 200:
        return pd.json_normalize(checkmtn.json())
    else:
        print('Error: '+ str(checkmtn.json()['message']))
        
def Update(JSON, ZIP=None):
    '''Update Manifest by providing eManifest JSON and optional Zip attachment'''
    if ZIP != None:
        m = encoder.MultipartEncoder(fields={
            "manifest" : (JSON, open(JSON, 'rb'), 'application/json'),
            "attachment" : (ZIP, open(ZIP, 'rb'), 'application/zip')
        })
    else:
        m = encoder.MultipartEncoder(fields={
            "manifest" : (JSON, open(JSON, 'rb'), 'application/json'),
        })
    update = requests.put(base_url+'/api/v1/emanifest/manifest/update', 
                         headers = {'Content-Type' : m.content_type, 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token}, 
                         data = m)
    print(update.json())
        
def Delete(MTN):
    '''Delete selected manifest'''
    delete = requests.delete(base_url+'/api/v1/emanifest/manifest/delete/'+MTN, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    print(delete.json())
        
def Save(JSON, ZIP=None):
    '''Save Manifest by providing eManifest JSON and optional Zip attachment'''
    if ZIP != None:
        m = encoder.MultipartEncoder(fields={
            "manifest" : (JSON, open(JSON, 'rb'), 'application/json'),
            "attachment" : (ZIP, open(ZIP, 'rb'), 'application/zip')
        })
    else:
        m = encoder.MultipartEncoder(fields={
            "manifest" : (JSON, open(JSON, 'rb'), 'application/json'),
        })
    save = requests.post(base_url+'/api/v1/emanifest/manifest/save', 
                         headers = {'Content-Type' : m.content_type, 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token}, 
                         data = m)
    print(save.json())
        
def GenerateUILink(**kwargs):
    '''Generate link to the UI of the eManifest module based on the following parameters: page, epaSiteId, manifestTrackingNumber, filter (takes list of MTNs)'''
    link = requests.post(base_url+'/api/v1/links/emanifest', 
                            headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if link.status_code == 200:
        return link.json()
    else:
        print('Error: '+ str(link.json()['errors'][0]['message']))
        
def CMELookup(activityLocation, agencyCode, nrrFlag=True):
    '''Retrieve all lookups for specific activity location and agency code, 
    including staff, focus area and sub-organization. Fields include activityLocation, agencyCode, and nrrFlag'''
    lookup = requests.get(base_url+'/api/v1/state/cme/evaluation/lookups/'+activityLocation+'/'+agencyCode+'/'+str(nrrFlag), 
                            headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})      
    if lookup.status_code == 200:
        return pd.DataFrame(lookup.json()['focusAreas'])
    else:
        print('Error: '+ str(lookup.json()['message']))
        
def CMEIndicators():
    '''Retrieve all evaluation indicators'''
    indic = requests.get(base_url+'/api/v1/state/cme/evaluation/evaluation-indicators', 
                            headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})      
    if indic.status_code == 200:
        return pd.DataFrame(indic.json())
    else:
        print('Error: '+ str(indic.json()['message']))
        
def CMETypes():
    '''Retrieve all evaluation types'''
    types = requests.get(base_url+'/api/v1/state/cme/evaluation/evaluation-types', 
                            headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})      
    if types.status_code == 200:
        return pd.DataFrame(types.json())
    else:
        print('Error: '+ str(types.json()['message']))
        
def GetAttachmentsReg(ManifestTrackingNumber):
    '''Retrieve eManifest details as json with attachments matching provided Manifest Tracking Number'''
    attach = requests.get(base_url+'/api/v1/state/emanifest/manifest/'+ManifestTrackingNumber+'/attachments', 
                          headers = {'Accept' : 'multipart/mixed', 'Authorization' : 'Bearer '+token}, stream=True)
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
        print('Error: '+ str(attach.json()['message']))
        
def SearchMTNReg(**kwargs):
    '''Retrieve manifest tracking numbers based on provided search criteria. Requires some of the following parameters: 
    stateCode, siteId (EPA Site ID), status (Pending|Scheduled|InTransit|Received|ReadyForSignature|Signed|SignedComplete|UnderCorrection|Corrected),
    dateType (CertifiedDate|ReceivedDate|ShippedDate|UpdatedDate),siteType (Generator|Tsdf|Transporter|RejectionInfo_AlternateTsdf), startDate, endDate'''
    fmtn = requests.post(base_url+'/api/v1/state/emanifest/search', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if fmtn.status_code == 200:
        return pd.DataFrame(fmtn.json()).rename(columns={0:'manifestTrackingNumber'})
    else:
        print('Error: '+ str(fmtn.json()['message']))
        
def GetCorrectionDetailsReg(MTN):
    '''Retrieve information about all manifest correction versions by manifest tracking number'''
    correct = requests.get(base_url+'/api/v1/state/emanifest/manifest/correction-details/'+MTN, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if correct.status_code == 200:
        return pd.json_normalize(correct.json(), 'emanifestVersions').assign(manifestTrackingNumber = MTN)
    else:
        print('Error: '+ str(correct.json()['message']))
        
def GetCorrectionVersionReg(**kwargs):
    '''Retrieve details of manifest correction version based on provided search criteria. Requires some of the following parameters: 
    manifestTrackingNumber (required), status (Signed|Corrected|UnderCorrection), ppcStatus (PendingDataEntry|DataQaCompleted), versionNumber'''
    cvd = requests.post(base_url+'/api/v1/state/emanifest/manifest/correction-version', 
                            headers = {'Content-Type' : 'text/plain', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps(dict(**kwargs)))  
    if cvd.status_code == 200:
        return cvd.json()
    else:
        print('Error: '+ str(cvd.json()['message']))
        
def GetMTNBySiteReg(SiteID):
    '''Retrieve manifest tracking numbers for a given Site ID'''
    smtn = requests.get(base_url+'/api/v1/state/emanifest/manifest-tracking-numbers/'+SiteID, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if smtn.status_code == 200:
        return pd.DataFrame(smtn.json()).rename(columns={0:'SiteID'})
    else:
        print('Error: '+ str(smtn.json()['message']))
        
def GetManByMTNReg(MTN):
    '''Retrieve eManifest for a given manifest tracking number'''
    eman = requests.get(base_url+'/api/v1/state/emanifest/manifest/'+MTN, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if eman.status_code == 200:
        return eman.json()
    else:
        print('Error: '+ str(eman.json()['message']))
        
def GetSitesReg(StateCode, SiteType):
    '''Retrieve site ids for provided state (code) and site type (i.e. Generator, TSDF, Transporter)'''
    sites = requests.get(base_url+'/api/v1/state/emanifest/site-ids/'+StateCode+'/'+SiteType, headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if sites.status_code == 200:
        return pd.DataFrame(sites.json()).rename(columns={0:'Site ID'})
    else:
        print('Error: '+ str(sites.json()['message']))
        
def GetHandler(handler_id, details=False):
    '''Retrieve a list of handler source records (and optionally more details) for specific handler id'''
    handler = requests.get(base_url+'/api/v1/state/handler/sources/'+handler_id+'/'+str(details), headers = {'Accept' : 'application/json', 'Authorization' : 'Bearer '+token})
    if handler.status_code == 200:
        return pd.json_normalize(handler.json())
    else:
        print('Error: '+ str(handler.json()['message']))
        
def RCRAUserAuth(user_id, password):
    '''Authenticates RCRAInfo V6 Users'''
    rcrauser = requests.post(base_url+'/api/v1/state/user/auth', 
                            headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json', 'Authorization' : 'Bearer '+token},
                            data = json.dumps({'userId': user_id, 'password' : password}))
    if rcrauser.status_code == 200:
        return pd.json_normalize(rcrauser.json())
    else:
        print('Error: '+ str(rcrauser.json()['message']))