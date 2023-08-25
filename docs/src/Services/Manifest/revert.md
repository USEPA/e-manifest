# Manifest Revert Service

## Description

The Revert Manifest service deletes the manifest version in the `“UnderCorrection”` status by provided Manifest Tracking
Number. Service will check if the manifest is locked. The manifest is locked for revert when Manifest is in a queue for
signing.

## Parameters

- [Security Token](../authentication.md#security-tokens)
- Manifest Tracking Number

## Sequence of Steps

1. The System will validate the Security Token

   1.1 If Web Security Token is invalid, the system stops the submission and generates the following error:

   - `E_SecurityApiTokenInvalid: Invalid Security Token`

   1.2. If Web Security Token expired, the system stops the submission and generates the following
   error:

   - `E_SecurityApiTokenExpired: Security Token is Expired`

   1.3. If Account was inactivated after the token was issued, the system stops the submission and
   generates the following error:

   - `E_SecurityApiInvalidStatus: This API ID is no longer active`

2. The system will perform User Authorization

   2.1 If Generator, Designated Facility, Transporters, Broker and Alternate Facility entities are not provided, then
   the System will stop the processing and generates the following error:

   - `E_UnableToAuthorize JSON does not contain manifest handlers, unable to authorize`

   2.2 If the User does not have permissions for any Site provided in the manifest JSON, the system will stop the
   processing and generates the following error:

   - `E_IndustryPermissions: The user does not have industry permissions for any Site on this manifest`

   2.3. If user is associated with a Broker site and the manifest submission type is “Image”, then the System will
   stop the processing and generates the following error:

   - `E_BrokerAuthorizationSave: Brokers are not authorized to create Image manifests`

   2.4. For `Image` or `DataImage5Copy` submission types, the user must be authorized for the site that is required to
   submit the manifest to EPA.

   2.4.1. If rejection = false and user is not authorized for the designatedFacility.epaSiteId, the following error is
   generated:

   - `E_DesignatedFacilityAuthorizationSave: User is not authorized for the Designated Facility. Cannot create Image or DataImage5Copy manifests.`

   - 2.4.2 If `rejection` is true, `rejectionInfo.transporterOnSite` is true,
     `alternateDesignatedFacilityType` is “Tsdf” and user is not authorized for
     `rejectionInfo.alternateDesignatedFacility.epaSiteId`, the following error is generated:

   - `E_AltFacilityAuthorizationSave: User is not authorized for the Alternate Designated Facility. Cannot create Image or DataImage5Copy manifests.`

   - 2.4.3. If `containsPreviousRejectOrResidue` is true, `additionalInfo.newManifestDestination`
     is `"OriginalGenerator"`and user is not authorized for `generator.epaSiteId`, the following error is
     generated:

   - `E_GeneratorAuthorizationSave: User is not authorized for the Generator. Cannot create Image or DataImage5Copy manifests`

3. If the User is authenticated and authorized, the system will check if the manifest is locked for corrections.

   3.1. If manifest is in the signing queue, it is locked for correct. The following error will be generated

   - `E_ManifestLockedAsyncSign: Manifest is locked because it is in the queue for signing. Manifest cannot be corrected.`

   3.2. If the manifest is in teh Change Biller process by EPA, it is locked for corrections. The following error will

   - `E_ManifestLockedEpaChangeBiller: Manifest is Locked because EPA is Changing Biller. Manifested cannot be corrected.`

4. The system will process the request.

   4.1. The system will check if the provided MTN is valid and exists in the system.

   4.1.1. Manifest Tracking Number shall be compliant with following rules:

   - Nine numeric characters + valid three character Manifest Tracking Suffix

   - If the provided Manifest Tracking Number does not have valid format the processing will be stopped and system
     generates the following error:
     - `E_InvalidManifestTrackingNumber: Provided Manifest Tracking Number has invalid format`
   - If the provided Manifest Tracking Number does not have a valid suffix the processing will be stopped and system
     generates the following error:
     - `E_InvalidManifestTrackingNumberSuffix: Provided Manifest Tracking Number has invalid`
   - If the Manifest Tracking Number is not in the system the processing will stop and the system generates the
     following error:
     - `E_ ManifestTrackingNumberNotFound: Provided Manifest Tracking Number was not found`

   4.2 the system will check if the user has Industry Permissions for the TSDF Site or for the Generator site or
   for the Alternate TSDF site, any Transporter site , or Broker site provided on the manifest. If the User does
   not have permission, the system will stop the processing and generates the following error:

   - `E_SitePermissions: The user does not have Industry Permissions for either the TSDF Site or Generator Site or Alternate TSDF site, any Transporter site, or Broker site specified in provided JSON`

   4.3 The system will check if the manifest ca be reverted. if no `"UnderCorrection"` version of the manifest exists,
   the system will stop processing and generate the following error:

   - `E_NoVersionForUnderCorrectionStatus: Manifest does not contain the Version in 'UnderCorrection' status`

   4.4 The system reverts the manifest (Deletes Manifest version in `"UnderCorrection"` status)

5. On success the system returns JSON containing the following information:

   - Manifest Tracking Number
   - Operation Status: `"Reverted"`
   - Date: Date/Time of the operation
   - Current Version Number

6. If an error is generated during the validation process, the system will return the following information:
   - Error: containing error code, error message, and error id and date

## Response JSON Example

[crud-manifest-success.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/crud-emanifest-success.json)

Completed Response Example

```json
{
  "manifestTrackingNumber": "100001380ELC",
  "operationStatus": "Reverted",
  "currentVersionNumber": 2,
  "date": "2017-07-27T19:13:28.628+0000"
}
```

Validation Error Return example

```json
{
"code": "E_ManifestTrackingNumberNotFound ",
"message": "Provided Manifest Tracking Number was not Found"
"errorId" : "9v7a9808-s35a5-4874-928f-12fc3def4b56",
"date" : "2017-06-23T23:15:45.095+0000"
}
```
