import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  AuthResponse,
  BillGetParameters,
  BillHistoryParameters,
  BillSearchParameters,
  ManifestCorrectionParameters,
  ManifestExistsResponse,
  ManifestSearchParameters,
  PortOfEntry,
  QuickerSign,
  RcraCode,
  SiteSearchParameters,
  UserSearchParameters,
} from './types';

export const RCRAINFO_PREPROD = 'https://rcrainfopreprod.epa.gov/rcrainfo/rest/api';
export const RCRAINFO_PROD = 'https://rcrainfo.epa.gov/rcrainfo/rest/api';

export type RcrainfoEnv = typeof RCRAINFO_PREPROD | typeof RCRAINFO_PROD | string | undefined;

interface RcraClientConfig {
  apiBaseURL?: RcrainfoEnv;
  apiID?: string;
  apiKey?: string;
  authAuth?: Boolean;
}

export type RcraClientClass = typeof RcraClient;

/**
 * Creates a new RcraClient object with the given configuration for use with the RCRAInfo API.
 * @param apiBaseURL - The base URL for the RCRAInfo API. defaults to RCRAINFO_PREPROD.
 * @param apiID - The API ID for the RCRAInfo.
 * @param apiKey - The API key for the RCRAInfo.
 * @param authAuth - Automatically authenticate if necessary. By default, this is disabled.
 */
export const newClient = ({ apiBaseURL, apiID, apiKey, authAuth }: RcraClientConfig = {}) => {
  return new RcraClient(apiBaseURL, apiID, apiKey, authAuth);
};

/**
 * An HTTP client for the RCRAInfo/e-Manifest web services.
 * Under the hood, RcraClient uses the isomorphic Axios HTTP library, it can be used in a browser or node.js environment.
 * The client can be configured to automatically authenticate with the API on every request. By default, this is disabled.
 * @param apiBaseURL
 * @param apiID
 * @param apiKey
 *
 */
class RcraClient {
  private apiClient: AxiosInstance;
  env: RcrainfoEnv;
  private apiID?: string;
  private apiKey?: string;
  token?: string;
  expiration?: string;
  autoAuth?: Boolean;

  constructor(apiBaseURL: RcrainfoEnv, apiID?: string, apiKey?: string, autoAuth: Boolean = false) {
    this.env = apiBaseURL || RCRAINFO_PREPROD;
    this.apiID = apiID;
    this.apiKey = apiKey;
    this.autoAuth = autoAuth;
    this.apiClient = axios.create({
      baseURL: this.env,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    });

    this.apiClient.interceptors.request.use(async (config) => {
      // if the request is for auth, don't add the token
      if (config.url?.includes('auth')) {
        return config;
      }
      // if autoAuth is disabled return
      if (!this.autoAuth) {
        return config;
      }
      // If authAuth is enabled, check if we already have a token. If not, authenticate.
      if (!this.token) {
        // Check the RcraClient object for apiID and apiKey.
        if (!this.apiID || !this.apiKey) {
          // If there's no token and no apiID or apiKey, throw an error. We can't authenticate.
          throw new Error('Please add API ID and Key to authenticate.');
        }
        // If there's no token, but there is an apiID and apiKey, try to authenticate.
        await this.authenticate().catch((err) => {
          throw new Error(`Received an error while attempting to authenticate: ${err}`);
        });
      }
      config.headers.Authorization = `Bearer ${this.token}`;
      return config;
    });
  }

  authenticate = async (): Promise<AxiosResponse<AuthResponse>> => {
    return this.apiClient
      .get(`v1/auth/${this.apiID}/${this.apiKey}`)
      .then((resp: AxiosResponse<AuthResponse>) => {
        if (resp.status === 200) {
          this.token = `${resp.data.token}`;
        }
        return resp;
      })
      .catch((err: AxiosResponse) => {
        return err;
      });
  };

  /**
   * Returns true if the client has a valid token.
   */
  isAuthenticated = (): boolean => {
    return this.token !== undefined;
  };

  // RCRAInfo Lookup Services

  /**
   * Returns a list of all available state waste codes for a given state.
   * @param stateCode
   */
  public getStateWasteCodes = async (stateCode: string): Promise<AxiosResponse<RcraCode[]>> => {
    return this.apiClient.get(`v1/lookup/state-waste-codes/${stateCode}`);
  };

  /**
   * Returns a list of all available federal waste codes.
   */
  public getFederalWasteCodes = async (): Promise<AxiosResponse<RcraCode[]>> => {
    return this.apiClient.get('v1/lookup/federal-waste-codes');
  };

  /**
   * Returns a list of all available density units of measurement (UOM).
   */
  public getDensityUOMs = async (): Promise<AxiosResponse<RcraCode[]>> => {
    return this.apiClient.get('v1/lookup/density-uom');
  };

  /**
   * Returns a list of all available source codes (type of activity or process that produced the waste).
   */
  public getSourceCodes = async (): Promise<AxiosResponse<RcraCode[]>> => {
    return this.apiClient.get('v1/lookup/source-codes');
  };

  /**
   * Returns a list of all available management method codes (how the waste is managed).
   */
  public getManagementMethodCodes = async (): Promise<AxiosResponse<RcraCode[]>> => {
    return this.apiClient.get('v1/lookup/management-method-codes');
  };

  /**
   * Returns a list of all available waste minimization codes.
   */
  public getWasteMinimizationCodes = async (): Promise<AxiosResponse<RcraCode[]>> => {
    return this.apiClient.get('v1/lookup/waste-minimization-codes');
  };

  /**
   * Returns a list of all available ports of entry where the waste can enter/exit the United States.
   */
  public getPortsOfEntry = async (): Promise<AxiosResponse<PortOfEntry[]>> => {
    return this.apiClient.get('v1/lookup/ports-of-entry');
  };

  // e-Manifest Lookup Services

  /**
   * Returns a list of all available DOT Hazard classes.
   */
  public getHazardClasses = async (
    shippingName?: string,
    idNumber?: string,
  ): Promise<AxiosResponse<string[] | string>> => {
    if (shippingName || idNumber) {
      // if either shippingName or idNumber is provided, attempt to get by shipping name and id number
      if (!shippingName || !idNumber) {
        // if only one is provided, throw an error
        throw new Error('Please provide both a shipping name and an ID number.');
      }
      return this.apiClient.get(
        `v1/emanifest/lookup/hazard-classes-by-shipping-name-id-number/${shippingName}/${idNumber}`,
      );
    }
    return this.apiClient.get('v1/emanifest/lookup/hazard-classes');
  };

  /**
   * Returns a list of all available DOT packing groups.
   */
  public getPackingGroups = async (
    shippingName?: string,
    idNumber?: string,
  ): Promise<AxiosResponse<string[] | string>> => {
    if (shippingName || idNumber) {
      // if either shippingName or idNumber is provided, attempt to get by shipping name and id number
      if (!shippingName || !idNumber) {
        // if only one is provided, throw an error
        throw new Error('Please provide both a shipping name and an ID number.');
      }
      return this.apiClient.get(
        `v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/${shippingName}/${idNumber}`,
      );
    }
    return this.apiClient.get('v1/emanifest/lookup/packing-groups');
  };

  // Site Services

  /**
   * Get a site by its EPA ID.
   */
  public getSite = async (siteID: string): Promise<AxiosResponse> => {
    return this.apiClient.get(`v1/site-details/${siteID}`);
  };

  /**
   * Returns true if the site, by EPA ID, exists in RCRAInfo.
   */
  public getSiteExists = async (siteID: string): Promise<AxiosResponse<{ result: boolean; epaSiteId: string }>> => {
    return this.apiClient.get(`v1/site-exists/${siteID}`);
  };

  /**
   * Search for sites by name, address (city, state, zip, etc.) EPA ID, or type.
   */
  public searchSites = async (searchParameters: SiteSearchParameters): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/site-search', searchParameters);
  };

  // User Services

  /**
   * Search for RCRAInfo registered users
   */
  public searchUsers = async (searchParameters: UserSearchParameters): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/user/user-search', searchParameters);
  };

  // e-Manifest Services

  /**
   * Returns info on bill, required to be paid by TSDFs, for incurred fees for each manifest submitted.
   * @param searchParameters
   */
  public getBill = async (searchParameters: BillGetParameters): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/emanifest/billing/bill', searchParameters);
  };

  /**
   * Search for bills by the given parameters.
   */
  public searchBill = async (searchParameters: BillSearchParameters): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/emanifest/billing/bill-search', searchParameters);
  };

  /**
   * Search for a TSDF's bill history by the given parameters.
   * @param searchParameters
   */
  public getBillHistory = async (searchParameters: BillHistoryParameters): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/emanifest/billing/bill-history', searchParameters);
  };

  // ToDo
  // public updateManifest = async (): Promise<AxiosResponse<any>> => {
  //   return this.apiClient.put('v1/emanifest/manifest/update');
  // };

  /**
   * Delete a manifest by its tracking number. There are restrictions on when a manifest can be deleted.
   * @param manifestTrackingNumber
   */
  public deleteManifest = async (manifestTrackingNumber: string): Promise<AxiosResponse<any>> => {
    return this.apiClient.delete(`v1/emanifest/manifest/delete${manifestTrackingNumber}`);
  };

  // ToDo
  // public saveManifest = async (): Promise<AxiosResponse<any>> => {
  //   return this.apiClient.post('v1/emanifest/manifest/save');
  // };

  // ToDo
  // public getManifestAttachments = async (manifestTrackingNumber: string): Promise<AxiosResponse<any>> => {
  //   return this.apiClient.get(`v1/emanifest/manifest/${manifestTrackingNumber}/attachments`);
  // };

  /**
   * Retrieve information about all manifest correction versions by manifest tracking number
   */
  public getManifestCorrections = async (manifestTrackingNumber: string): Promise<AxiosResponse<any>> => {
    return this.apiClient.get(`v1/emanifest/manifest/correction-details/${manifestTrackingNumber}`);
  };

  /**
   * Retrieve details of manifest correction version
   */
  public getManifestCorrectionVersion = async (
    parameters: ManifestCorrectionParameters,
  ): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/emanifest/manifest/correction-version', parameters);
  };

  /**
   * Retrieve details of manifest correction version including attachments.
   */
  public getManifestCorrectionAttachments = async (
    parameters: ManifestCorrectionParameters,
  ): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/emanifest/manifest/correction-version/attachments', parameters);
  };

  /**
   * Retrieve Manifest Tracking Numbers for provided site id.
   */
  public getMTN = async (siteID: string): Promise<AxiosResponse<any>> => {
    return this.apiClient.get(`v1/emanifest/manifest-tracking-numbers/${siteID}`);
  };

  /**
   * Retrieve site ids for provided state (code) and site type (i.e. Generator, Tsdf, Transporter).
   */
  public getSiteID = async (stateCode: string, siteType: string): Promise<AxiosResponse<any>> => {
    return this.apiClient.get(`v1/emanifest/site-ids/${stateCode}/${siteType}`);
  };

  /**
   * Retrieve e-Manifest by provided manifest tracking number.
   */
  public getManifest = async (manifestTrackingNumber: string): Promise<AxiosResponse<any>> => {
    return this.apiClient.get(`v1/emanifest/manifest/${manifestTrackingNumber}`);
  };

  /**
   * Retrieve manifest tracking numbers based on provided search criteria in JSON format.
   */
  public searchManifest = async (parameters: ManifestSearchParameters): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/emanifest/manifest/search', parameters);
  };

  /**
   * Check if Manifest Tracking Number exists. Unless system error happens, this service always returns 200 HTTP code.
   */
  public getMTNExists = async (manifestTrackingNumber: string): Promise<AxiosResponse<ManifestExistsResponse>> => {
    return this.apiClient.get(`v1/emanifest/manifest/mtn-exists/${manifestTrackingNumber}`);
  };

  /**
   * Revert manifest in 'UnderCorrection' status to previous 'Corrected' or 'Signed' version.
   */
  public revertManifest = async (manifestTrackingNumber: string): Promise<AxiosResponse<any>> => {
    return this.apiClient.get(`v1/emanifest/manifest/revert/${manifestTrackingNumber}`);
  };

  /**
   * Performs 'quicker' signature for the entity within the manifest specified by given
   * siteId and siteType. If siteType is 'Transporter', transporter order must be specified to
   * indicate which transporter performs the signature.
   */
  public SignManifest = async (parameters: QuickerSign): Promise<AxiosResponse<any>> => {
    return this.apiClient.post('v1/emanifest/manifest/quicker-sign', parameters);
  };

  // ToDo
  // public correctManifest = async (): Promise<AxiosResponse<any>> => {
  //   return this.apiClient.post('v1/emanifest/manifest/correct');
  // };
}
