# Manifest Data Services

The manifest data services is category of auxiliary manifest service that can be used to retrieve data for constructing
the manifest form and additional information.

## Site IDs Service

Returns the list of all Site Ids for the provided State Code and Site Type (Generator, Transporter,
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

The following HTTP request will return the list of all Site Ids for the state of California and Transporter Site Type:

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
provided Site Id. The service won’t return Manifests which are in Draft status.

### Parameters

- [Security Token](../authentication.md#security-tokens)
- Site Id to pull manifest tracking numbers for

### Example

The following example will return the list of all Manifest Tracking Numbers for the site with Site Id `VATESTGEN001`

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
