# Manifest Sign Service

## Intro

The Manifest signature service exposes the ability to create electronic signatures through the RCRAInfo APIs.
The service performs a "quicker sign" signature for the specified handler, by `siteId` and `siteType`, that is party to
the manifest(s). Quicker signatures are only available for electronic manifests. If `siteType` is `Transporter`, the
transporter order must be specified to indicate which transporter performs the signature.

## Parameters

- [Security Token](../authentication.md#security-tokens)
- [Quicker Sign JSON](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/quicker%20sign.json)
  passed in the body of the request, JSON encoded.
  - `siteId`: required, the RCRAInfo site ID of the handler to sign the manifest
  - `siteType`: required, the RCRAInfo site type of the handler to sign the manifest
    - `Generator`
    - `Transporter`
    - `TSDF`
    - `RejectionInfo_AlternateTsdf`
  - `transporterOrder`: required only if `siteType` is `Transporter`, the order of the transporter signing the
    manifest
  - `printedSignatureName`: required, the name of the person signing the manifest
  - `printedSignatureDate`: required, the date of the signature for the person that signed the manifest.
    YYYY-MM-DDThh:mm:ss.sTZD date/time format shall be provided. The printed signature dates will be set to noon of
    the date entered. The date and time stamp of the signature of the user submitting the signature are captured in
    the system.
  - `manifestTrackingNumbers`: required, an array of manifest tracking numbers to sign

## Examples

An example of the JSON body of a site signing 2 manifest as the transporter.

```json
{
  "siteId": "VATESTRAN02",
  "siteType": "Transporter",
  "transporterOrder": 1,
  "printedSignatureName": "John Trucker Smith",
  "printedSignatureDate": "2021-10-27T03:19:25.443+0000",
  "manifestTrackingNumbers": ["200030073ELC", "100030074ELC"]
}
```

### Completed Response Example

A successful signature will return a report including information like the following

```json
{
  "reportId": "6XedXX88-2YYb-4zOe-9pj1-2iuy2c20zed7",
  "date": "2023-02-06T23:16:20.380+00:00",
  "operationStatus": "Completed",
  "manifestReports": [
    {
      "manifestTrackingNumber": "100034662ELC"
    }
  ],
  "signerReport": {
    "printedSignatureName": "John Smith",
    "printedSignatureDate": "2023-02-06T12:00:00.000+00:00",
    "electronicSignatureDate": "2023-02-06T23:16:20.795+00:00",
    "firstName": "Jane",
    "lastName": "Doe",
    "userId": "JANEDOERCRA",
    "warnings": [
      {
        "field": "printedSignatureDate",
        "message": "Printed Signature Date is set to noon UTC of the day of the provided date",
        "value": "2023-02-06T19:55:58.971Z"
      }
    ]
  },
  "siteReport": {
    "siteId": "VATESTTSDF03",
    "siteType": "Tsdf"
  }
}
```

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will process the request

   - 3.1. The system will check for valid Site Type Enumerated values. If the value provided does not
     match the values in the quicker sign schema, then the service generates the following error:

     - `E_SystemError: Instance value (\"TSDF\") not found in enum (possible values:[\"Generator\",\"Transporter\",\"Tsdf\",\"RejectionInfo_AlternateTsdf\"]): TSDF`

   - 3.2 If the site type is set to Transporter, the system will check for a value in the `transporterOrder` field. If
     the field is null, the service will generate the following error:

     - `Transporter Order is required when site type is Transporter`

   - 3.3. the system will check the Manifest Tracking Number(s) exist. If the value provided does not match an existing
     manifest, then the service generates the following error in the Manifest Reports object (other errors and warnings
     in this section are truncated):

   ```json
   {
     "reportId": "6XedXX88-2YYb-4zOe-9pj1-2iuy2c20zed7",
     "date": "2023-02-06T23:34:38.886+00:00",
     "operationStatus": "Failed",
     "manifestReports": [
       {
         "manifestTrackingNumber": "300034662ELC",
         "errors": [
           {
             "field": "manifestTrackingNumber",
             "message": "Manifest not found",
             "value": "300034662ELC"
           }
         ]
       }
     ]
   }
   ```

   (the other errors and warning in this section are truncated)

   - 3.4. The system will check if the Site ID and provided Manifest Tracking Number(s) in the array are available for
     the signature.
     - 3.4.1. If the provided Manifest Tracking Number is not ready for signature, has been signed by the site, or
       has a different site type than what was submitted, the processing will be stopped and system generates the
       following error:
       - `E_SystemError: "Manifest is not ready to be quick signed by handler Site ID`
   - 3.5. The system will check if the Printed Signature Name field has data in it, if the field is null the system
     generates the following error in the Signer Report object in the response:
     - `Printed Signature Name is required`
   - 3.6. The system will check the length of the Printed Signature Name field, if the field exceeds 80 character the
     system truncates the field to 80 and generates the following warning in the Signer Report object in the response:
     - `Printed Signature Name must be 80 characters or less`
   - 3.7. The system will check for a valid Printed Signature Date field format. If the value provided does not match
     the date format in the quicker sign schema, the system will stop the processing and the service generates the
     following error:
     - `E_SystemError: "String \"202-02-06T19:55:58.971+0000\" is invalid against requested date format(s) [yyyy-MM-dd'T'HH:mm:ssZ, yyyy-MM-dd'T'HH:mm:ss.SSSZ]: 202-02- 06T19:55:58.971+0000`
   - 3.8. The system will check the time stamp of the Printed Signature Date field, if the field is not set to noon UTC
     the system will set the field to noon UTC and generates the following warning in the Signer Report object in the
     response:
     - `Printed Signature Date is set to noon UTL of teh day of teh provided date`
   - 3.9. The system will compare the date of the signature with the previous signature on the manifest. if the date
     provided is before the date of the previous signature the system generates the following error in the Signer
     Report object in the response:
     - `Specified paper signature date can't be before %s's paper signature date`
   - 3.10. The system will Quicker Sign the manifest(s)

4. On success, the system returns JSON containing

   - Operation Status: "Completed"
   - Date: Date/Time of the operation
   - manifestReports: The manifests signed from the submission
   - signerReport: Information on the user and the printed signer that signed the manifest(s)
   - siteReport: The site that signed the manifest(s)

5. If at least one manifest but not all the manifests were signed the system returns JSON containing:

   - Operation Status: "PartiallyCompleted"
   - Date: Date/Time of the operation
   - manifestReports: The manifests signed from the submission and manifests not signed as
     well as the errors as to why they were not signed
   - signerReport: Information on the user and the printed signer that signed the manifest(s)
   - siteReport: The site that signed the manifest(s)

6. If any system error were encountered during processing, the system will return:
   - Operation Status: "Failed"
   - Date: Date/Time of the operation
   - manifestReports: If applicable the errors encountered
   - signerReport: If applicable the errors encountered
   - siteReport: If applicable the errors encountered
