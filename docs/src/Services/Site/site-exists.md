# Site Exists Service

This service checks for the existence of the provided EPA Site ID and, if `"result": true`, if the site has a registered
user in the e-Manifest system. The service returns the provided EPA Site ID and `"return": false`
if the provided EPA Site ID does not have a registered user in the e-Manifest system or provided EPA Site ID
is invalid. It is recommended to invoke the service before invoking search manifest services.

## Parameters

- [Security Token](../authentication.md#security-tokens)
- Site ID: 12 character string
-

## Examples

```http
GET /rcrainfo/rest/api/v1/site-exists/VATESTGEN001 HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService

```

### Completed Response Example

```json
{
  "epaSiteId": "VATESTGEN001",
  "result": true
}
```

See [site-exists-return.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/site-exist-return.json)

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).

3. The system will process the request

   - 3.1. If the site with the provided EPA Site ID is registered in the e-Manifest system, the service will generate
     JSON containing:
     - EPA Site ID
     - Result: true
   - 3.2. If the site with the provided EPA Site ID is not registered in the e-Manifest system or the provided EPA Site
     ID is invalid, the service will generate JSON containing:
     - EPA Site ID
     - Result: false
   - 3.3. The service returns generated JSON

4. If authentication, authorization, or system errors were encountered during processing, the system will return:

   - `error`: containing error code, error message, error id, and error date
