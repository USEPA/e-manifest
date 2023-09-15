# Site Search Service

Returns a list of sites that match the search criteria.

- `"epaSiteId"`: valid activity location, at least 2 characters
- `"name"`: site name, any number of characters not exceeding 80 characters
- `"streetNumber"`: optional parameter, any number of characters not exceeding 12 characters
- `"address1"`: optional parameter, cannot exceed 50 characters
- `"city"`: cannot exceed 25 characters
- `"state"`: 2 character state code
- `"zip"`: valid zip code
- `"siteType"`: optional, one of enum values `["Generator", "Transporter", "TSDF", "Broker"]`
- `"pageNumber"`: optional, defaults to 1,

## Notes

- The system will perform exact search if provided site id contains exactly 12 characters. Any additional parameters
  will be ignored.
- If at least one of the following parameters is valid, the service will perform non-exact search by individual
  parameters or any combination of them (any optional parameters can be added). Response will contain warnings for any
  invalid parameters.
  - `"epaSiteId"`: if less than 12 characters
  - `"name"`
  - `"streetNumber"`: if streetNumber is provided and address1 is not provided the service will not use streetNumber
    for the search, the service will return an error
  - `"address1"`: if address1 is provided and neither valid city nor valid zip are provided the service will not use
    address1 for the search, the service will return an error
  - `"city"`
  - `"state"`
  - `"zip"`

## Parameters

- Site Search
  JSON ([schema](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/site-search.json))
- [Security Token](../authentication.md#security-tokens)

## Examples

```http
POST /rcrainfo/rest/api/v1/site-search HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
 "epaSiteId":"VATEST",
 "name":"VA TEST",
 "streetNumber":"123",
 "address1":"VA TEST GEN 2021 WAY",
 "city":"Arlington",
 "state":"VA",
 "zip":"22202",
 "siteType":"Generator"
}
```

### Valid site ID 12 character - exact search

```json
{
  "epaSiteId": "VATESTGEN001"
}
```

### Valid site ID, siteType, and pageNumber

```json
{
  "epaSiteId": "VATESTTSD",
  "siteType": "Tsdf",
  "pageNumber": 1
}
```

note, `"pageNumber"` is optional and defaults to 1

### Valid state code and name

```json
{
  "state": "VA",
  "name": "VA TEST"
}
```

### Valid zip and name

```json
{
  "zip": "22202",
  "name": "VA TEST"
}
```

### Valid site ID, zip, and name

```json
{
  "epaSiteId": "VATESTGEN",
  "zip": "22202",
  "name": "VA TEST"
}
```

### Invalid site ID

```json
{
  "epaSiteId": "VATESTGEN"
}
```

If `"epaSiteId"` is less than 12 characters, additional parameters are required or the service will return an error.

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will process the request.

   - 3.1 The service checks if required parameters were provided
   - 3.2 If none of following required parameters are provided:

     - `"epaSiteId"`
     - `"name"`
     - `"streetNumber"`
     - `"address1"`
     - `"city"`
     - `"state"`
     - `"zip"`
       the process will stop and the service will return the following error:
     - `E_SearchParameterRequired: Missing required search parameters: epaSiteId, name,
streetNumber , address1, city, state, zip`

   - 3.3. If all following required parameters are invalid:

     - `epaSiteId`
     - `state`
     - `zip`

     and none of the following parameters are provided:

     - `name`
     - `city`
     - `streetNumber`
     - `address1`

     the processing will be stopped and the system will generate the following error:

     - `E_InvalidSiteIdStateZip: Provided Site ID, State, Zip have an invalid format`

   - 3.4. If the provided Site ID is invalid and none of the required search parameters are
     provided: `name`, `streetNumber`, `address1`, `city`, `state`, `zip`, the processing will be stopped, and the
     system will generate the following error:

     - `E_InvalidSiteId: Provided Site ID has an invalid format`

   - 3.5. If the provided State Code is invalid and none of the required search parameters are
     provided: `name`, `streetNumber`, `address1`, `city`, `site id`, `zip`, the processing will be stopped, and the
     system will generate the following error:

     - `E_InvalidStateCode: Provided State Code is invalid`

   - 3.6. If the provided Zip is invalid and none of the required search parameters are
     provided: `name`, `streetNumber`, `address1`, `city`, `site id`, `state`, the processing will be stopped, and the
     system will generate the following error:

     - `E_InvalidZip: Provided Zip is invalid`

   - 3.7. If the provided State Code is invalid and provided Site ID is invalid and none of the required search
     parameters are provided: `name`, `address1`, `city`, `zip`, the processing will be stopped, and the system will
     generate the following error:

     - `E_InvalidStateCodeSiteId: Provided State Code and Site ID are invalid`

   - 3.8. If the provided State Code is invalid and provided Zip is invalid and none of the required search parameters
     are provided: `name`, `streetNumber`, `address1`, `city`, `site id`, the processing will be stopped, and the
     system will generate the following error:

     - `E_InvalidStateCodeZip: Provided State Code and Zip are invalid`

   - 3.9. If the provided Zip is invalid and provided Site ID is invalid and none of the required search parameters are
     provided:`name`, `streetNumber`, `address1`, `city`, `State`, the processing will be stopped, and the system will
     generate the following error:

     - `E_InvalidZipSiteId: Provided Zip and Site ID are invalid`

   - 3.10. If `streetNumber` is provided and `address1` is not provided and none of the other parameters are provided,
     the service will return an error:

     - `E_Address1NotProvided: Street number is not used for the search because address1 is not provided`

   - 3.11. If `address1` is provided and neither a valid city nor a valid zip are provided, the service will return an
     error:

     - `E_CityZipNotProvided: Address1 is not used for the search because neither City nor Zip are provided`

4. The System returns the response

   - 4.1. If sites were found, the system returns:
     - JSON containing a list of sites, provided search parameters, and any encountered validation warnings
   - 4.2. If no sites were found, the system returns JSON containing the following information:
     - An empty list and any encountered validation warnings
   - 4.3. If any authentication, authorization, validation, or system error was encountered during processing, the
     system will return an appropriate error code.
