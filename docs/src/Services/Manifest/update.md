# Manifest Update Service

The Update service updates an existing Manifest. The service requires that the industry system submits a complete
Manifest JSON in order to update a manifest. Individual Manifest fields cannot be updated via this service, only the
entire manifest (see the [manifest correct service](./correct.md) docs for making post-shipment corrections). The update
service accepts Manifest data in JSON format compliant with the {{#include ../../components/manifest-json-link.md}}
and can also accept a Manifest attachment for the `DataImage5Copy` and `Image` submission types (Scanned Signed
Paper Manifest Image pdf). Manifest JSON must contain the Manifest Tracking Number generated for that manifest by
the [Save Manifest service](./save.md). The Save manifest service must be invoked prior to the Update Manifest service
for any manifest. The following submission types are supported:

- `FullElectronic`
- `DataImage5Copy`
- `Image`
- `Hybrid`

For`FullElectronic`and`Hybrid`submission types, the Manifest can be updated with "Pending" or `Scheduled` statuses. For
these submission types the transition to the next statuses after `Scheduled` will be done by e-Manifest.

For `DataImage5Copy` and `Image` submission types the Manifest status shall not be submitted. For this submission type
the status transition will be done by e-Manifest.

Signed manifests of any submission types cannot be Updated via Update service. `Image` Manifests submitted via mail
cannot be updated via Update service at any time.For the `DataImage5Copy` and `Image` submission types the service
supports receiving the scanned document attachment (Printed, Signed, Scanned Manifest form-2050). Manifest attachment
shall be passed as a multipart binary content. (See sample client implementation for details). For
the `DataImage5Copy"` submission type if the Manifest contains an attachment the following metadata JSON elements shall
be presented in the Manifest JSON:

```json
{
  "printedDocument": {
    "name": "user provided document name.pdf",
    "size": 23455,
    "mimeType": "APPLICATION_PDF"
  }
}
```

Service will check if the manifest is locked. The manifest is locked for update when Manifest is in a queue for signing.

Service will validate submitted JSON (see sectionManifest entities and fields validation for Update service) and if:

- No Errors or Warnings were found: The service will update the manifest and return the existing Manifest Tracking
  Number
- Only Warnings were found: The service will update the manifest and return the existing Manifest Tracking Number and
  Warning Report containing all found Warnings
- Error(s) were found: The service won't update the manifest and returns Error Report containing all found errors.
- Error(s) and Warnings were found. The service won't update the manifest and returns Error Report containing all found
  errors and warnings.

## Examples

```http
POST /rcrainfo/rest/api/v1/emanifest/manifest/update HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
    "manifestTrackingNumber": "123456789ELC",
    "status": "Scheduled",
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
3. If the user was authenticated and authorized, the system will check if manifest is locked for update.

   - 3.1. If the manifest is in the signing queue, it is locked for update. The following error will be
     generated:
     - `E_ManifestLockedAsyncSign`: Manifest is locked because it is in the queue for signing.
       Manifest cannot be updated.
   - 3.2. If the manifest is in the Change Biller process by EPA, it is locked for update. The following
     error will be generated:
     - `E_ManifestLockedEpaChangeBiller`: Manifest is locked because EPA is Changing Biller.
       Manifest cannot be updated.

4. The system will process the request

   - 4.1. The system will validate the provided Manifest JSON and Attachment Document
     - 4.1.1. The system will validate the e-Manifest fields according to the rules described in
       section Manifest entities and fields validation for Update service
   - 4.2. If no errors or warnings are generated during the validation process, the service will perform
     the following steps:
     - 4.2.1. Update existing Manifest with provided Manifest information
     - 4.2.2. Create or Update Attachment Document into e-Manifest database
     - 4.2.3. Return Manifest Tracking Number to the Requestor.
   - 4.3. If only warnings are generated during the validation process, the service will perform
     following steps:
     - 4.3.1. Update existing Manifest with provided Manifest information
     - 4.3.2. Create or Update Attachment Document into e-Manifest database
     - 4.3.3. Return Manifest Tracking Number and Warning(s) Report to the Requestor
   - 4.4. If an error is generated during the validation process the system will perform the following
     steps:
     - 4.4.1. Generate Error Report with all errors found during validation process
     - 4.4.2. Return Error Report to the Requestor.
   - 4.5. If any errors and warnings were generated during the validation process the system will perform
     following steps
     - 4.5.1. Generate Error/Warning Report with all errors and warnings found during validation
       process
     - 4.5.2. Return Error/Warning Report to the Requestor.
