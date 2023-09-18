# Manifest Search Service

Returns a list of manifests matching the search criteria. The service can be used by both industry and states.

## Parameters

- [Security Token](../authentication.md#security-tokens)
- The following service parameters will be passed as JSON compliant to the JSON schema defined in
  [search-manifest.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/search-manifest.json).

  - `stateCode`: Valid State Code. This is one of two Mandatory Parameters. Either `stateCode` or `siteId` shall be
    provided.
  - `siteId`: TSDF, Generator, or Transporter Site ID. This is one of two Mandatory Parameters. Either `stateCode` or
    `siteId` shall be provided.
  - `siteType`: The type of the site (Generator, Transporter, TSDF) which will be used for the search. If the site
    location address state code is equal to the provided `stateCode` then this search criteria is a match. One of the
    following values may be provided:

    - `Generator`
    - `Transporter`
    - `Tsdf`

    If a parameter is not provided then the search will be performed for all Generators and Transporters and
    TSDFs. This is an optional Parameter.

  - `status`: Manifest Status. Following values can be provided:

    - `Pending`
    - `Scheduled`
    - `InTransit`
    - `ReadyForSignature`
    - `Signed`
    - `SignedComplete`
    - `Corrected`
    - `UnderCorrection`

    If the parameter is provided the manifests which are in the provided status will match the search criteria. If
    this parameter is not provided manifests which are in any of the above statuses will match the search
    criteria. This is an optional parameter.

  - `dateType`: type of the Date which will be used for the date range search. The following values can be provided:

    - `ShippedDate`
    - `ReceivedDate`
    - `CertifiedDate`
    - `UpdatedDate`

    The service will perform a date range search when the date type, startDate and endDate parameters are
    provided. This is an optional parameter.

  - `startDate`: Starting date/time of the date range search. YYYY-MM-DDThh:mm:ss.sTZD date/time format shall be
    provided. This is an optional parameter.
  - `endDate`: Ending date/time of the date range search. YYYY-MM-DDThh:mm:ss.sTZD date/time format shall be provided.
    This is an optional parameter.

## Examples

```http
POST /rcrainfo/rest/api/v1/emanifest/search HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
    "stateCode": "VA",
    "status": "Pending",
    "dateType": "UpdatedDate",
    "startDate": "2023-08-01T00:00:00.0-05:00",
    "endDate": "2023-08-31T23:59:59.0-05:00"
}
```

### Valid JSON Bodies

The following example searched for all manifests where the Generator site address state code is equal to "MD" and have
"Scheduled" status:

```json
{
  "stateCode": "MD",
  "status": "Scheduled",
  "siteType": "Generator"
}
```

The following example searches for all manifests where either the Generator or Transporter(s) or TSDF site address state
code is equal to "TX" and have been shipped in the Date range between March 6, 2018 9:57:33pm and March 15, 2018 9:14:
44pm:

```json
{
  "stateCode": "TX",
  "dateType": "CertifiedDate",
  "startDate": "2018-03-06T21:57:33",
  "endDate": "2018-03-15T21:14:44"
}
```

The following example to search for all manifests where siteId is
provided and the manifest status is `Signed`

```json
{
  "siteId": "VATESTGEN001",
  "status": "Signed"
}
```

### Example Response body

```json
["100035794ELC", "100035671ELC", "100035735ELC", "100035569ELC", "100035664ELC"]
```

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will process the request.

   - 3.1. If `stateCode` is not provided and `siteId` is not provided, the service will stop processing and generates
     the
     following error:
     - `E_SearchParameterRequiredStateCodeorSiteId: Missing required search parameter State Code or Site ID`
   - 3.2. If an invalid `stateCode` is provided, the service will stop processing and generates the following error:
     - `E_InvalidStateCode: Invalid State Code is Provided`
   - 3.3. If provided Site ID is invalid, the system will stop processing and generate the following error:
     - `E_InvalidSiteId: Provided Site ID has invalid format`
   - 4.1. If Site with provided Site ID is not registered in RCRAInfo, the system will stop processing and generate the
     following error:
     - `E_SiteIsNotFound: Site with Provided Site ID is not Found`
   - 4.2. If the provided status is invalid, the system will stop processing and generate a schema error.
   - 4.3. If the provided dateType is invalid, the system will stop processing and generate a schema error.
   - 4.4. If the provided startDate is invalid, the system will stop processing and generate a schema error.
   - 4.5. If the provided endDate is invalid, the system will stop processing and generate a schema error.

4. System returns the response

   - 5.1. If the System found manifests for the provided search criteria, it returns JSON containing the list of
     obtained Manifest Tracking Numbers
   - 5.2. If no manifests were found for the provided State code, the system returns JSON containing:

5. empty list

   - 6.1. If any system errors were encountered during the processing, the system returns JSON containing:

6. `error`: containing error code, error message, error id
