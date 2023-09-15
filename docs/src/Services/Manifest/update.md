# Manifest Update Service

The Update service updates an existing Manifest. The service requires that the industry system submits a complete
Manifest JSON in order to update a manifest. Individual Manifest fields cannot be updated via this service, only the
entire manifest (see the [manifest correct service](./correct.md) docs for making post-shipment corrections). The update
service accepts Manifest data in JSON format compliant with the e-Manifest JSON
schema ([e-Manifest JSON Schema](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/emanifest.json))
and can also accept a Manifest attachment for the `"DataImage5Copy"` and `"Image"` submission types (Scanned Signed
Paper
Manifest Image pdf). Manifest JSON must contain the Manifest Tracking Number generated for that manifest by the [Save
Manifest service](./save.md). The Save manifest service must be invoked prior to the Update Manifest service for any
manifest. The following submission types are supported:

- `"FullElectronic"`
- `"DataImage5Copy"`
- `"Image"`
- `"Hybrid"`

For`"FullElectronic"`and`"Hybrid"`submission types, the Manifest can be updated with "Pending" or `"Scheduled"`
statuses.
For these submission types the transition to the next statuses after `"Scheduled"` will be done by e-Manifest.

For `"DataImage5Copy"` and `"Image"` submission types the Manifest status shall not be submitted. For this submission
type
the status transition will be done by e-Manifest.

Signed manifests of any submission types cannot be Updated via Update service. `"Image"` Manifests submitted via mail
cannot be updated via Update service at any time.For the `"DataImage5Copy"` and `"Image"` submission types the service
supports receiving the scanned document attachment (Printed, Signed, Scanned Manifest form-2050). Manifest attachment
shall be passed as a multipart binary content. (See sample client implementation for details). For
the `"DataImage5Copy"`
submission type if the Manifest contains an attachment the following metadata JSON elements shall be presented in the
Manifest JSON:

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

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
