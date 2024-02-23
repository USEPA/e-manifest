# Manifest Data Services

The manifest data services is category of auxiliary manifest service that can be used to retrieve data for constructing
the manifest form and additional information.

## Site IDs Service

Returns the list of all site IDs for the provided State Code and Site Type (Generator, Transporter,
TSDF, Broker).

### Parameters

- [Security Token](../authentication.md#security-tokens)
- State Code
- Site Type. One of the following values:
  - `Generator`
  - `Transporter`
  - `Tsdf`
  - `Broker`

### Example

The following HTTP request will return the list of all site IDs for the state of California and Transporter Site Type:

```http
GET /rcrainfo/rest/api/v1/emanifest/site-ids/CA/Transporter HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json

```

### Completed Response Example

```json
["CAD009999999", "CAD009999995", "CAD009999998", "CAD009999997"]
```

## Site Manifest Tracking Numbers Service

Returns the list of Manifest Tracking Numbers for all Manifests stored in the system for the
provided site ID. The service won’t return Manifests which are in Draft status.

### Parameters

- [Security Token](../authentication.md#security-tokens)
- Site ID to pull manifest tracking numbers for

### Example

The following example will return the list of all Manifest Tracking Numbers for the site with site ID `VATESTGEN001`

```http
GET /rcrainfo/rest/api/v1/emanifest/manifest-tracking-numbers/VATESTGEN001 HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json

```

### Completed Response Example

```json
["111111111ELC", "222222222ELC", "333333333ELC", "444444444ELC"]
```

## Correction Details Service

The service returns information about all manifest correction versions by manifest tracking number. The system will
create new manifest versions for both the industry corrections and for the Paper Processing Center (PPC) data
processing. PPC data processing will be performed on `Image` manifests which were submitted by Industry via Web or
Services and on `Image` manifests which were submitted by mail. Depending on the manifest status the service can return
the following information about the manifest:

- If the manifest status is before `Signed` then no manifest versions associated with the manifest will be returned
- If the manifest status is `Signed` and neither `Corrected` nor `UnderCorrection` versions were created then the
  service will return information about the `Signed` version of the manifest.
- If the manifest status is `Corrected` then the service will return information about `Signed` version and all `
Corrected` versions of the manifest.
- If the manifest status is `UnderCorrection` then the service will return information about the `Signed` version of the
  manifest, the `UnderCorrection` version and all `Corrected` versions of the manifest (if any `Corrected` versions were
  created).

Depending on the on manifest Paper Processing Center (PPC) status the service can return the following information about
the manifest versions associated with the PPC processing:

- If ppc status is `Draft` or `DataEntryInProgress` or `PendingDataQc` or `PendingDataQa` then
  no manifest versions associated with PPC processing will be returned
  If PPC status is either `PendingDataEntry` or `DataQaCompleted` then the service will return
  information about the manifest version(s) created for PPC processing.

### Parameters

- [Security Token](../authentication.md#security-tokens)
- Manifest Tracking Number

### Example

```http
GET /rcrainfo/rest/api/v1/emanifest/manifest/get-manifest-correction-details/123456789ELC HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json

```

### Completed Response Example

```json
{
  "manifestTrackingNumber": "111111111ELC",
  "emanifestVersions": [
    {
      "status": "UnderPpcDataEntry",
      "versionNuber": 3,
      "createdDate": "2018-19-25T17:53:54.944+0000",
      "updatedDate": "2018-20-25T17:53:54.944+0000",
      "updatedBy": "x"
    },
    {
      "status": "UnderCorrection",
      "epaSiteId": "OH000023465",
      "createdDate": "2018-09-25T17:53:54.944+0000",
      "updatedDate": "2018-10-25T17:53:54.944+0000",
      "updatedBy": "c"
    },
    {
      "status": "Corrected",
      "versionNumber": 2,
      "active": false,
      "electronicSignature": {
        "signer": {
          "firstName": "b",
          "lastName": "b",
          "userId": "b"
        },
        "signatureDate": "2018-09-25T17:53:54.944+0000",
        "humanReadableDocument": {
          "name": "human-readable.html",
          "size": 1231,
          "mimeType": "TEXT_HTML"
        }
      },
      "epaSiteId": "MD0000206060",
      "createdDate": "2018-09-25T17:53:54.944+0000",
      "updatedDate": "2018-09-25T17:53:54.944+0000",
      "updatedBy": "b"
    },
    {
      "status": "Signed",
      "versionNumber": 1,
      "active": false,
      "electronicSignature": {
        "signer": {
          "firstName": "a",
          "lastName": "a",
          "userId": "a"
        },
        "signatureDate": "2018-09-25T17:53:54.944+0000",
        "humanReadableDocument": {
          "name": "human-readable.html",
          "size": 1346671,
          "mimeType": "TEXT_HTML"
        }
      },
      "epaSiteId": "AK9690330742",
      "createdDate": "2018-06-25T17:53:54.944+0000",
      "updatedDate": "2018-08-25T17:53:54.944+0000",
      "updatedBy": "a"
    }
  ]
}
```

## Manifest Correction Version Services

The Get Manifest Correction Version service returns the data associated with a specific Manifest
correction version based on the provided input parameters. The service also will return the
manifest version(s) created via the PPC processing. The following fields in the returned JSON
specify correction details:

- `status`: The following values can be returned:
  - `Signed`: version signed by the TSDF
  - `Corrected`: version was corrected and electronically signed by either a TSDF or Generator or Transporter user
  - `UnderCorrection`: version is under correction and has not been electronically signed
- `ppcStatus`: The following values can be returned:
  - `PendingDataEntry`: this status will be returned for the Image manifests submitted by industry or mail manifests
    which have not been processed by the PPC
  - `DataQaCompleted`: this status will be returned for the Image manifests which have been processed by the PPC
- `correctionInfo`: contains the following correction information:
  - versionNumber: Contains Manifest version number. Manifest versions will be created only for the manifest which are
    in the `Corrected` or `Signed` statuses. If the version is in the `UnderCorrection` status the version number is
    not assigned.
  - `electronicSignature`: containing
    - `signer`: container user information of the signer
      - `firstName`
      - `lastName`
      - `userId`
    - `signatureDate`
    - `humanReadableDocument`: containing
      - `name`: "human-readable.html"
      - `size`
      - `mimeType`: "TEXT_HTML"
  - `active`: indicates if the Manifest version is active or outdated for the industry.
  - `ppcActive`: Indicates if the Manifest version is active or outdated for the PPC.
  - `epaSiteId`: EPA Site ID associated with the user who signed the version.

The service optionally returns Manifest attachments. If the Manifest contains an attachment(s) and the attachment option
is specified, the following documents will be returned:PDF Document containing printed, scanned and manually signed
Manifest form (Printed Document). Note that this document is not available for the “FullElectronic” or “Hybrid”
submission types.

HTML Document(s) containing human readable representation of the Manifest data signed electronically - Copy Of Record
document (COR). Note that the system generates this Document(s) at the time when the users (Generator, Transporters,
TSDF) are electronically signing the manifest. In order to identify what party the COR document was generated by the
following naming convention is used:

- COR document generated when Generator signed the manifest : <cor-g.html>
- COR document generated when Generator signed the manifest for rejection (If shipment was returned back to the original
  Generator): <cor-g-reject.html>
- COR document generated when Transporter(s) signed the manifest: <cor-t-{transporter order}.html>
- COR document generated when TSDF signed the manifest: <cor-tsdf.html>

PDF Document containing form 8700-22 representation of the Manifest Data. The following document metadata JSON elements
will be presented in Manifest JSON if the Manifest contains attachments:

- Printed Document metadat example

  ```json
  {
    "printedDocument": {
      "name": "user provided document name.pdf",
      "size": 500,
      "mimeType": "APPLICATION_PDF"
    }
  }
  ```

- COR Document (Human Readable Document) signed by TSDF metadata example:

  ```json
  {
    "humanReadableDocument": {
      "name": "cor-tsdf.html",
      "size": 1231,
      "mimeType": "TEXT_HTML"
    }
  }
  ```

- Form 2050 Document metadata example:
  ```json
  {
    "formDocument": {
      "name": "form-8700-22.pdf",
      "size": 1231,
      "mimeType": "APPLICATION_PDF"
    }
  }
  ```

All documents will zipped and zip file will be returned as a multipart binary content. See sample client implementation
for details

### Parameters

- [Security Token](../authentication.md#security-tokens)
- Manifest Tracking Number
- status
- ppcStatus
- versionNumber

### Example

```http
POST /rcrainfo/rest/api/v1/emanifest/manifest/correction-version/attachments HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json

{
"manifestTrackingNumber": "111111111ELC",
"status": "UnderCorrection",
"ppcStatus": "DataQaCompleted",
"versionNumber": 2,
}
```

### Request JSON Schema

[emanifest-correction-version.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/emanifest-correction-version.json)
