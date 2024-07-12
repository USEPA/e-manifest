# Manifest User Interface (UI) Link service

The e-Manifest UI service exposes one endpoint that can be used to generate a link (URL) to the RCRAInfo user
interface (specifically the e-Manifest module). This service provides a method to streamline the manifest signing
process for users that do not have an independent system to manage manifests.

It can be used for the following use cases:

1. Link to View a manifest
2. Link to Sign a manifest
3. Link to Edit a manifest
4. Link to display manifest dashboard
5. Link to bulk sign manifest(s)

## Parameters

- [Security Token](../authentication.md#security-tokens)
- The following parameters can be passes in JSON format in the body of the request:

  - `page` specifies the type of the page the link should direct users to. This is a required parameter the options
    include:
    - `Sign`
    - `View`
    - `Edit`
    - `Dashboard`
    - `BulkSign`
    - `BulkQuickSign`
  - `epaSiteId`: the EPA site ID of either the generator, transporter(s) or TSDF participating in the manifest. This
    is a required parameter.
  - `manifestTrackingNumber`: the tracking number of the manifest. This is a required parameter if the
    provided `page` value is either `View`, `Edit`, or `Sign`. This parameter may not be provided if
     the `page` value is equal to `Dashboard`, `BulkSign`, or `BulkQuickSign`.
  - `filter`: An array of manifest tracking number(s) which should be displayed on the manifest Dashboard or bulk
    sign page. This parameter may not be provided if the `page` value is equal to `View`, `Edit`, or `Sign`.
  - `view` : A string value specifying the view the page should take in the UI.  This parameter may not be provided
    if the `page` value is equal to `View`, `Edit`, or `Sign`. Values include `Incoming`, `Outgoing`,
    `All`, `Transporting`, `Broker`, and `CorrectionRequests` if the provided `page` value is `Dashboard`. Values
    include `Original`, `Corrections`, and `CorrectionRequests` if the provided `page` value is `BulkSign`. Values
    include `Incoming`, `Outgoing`, and `Transporting` if the provided `page` value is `BulkQuickSign`. 

## Examples

```http
POST /rcrainfo/rest/api/v1/links/emanifest HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
    "page": "View",
    "epaSiteId": "VATESTGEN001",
    "manifestTrackingNumber": "100035836ELC"
}
```

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will process the request

   - 3.1. If page is not provided then the service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Object has missing required properties ([\"page\"])",
         "field": ""
       }
     ]
   }
   ```

   - 3.2. If provided page is invalid then the service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Instance value (\"provided value\") not found in enum (possible values: [\"Dashboard\",\"BulkSign\",\"View\",\"Edit\",\"Sign\"])",
         "field": ".page",
         "value": "provided value"
       }
     ]
   }
   ```

   - 3.3. If `epaSiteId` is not provided then the service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Object has missing required properties ([\"epaSiteId\"])",
         "field": ""
       }
     ]
   }
   ```

   - 3.4. If provided `epaSiteId` has invalid format then the service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Regex \"^([A-Z][A-Z][A-Za-z0-9]{2,10})$\" does not match input string\"AK96903307420\"",
         "field": ".epaSiteId"
       }
     ]
   }
   ```

   - 3.5. If provided `epaSiteId` is not registered then the service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Site with provided epa site id is not registered",
         "field": "epaSiteId"
       }
     ]
   }
   ```

   - 3.6. If provided `page` is equal to "View" or "Sign" or "Edit" and `manifestTrackingNumber` is not provided then
     the
     service
     generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Value is not provided",
         "field": "manifestTrackingNumber"
       }
     ]
   }
   ```

   - 3.7. If provided `page` is equal to "View" or "Sign" or "Edit" and the `manifestTrackingNumber` provided has an
     invalid
     format
     then the service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Regex \"^[0-9]{9}[A-Z]{3}$\" does not match input string \"provided mtn\"",
         "field": ".manifestTrackingNumber"
       },
       {
         "message": "Invalid Field Format. 9 digits followed by 3 upper case letters is expected",
         "field": "manifestTrackingNumber"
       }
     ]
   }
   ```

   - 3.8. If provided `page` is equal to "View" or "Sign" or "Edit" and the `manifestTrackingNumber` is not found then
     the service
     generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Provided Manifest Tracking Number is not found",
         "field": "manifestTrackingNumber"
       }
     ]
   }
   ```

   - 3.9. If provided `page` is equal to "View" or "Sign" and manifest with provided epa site id
     and `manifestTrackingNumber` is
     not
     found then the service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Provided site id is not participating in the manifest",
         "field": "manifestTrackingNumber"
       }
     ]
   }
   ```

   - 3.10. If provided `page` is equal to "Sign" and manifest is in "Pending" status then the service generates
     following error:

   ```json
   {
     "errors": [
       {
         "message": "Provided manifest is not ready to be signed",
         "field": "manifestTrackingNumber"
       }
     ]
   }
   ```

   - 3.11. If provided `page` is equal to "Dashboard" or "BulkSign" and provided filter elements has invalid format
     then the
     service generates following error:

   ```json
   {
     "errors": [
       {
         "message": "Regex \"^[0-9]{9}[A-Z]{3}$\" does not match input string\"100024600EBLC\"",
         "field": ".filter[i]"
       },
       {
         "message": "Invalid Field Format. 9 digits followed by 3 upper case letters is expected",
         "field": ".filter"
       }
     ]
   }
   ```

4. On success, the service returns the URL for the manifest page
5. If any validation errors were found the service returns an error report
6. If any system errors were encountered during processing, the system will r
