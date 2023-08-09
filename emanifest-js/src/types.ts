export interface AuthResponse {
  token: string;
  expiration: string;
}

export type PackingGroups = 'I' | 'II' | 'III';
export type ManifestStatus =
  | 'Pending'
  | 'Scheduled'
  | 'InTransit'
  | 'Received'
  | 'ReadyForSignature'
  | 'Signed'
  | 'SignedComplete'
  | 'UnderCorrection'
  | 'Corrected';

export type SubmissionType = 'FullElectronic' | 'DataImage5Copy' | 'Hybrid' | 'Image';
export type OriginType = 'Web' | 'Service' | 'Mail';

export type SiteType = 'Generator' | 'Tsdf' | 'Transporter' | 'Rejection_AlternateTsdf';

/**
 * structure of many codes used by the manifest (waste codes, management methods codes, etc.)
 */
export interface RcraCode {
  code: string;
  description: string;
}

export interface RcraState {
  code: string;
  name: string;
}

export interface PortOfEntry {
  cityPort: string;
  state: RcraState;
}

export interface SiteSearchParameters {
  epaSiteId: string;
  name: string;
  streetNumber: string;
  address1: string;
  city: string;
  state: string;
  zip: string;
  siteType: 'Generator' | 'Tsdf' | 'Transporter' | 'Broker';
  pageNumber: number;
}

export interface UserSearchParameters {
  userId: string;
  siteIds: string[];
  pageNumber: number;
}

export interface BillGetParameters {
  billId: string;
  billingAccount: string;
  monthYear: string;
}

export interface BillHistoryParameters {
  billingAccount: string;
  startDate: string;
  endDate: string;
}

export interface BillSearchParameters extends BillHistoryParameters {
  billStatus: string;
  amountChanged: boolean;
  pageNumber: number;
}

export interface ManifestCorrectionParameters {
  manifestTrackingNumber: string;
  status: 'Signed' | 'Corrected' | 'UnderCorrection';
  ppcStatus: 'PendingDataEntry' | 'DataQaCompleted';
  version: number;
}

export interface ManifestSearchParameters {
  stateCode: string;
  siteId: string;
  status: ManifestStatus;
  dateType: 'CertifiedDate' | 'ReceivedDate' | 'ShippedDate' | 'UpdatedDate';
  siteType: SiteType;
  startDate: string;
  endDate: string;
  correctionRequestStatus: 'NotSend' | 'Sent' | 'industryResponded' | 'Cancelled';
}

export interface ManifestExistsResponse {
  result: boolean;
  submissionType: SubmissionType;
  originType: OriginType;
  manifestTrackingNumber: string;
  status: ManifestStatus;
}

export interface QuickerSign {
  manifestTrackingNumbers: string[];
  siteID: string;
  siteType: SiteType;
  printedSignatureName: string;
  printedSignatureDate: string;
  transporterOrder: number;
}
