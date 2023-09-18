# Manifests Save Service

The Save Service creates the new Manifest. The service accepts Manifest data in JSON format compliant with {{#include
../../components/manifest-json-link.md}}. The following submission types are supported for this release:

- `FullElectronic`
- `DataImage5Copy`
- `Image`
- `Hybrid`

For the `FullElectronic` and `Hybrid` submission types, the Manifest can be submitted at either `Pending`
or `Scheduled`
status. If the manifest was created in `Pending` status the transition to `Scheduled` status will be done via the
update
service. The transition to the statuses after `Scheduled` for these submission types will be done automatically by
e-Manifest.

For the `DataImage5Copy` and `Image` submission types, the Manifest will be assigned the `ReadyForSignature`
status.
The
transition to the next status for these submission type will be done automatically by e-Manifest.

Manifests with the `Mail` origin type cannot be saved via the Save service.

For the `DataImage5Copy` and `Image` submission types, the service requires receiving the scanned compressed
document
attachment (Printed/Paper, Signed, Scanned Manifest form-2050). Manifest attachment shall be passed as a multipart
binary content. (See sample client implementation for details
at: https://github.com/USEPA/e-manifest/tree/master/Services-Information/sample-client)

For the `"DataImage5Copy` and `"Image` submission types, if the
Manifest contains an attachment, the
following metadata
JSON elements shall be presented in the Manifest JSON:

```json
{
  "printedDocument": {
    "name": "user provided document name.pdf",
    "size": 23455,
    "mimeType": "APPLICATION_PDF"
  }
}
```

where `size` is the number of bytes of the PDF document.

The service will validate the submitted JSON and if:

- No Errors or Warnings were found: Service will save the manifest and return generated Manifest Tracking Number
- Only Warnings were found: Service will save the manifest and return generated Manifest Tracking Number and Warning
  Report containing all found Warnings
- Error(s) were found: Service won't save the manifest and return Error Report containing all found errors.
- Error(s) and Warnings were found. Service won't save the manifest and return Error and Warning Report containing all
  found errors and warnings

## Parameters

- {{#include ../../components/manifest-json-link.md}}
- [attachment](./manifest-attachments.md) (optional)
- [Security Token](../authentication.md#security-tokens)

## Examples

```http
POST /rcrainfo/rest/api/v1/emanifest/manifest/save HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
    "manifestTrackingNumber": "123456789ELC",
    "discrepancy": false,
    "submissionType": "FullElectronic",
    "generator": {
        "epaSiteId": "VATESTGEN001",
        "name": "VA TEST GEN 2021",
        "..." : "..."
    },
}
```

See {{#include ../../components/manifest-json-link.md}}.

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. If the User is authenticated and authorized, the system processes the request
4. The system validates the provided Manifest JSON and Attachment Document according to the rules described
   in "[Manifest entities and fields validation for Save service]()". If no errors or warnings were generated during the
   validation process, the service perform the following steps:

   - Generate a Manifest Tracking Number (MTN) for the provided manifest data
   - Store the provided manifest information and attachment document (if applicable) in the e-
     Manifest database
   - Return the MTN to the requestor

5. If a warning is generated during the validation process, the service performs the following steps:

   - Generate an MTN for the provided manifest data
   - Store the provided manifest information and an attachment document in the e-Manifest
     database
   - Return the MTN and Warning(s) report to the requestor

6. If an error is generated during the validation process, the service performs following steps:

   - Generate Error Report with all errors found during validation process
   - Return Error Report to the requestor

7. If any errors and warnings were generated during validation process, the service performs the
   following steps:

   - Generate an Error/Warning report with all errors and warnings found during validation process
   - Return Error/Warning report to the requestor

## Response

see the [crud-emanifest-return.json]()
