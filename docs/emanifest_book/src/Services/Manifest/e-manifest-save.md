# Saving Manifests

The Save Service creates the new Manifest. The service accepts Manifest data in JSON format compliant with e-Manifest
JSON
schema [e-Manifest JSON Schema](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/emanifest.json).
The following submission types are supported for this release:

- FullElectronic
- DataImage5Copy
- Image
- Hybrid

For the “FullElectronic” and “Hybrid” submission types, the Manifest can be submitted at either “Pending” or “Scheduled”
status. If the manifest was created in “Pending” status the transition to “Scheduled” status will be done via the update
service. The transition to the statuses after “Scheduled” for these submission types will be done automatically by
e-Manifest.

For the “DataImage5Copy” and “Image” submission types, the Manifest will be assigned the "ReadyForSignature" status. The
transition to the next status for these submission type will be done automatically by e-Manifest.

Manifests with the “Mail” origin type cannot be saved via the Save service.

For the “DataImage5Copy” and “Image” submission types, the service requires receiving the scanned compressed document
attachment (Printed/Paper, Signed, Scanned Manifest form-2050). Manifest attachment shall be passed as a multipart
binary content. (See sample client implementation for details
at: https://github.com/USEPA/e-manifest/tree/master/Services-Information/sample-client)

For the <mark style="background: #00ced1!important">DataImage5Copy</mark> and “Image” submission types, if the
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

