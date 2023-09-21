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
  - "Generator"
  - "Transporter"
  - "Tsdf"
  - "Broker"

### Example

The following HTTP request will return the list of all Site Ids for the state of California and Transporter Site Type:

```http
GET /rcrainfo/rest/api/v1/emanifest/site-ids/CA/Transporter HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json

```

### Successful Response Body

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

### Successful Response Body

```json
["111111111ELC", "222222222ELC", "333333333ELC", "444444444ELC"]
```

## Correction Details Service

## Manifest Correction Version Services
