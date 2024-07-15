from datetime import datetime
from typing import (
    Any,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
)

from typing_extensions import Required


class RcraCodeDescription(TypedDict, total=False):
    """A code and an accompanying description"""

    code: Required[str]
    description: str


class Phone(TypedDict, total=False):
    """A RCRAInfo phone number"""

    number: Required[str]
    extension: Optional[str]


class Contact(TypedDict, total=False):
    """RCRAInfo user contact information"""

    firstName: str
    middleInitial: str
    lastName: str
    phone: Phone
    email: str
    companyName: str


class RcraLocality(TypedDict, total=False):
    """A RCRAInfo locality (state or country)"""

    code: Required[str]
    name: str


class Address(TypedDict, total=False):
    """An address in the RCRAInfo system"""

    address1: Required[str]
    address2: str
    city: str
    country: RcraLocality
    state: RcraLocality
    zip: str


SiteType = Literal["Generator", "Tsdf", "Transporter", "Broker", "RejectionInfo_AlternateTsdf"]


class RcraSite(TypedDict):
    """A site in the RCRAInfo system"""

    canEsign: bool
    contact: Contact
    epaSiteId: str
    federalGeneratorStatus: str
    gisPrimary: bool
    hasRegisteredEmanifestUser: bool
    limitedEsign: bool
    mailingAddress: Address
    name: str
    siteAddress: Address
    siteType: SiteType


class PortOfEntry(TypedDict):
    """Ports that waste can enter/exit the US"""

    cityPort: str
    state: RcraLocality


class SiteExistsResponse(TypedDict):
    """site exists service response"""

    epaSiteId: str
    result: bool


class SiteSearchArgs(TypedDict, total=False):
    """Search parameters for site search service"""

    epaSiteId: Optional[str]
    name: Optional[str]
    streetNumber: Optional[str]
    address1: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    siteType: Optional[str]
    pageNumber: Optional[int]


class UserSearchArgs(TypedDict, total=False):
    """Search parameters for user search service"""

    userId: Optional[str]
    siteIds: Optional[List[str]]
    pageNumber: Optional[int]


class _UserPermission(TypedDict):
    """A user's permissions for a module in RCRAInfo for a given site"""

    level: str
    module: str


class _UserSiteAccess(TypedDict):
    """A user's permissions for a site"""

    permissions: List[_UserPermission]
    siteId: str
    siteName: str


class _UserWithSiteAccess(TypedDict):
    """User details from the user search service"""

    email: str
    esaStatus: str
    firstName: str
    lastLoginDate: str
    lastName: str
    phone: Phone
    sites: List[_UserSiteAccess]
    userId: str


class UserSearchResponse(TypedDict):
    """body of the response from the user search service"""

    currentPageNumber: int
    searchedParameters: list
    totalNumberOfPages: int
    totalNumberOfUsers: int
    users: List[_UserWithSiteAccess]
    warnings: List[Any]


CorrectionRequestStatus = Literal["NotSent", "Sent", "IndustryResponded", "Cancelled"]

DateType = Literal["CertifiedDate", "ReceivedDate", "ShippedDate", "UpdatedDate", "QuickSignDate"]

SubmissionType = Literal["FullElectronic", "Hybrid", "Image", "DataImage5Copy"]

Status = Literal[
    "Pending",
    "Scheduled",
    "InTransit",
    "Received",
    "ReadyForSignature",
    "Signed",
    "SignedComplete",
    "UnderCorrection",
    "Corrected",
]


class _ManifestComment(TypedDict):
    """A comment on a manifest"""

    label: str
    description: str
    handlerId: str


class MtnSearchArgs(TypedDict, total=False):
    """Search parameters for manifest tracking numbers"""

    stateCode: str
    siteId: str
    submissionType: SubmissionType
    status: Status
    dateType: DateType
    siteType: SiteType
    transporterOrder: int
    startDate: datetime
    endDate: datetime
    correctionRequestStatus: CorrectionRequestStatus
    comments: _ManifestComment


BillStatus = Literal[
    "Active",
    "Paid",
    "Unpaid",
    "ReadyForPayment",
    "Credit",
    "InProgress",
    "SendToCollections",
    "ZeroBalance",
]


class SearchBillArgs(TypedDict, total=False):
    """Search parameters for billing history"""

    billingAccount: str
    billStatus: BillStatus
    startDate: datetime | str
    endDate: datetime | str
    amountChanged: bool
    pageNumber: int


class CorrectionVersionSearchArgs(TypedDict, total=False):
    """Search parameters for manifest correction versions"""

    manifestTrackingNumber: str
    status: Status
    ppcStatus: Literal["PendingDataEntry", "DataQaCompleted"]
    versionNumber: str


class CorrectionRevertResponse(TypedDict):
    """Information returned after successfully reverting a manifest under correction"""

    currentVersionNumber: int
    date: str
    manifestTrackingNumber: str
    operationStatus: str


class ManifestOperationResponse(TypedDict):
    """Information returned to indicate the status of a manifest operation"""

    manifestTrackingNumber: str
    operationStatus: str
    date: datetime


class SignManifestArgs(TypedDict, total=False):
    """Arguments for Quick signing a manifest through the quicker-sign service"""

    manifestTrackingNumbers: Required[List[str]]
    siteId: Required[str]
    siteType: Required[SiteType]
    printedSignatureName: Required[str]
    printedSignatureDate: Required[Union[datetime, str]]
    transporterOrder: int


class _QuickSignManifestReport(TypedDict):
    """Part of body returned from the quicker-sign service"""

    manifestTrackingNumber: str


class _QuickSignSignerReport(TypedDict, total=False):
    """Report of the signer's actions. Part of body returned from the quicker-sign service"""

    electronicSignatureDate: datetime
    firstName: str
    lastName: str
    printedSignatureDate: datetime
    printedSignatureName: str
    userId: str
    warnings: List[dict]


class _QuickSignSiteReport(TypedDict):
    """Part of body returned from the quicker-sign service"""

    siteId: str
    siteType: str


class ManifestSignatureResponse(ManifestOperationResponse):
    """Status report returned from the quicker-sign service"""

    manifestReports: List[_QuickSignManifestReport]
    reportId: str
    signerReport: _QuickSignSignerReport
    siteReport: _QuickSignSiteReport


UiLinkViews = Literal[
    "Incoming",
    "Outgoing",
    "All",
    "Transporting",
    "Broker",
    "CorrectionRequests",
    "Original",
    "Corrections",
]

UiLinkPages = Literal["Dashboard", "BulkSign", "BulkQuickSign", "Edit", "View", "Sign"]


class UILinkArgs(TypedDict, total=False):
    """Arguments for generating a Manifest UI link"""

    page: Required[UiLinkPages]
    epaSiteId: Required[str]
    manifestTrackingNumber: str
    filter: List[str]
    view: UiLinkViews


AgencyCode = Literal["B", "C", "E", "L", "N", "S", "T", "X", "J", "P"]

OriginType = Literal["Service", "Web", "Mail"]


class DiscrepancyResidueInfo(TypedDict, total=False):
    """Manifest Waste Discrepancy info"""

    wasteQuantity: bool
    wasteType: bool
    discrepancyComments: Optional[str]
    residue: bool
    residueComments: Optional[str]


class DotInformation(TypedDict):
    """Waste Line Department of Transportation Information"""

    idNumber: RcraCodeDescription
    printedDotInformation: str


class Quantity(TypedDict, total=False):
    """Waste Line Quantities"""

    containerNumber: int
    containerType: RcraCodeDescription
    quantity: int
    unitOfMeasurement: RcraCodeDescription


class BrInfo(TypedDict, total=False):
    """Biennial Report Information that can be added to a manifest"""

    density: Optional[float]
    densityUnitOfMeasurement: Optional[RcraCodeDescription]
    formCode: Optional[RcraCodeDescription]
    sourceCode: Optional[RcraCodeDescription]
    wasteMinimizationCode: Optional[RcraCodeDescription]
    mixedRadioactiveWaste: Optional[bool]


class HazardousWaste(TypedDict, total=False):
    """Key codes that indicate the type of hazardous waste"""

    federalWasteCodes: List[RcraCodeDescription]
    tsdfStateWasteCodes: List[RcraCodeDescription]
    txWasteCodes: List[str]
    generatorStateWasteCodes: List[RcraCodeDescription]


class Comment(TypedDict, total=False):
    """A comment on a manifest or waste line"""

    label: Optional[str]
    description: Optional[str]
    handlerId: Optional[str]


class AdditionalInfo(TypedDict, total=False):
    """Additional Information structure for use on a manifest or individual waste line"""

    originalManifestTrackingNumbers: Optional[List[str]]
    newManifestDestination: Optional[str]
    consentNumber: Optional[str]
    comments: Optional[List[Comment]]


class PcbInfo(TypedDict, total=False):
    """Polychlorinated biphenyls information on a manifest waste line"""

    loadType: Optional[RcraCodeDescription]
    articleContainerId: Optional[str]
    dateOfRemoval: Optional[str]
    weight: Optional[float]
    wasteType: Optional[str]
    bulkIdentity: Optional[str]


class Waste(TypedDict, total=False):
    """Instance of a manifest waste line"""

    lineNumber: Required[int]
    dotHazardous: Required[bool]
    epaWaste: Required[bool]
    pcb: Required[bool]
    dotInformation: Optional[DotInformation]
    wasteDescription: Optional[str]
    quantity: Optional[Quantity]
    brInfo: Optional[BrInfo]
    br: bool
    hazardousWaste: Optional[HazardousWaste]
    pcbInfos: Optional[List[PcbInfo]]
    discrepancyResidueInfo: Optional[DiscrepancyResidueInfo]
    managementMethod: Optional[RcraCodeDescription]
    additionalInfo: Optional[AdditionalInfo]


class __BaseManifest(TypedDict, total=False):
    """For Internal Use. The bulk of fields in the manifest except for the 'import' field"""

    createdDate: datetime | str
    updatedDate: datetime | str
    manifestTrackingNumber: str
    status: Status
    discrepancy: bool
    submissionType: SubmissionType
    originType: OriginType
    shippedDate: datetime | str
    receivedDate: datetime | str
    generator: RcraSite
    transporters: list[RcraSite]
    designatedFacility: RcraSite
    additionalInfo: AdditionalInfo
    wastes: list[Waste]
    rejection: bool
    residue: bool
    # import: bool # This field is added via the ImportFieldMixin
    containsPreviousResidueOrRejection: bool


# Since we can't use the 'import' keyword as a field name, we add it via this mixin
ImportFieldMixin = TypedDict("ImportFieldMixin", {"import": bool})


class Manifest(__BaseManifest, ImportFieldMixin):
    """The RCRA uniform hazardous waste manifest"""

    pass


class ManifestExistsResponse(TypedDict):
    """manifest exists service response"""

    manifestTrackingNumber: str
    result: bool
    originType: OriginType
    submissionType: SubmissionType
    status: Status
