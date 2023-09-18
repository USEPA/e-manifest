# Manifest Delete Service

The Delete service allows certain manifests to be removed from the system by Manifest Tracking Number (MTN). Depending
on the manifest submission type, the manifest can be deleted in the following statuses:

- `"FullElectronic"`: can be deleted only if in the `"Pending"` or `"Scheduled"` status
- `"Hybrid"`: can be deleted only if in the `"Pending"` or `"Scheduled"` status
- `"DataImage5Copy"`: can be deleted only if in the `"ReadyForSignature"` or "MtnValidationFailed" status
- `"Image"`: can be deleted only if `originType` = `"Web"` or `"Service"` and status is in the `"ReadyForSignature"`
  or `"MtnValidationFailed"` status

Service will check if the manifest is locked. The manifest is locked for delete when Manifest is in a queue for signing.

## Parameters

- [Security Token](../authentication.md#security-tokens)
- Manifest Tracking Number

## Examples

```http
DELETE /rcrainfo/rest/api/v1/emanifest/manifest/delete/123456789ELC HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json

```

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will check if the provided manifest tracking number is valid and exists in the system.

   3.1 {{#include ../../components/mtn-validation-steps.md}}

   3.2 The system will check if the manifest can be deleted.

   - If the manifest submission type is `"FullElectronic"` or `"Hybrid"` or not selected and manifest status is
     not `"Pending"`of `"Scheduled"` the system will stop the processing and generate the following error:
     - `E_IncorrectStatusForDelete: Manifest with submission type of [Full Electronic/Hybrid] can be deleted only in Pending or Scheduled status`
   - If Manifest submission type is `"DataImage5Copy"` and Manifest status is not `"ReadyForSignature"` the system will
     stop the processing and generates the following error:
     - `E_IncorrectStatusForDelete: Manifest with submission type of DataImage5Copy can be deleted only in ReadyForSignature or MtnValidationFailed status`
   - If Manifest submission type is "Image" following applies
     - If manifest origin type is `"Web"` or `"Service"` and Manifest status is not `"ReadyForSignature"` the system
       will stop the processing and generates the following error:
       - ` E_IncorrectStatusForDelete: Manifest with submission type of Image can be deleted only in ReadyForSignature or MtnValidationFailed status`
     - If manifest origin type is "Mail" the system will stop the processing and generates the following error:
       - `E_IncorrectOriginForDelete: Manifest with origin type of Mail cannot be deleted`

4. The system will delete the manifest.
5. On success the system returns JSON containing the following information:
   - Manifest Tracking Number
   - Operation Status: `"Deleted"`
   - Date: Date/Time of the operation
6. If any system errors were encountered during processing, the system will return:
   - error containing error code, error message, and error id and date
