# Manifest Correct Service

## Introduction

The Correct Manifest Service creates and updates a Manifest Correction (a new version of the manifest will be either
created or updated by the service). If the current manifest status is either `Signed` or `Corrected` then a new
version of the Manifest Correction will be created and automatically receives the status of `UnderCorrection`. If the
current manifest status is `UnderCorrection` then the current Manifest Correction version can be updated with the same
service. Note, there is only one version with the `UnderCorrection` status at any given time and this version is
viewable and editable by all registered handlers on the manifest.

For the Image manifests submitted via the Industry application or save service, the Correct service will create a new
version either before the manifest was processed by the by Paper Processing Center (PPC) or after the manifest was
processed by PPC. If the manifest is currently being processed by PPC the service will return an error.

For manifests submitted by mail (`Image` no longer accepted since 2021) the Correct service will create a new version
only after the manifest was processed by PPC. The service will not create new version if the manifest was not processed
by PPC or is currently being processed by PPC.

The service accepts Manifest data in JSON format compliant with the {{#include ../../components/manifest-json-link.md}}.
All submission types are supported by this service. For the `"DataImage5Copy"` and `Image` submission types, the
service supports (but does not mandate) receiving the scanned compressed document attachment (Printed/Paper, Signed,
Scanned Manifest form-2050). If a user wishes to send a manifest attachment, it shall be passed as a multipart binary
content. (See sample client implementation for details at:

https://github.com/USEPA/e-manifest/tree/master/Services-Information/sample-client For the `"DataImage5Copy"`
and `Image` submission types, if the Manifest contains an attachment the following metadata JSON elements shall be
presented in the Manifest JSON:

```json
{
  "printedDocument": {
    "name": "user_provided_document_name.pdf",
    "size": 23455,
    "mimeType": " APPLICATION_PDF"
  }
}
```

where `size` is the number of bytes of the PDF document.

The service will validate the submitted JSON (see details in section "Manifest entities and fields
validation for Create Correction service") and if:

- No Errors or Warnings were found: The service will create or update the manifest correction
  and return the Manifest Tracking Number, operation status, and operation date.
- Only Warnings were found: The service will create or update the manifest correction and
  return the Manifest Tracking Number, operation status, current version, operation date and
  Warning Report containing all found warnings.
- Error(s) were found: The service will not create or update the manifest correction and
  return Error Report containing all found errors.
- Error(s) and Warnings were found. Service will not create or update the manifest correction
  and return Error and Warning Reports containing all found errors and warnings.

## Parameters

- {{#include ../../components/manifest-json-link.md}}
- [attachment](./manifest-attachments.md) (optional)
- [Security Token](../authentication.md#security-tokens)

## Examples

```http
PUT /rcrainfo/rest/api/v1/emanifest/manifest/correct HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
    "manifestTrackingNumber": "123456789ELC",
    "status": "Signed",
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

and [crud-emanifest-return.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/crud-emanifest-return.json)

### Completed Response Examples

Correction created response without warnings

```json
{
  "manifestTrackingNumber": "100001380ELC",
  "reportId": "43f52e98-4b01-4b61-8c42-3d6ab42c5bf3",
  "date": "2018-10-09T15:18:56.145+0000",
  "operationStatus": "CorrectionCreated"
}
```

correction updated response without warning

```json
{
  "manifestTrackingNumber": "100001380ELC",
  "reportId": "33f561fc-2142-48b5-97eb-c6de0899814f",
  "date": "2018-10-09T15:21:09.306+0000",
  "operationStatus": "CorrectionUpdated"
}
```

Response with Warnings and Response with Errors are identical to the Save and Update
services Warning and Error Responses

## Sequence of Steps

1.  [Security Token Validation](../authentication.md#security-token-validation).
2.  [User Authorization](../authentication.md#user-authorization).
3.  The system will check if the manifest is locked for corrections.

    3.1. If manifest is in the signing queue, it is locked for correct. The following error will be generated

        - `E_ManifestLockedAsyncSign: Manifest is locked because it is in the queue for signing. Manifest cannot be corrected.`

    3.2. If the manifest is in teh Change Biller process by EPA, it is locked for corrections. The following error will

        - `E_ManifestLockedEpaChangeBiller: Manifest is Locked because EPA is Changing Biller. Manifested cannot be corrected.`

4.  The system will process the request.

    4.1. The system will validate the provided Manifest JSON and Attachment Document according to
    the [Manifest Save Service](./save.md)

    4.2 If no errors or warnings were generated during the validation process, the service will perform the following
    steps:

    - If the current manifest status is either `Signed` or `Corrected`, then the service creates a new manifest
      version with the provided Manifest information. The service assigns the `UnderCorrection` status to the new
      manifest version.
    - If the current manifest status is `UnderCorrection`, then the service updates the existing Manifest with the
      provided Manifest information.
    - Returns manifest Tracking Number, operation status, and operation date and warning(s) report to the requester.

    4.3. If a warning is generated during the validation process, the service performs the following steps:

    - Generate an Error/Warning Report with all errors and warnings found during validation process.
    - Return Error/Warning report to the requester.
