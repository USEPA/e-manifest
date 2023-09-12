# Manifest Revert Service

## Description

The Revert Manifest service deletes the manifest version in the `“UnderCorrection”` status by provided Manifest Tracking
Number. Service will check if the manifest is locked. The manifest is locked for revert when Manifest is in a queue for
signing.

## Parameters

- [Security Token](../authentication.md#security-tokens)
- Manifest Tracking Number

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
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
  "message": "Provided Manifest Tracking Number was not Found",
  "errorId": "9v7a9808-s35a5-4874-928f-12fc3def4b56",
  "date": "2017-06-23T23:15:45.095+0000"
}
```
