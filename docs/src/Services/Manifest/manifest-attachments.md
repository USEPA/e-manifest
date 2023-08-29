# Manifest Attachments

The e-Manifest system allows users to upload/download manifests and continuation sheets in PDF format, for both
electronic and paper manifests. This is used for various purposes, including:

1. Uploading scanned copies of paper manifests prior to submitting (certifying) them
2. Downloading the scanned copy of paper manifests for viewing or printing
3. Downloading electronic manifests in PDF format that can be used for DOT shipping paper requirements
4. Downloading electronic manifests in PDF format that can be signed by the generator for hybrid manifests

## Overview

Manifest attachments are passed in the body of HTTP request/responses as part of multipart binary content. For example,
when invoking the Get Manifest Attachment service, the body of the response will contain two parts, passed as a
multipart/mixed MIME type:

1. The JSON encoded manifest data
2. A .zip file containing the manifest attachment in PDF format

The two parts of the multipart entity are separated by a boundary string, which is specified in the `Content-Type`
header, like so, `Content-Type: multipart/mixed; boundary=Bounday_example_12345`.

When uploading to (e.g., the [Save Manifest service](./save.md)) the .zip file must contain only 1 one PDF file

### Multipart/mixed MIME Type

For more information on the
multipart/mixed [MIME](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) type,
see [RFC 2046](https://tools.ietf.org/html/rfc2046) (particularly section 5.1).

As a simplified example, An HTTP response with a manifest attachment response will look like the following:

```text
HTTP/1.1 200 OK
Content-Type: multipart/mixed; boundary=Boundary_example_12345

 --Boundary_example_12345
 Content-type: application/json

 {
    "manifestTrackingNumber": "123456789ELC",
    "createdDate": "2018-01-01T00:00:00Z",
    ...
 }

 --Boundary_example_12345
 Content-Type: application/octet-stream

    <binary data>
 --Boundary_example_12345--
```

## Attachment Validation

The e-Manifest system does not accept attachments for electronic manifests (they are not required for the electronic
manifesting process). The following validation rules apply to manifest attachments uploaded for paper manifests
submitted as `DataImage5Copy` or `Image` using the [Save](./save.md) or [update](./update.md) Manifest services:

1. For the `DataImage5Copy` and `Image` submission type an attachment contains the scanned copy of the printed
   manifest (form 8700-22) and accompanying continuation sheets (form 8700-22a) signed by the Generator, Transporter(s),
   Designated Facility, and Alternate Designated Facility (if applicable).
2. The scanned document must be zipped and submitted as a part of the Save and Update Manifest service. The zipped
   manifest attachment must be passed as a multipart binary content. The attachment may be submitted at the
   ReadyForSignature status. If the manifest contains an attachment, then attachment metadata elements shall be provided
3. If the document is already stored as a part of the manifest and document is not provided, the service generates no
   errors or warnings.
4. If the document is not stored and the status is ReadyForSignature, the document is mandatory.
5. If an attachment is provided, the service checks if the attachment is a zip file (The services only accept one PDF
   file within the zip file for the printedDocument element). If a non-zipped attachment is provided, the service
   generates the following error:
   ```json
   {
     "message": "Attached document is not compressed(zipped). Service accepts compressed (zip) attachments only",
     "field": "Emanfiest.printedDocument.name",
     "value": "name of the attached document"
   }
   ```
6. If a zipped attachment is provided, the service will unzip the document and perform the following steps:

   - 6.1. If the zip file contains more than one document the service generates the following error:

   ```json
   {
     "message": "Zip contains more than one document",
     "field": "Emanifest.printedDocument"
   }
   ```

   - 6.2. If the attachment contained in the zip file is not a PDF, the service generates the following error:

   ```json
   {
     "message": "Attachment Document is not a PDF",
     "field": "Emanifest.printedDocument"
   }
   ```

7. If an attachment is not provided and Emanifest.printedDocument metadata is provided, the service generates a warning
   ```json
   {
     "message": "no attachment provided",
     "field": "Emanifest.printedDocument.name"
   }
   ```
8. If the following attachment metadata is not provided:

   ```json
   {
     "printedDocument": {
       "name": "name provided by the user.pdf",
       "size": 100,
       "mimeType": "APPLICATION_PDF"
     }
   }
   ```

   where size the number of bytes, the service generates the following error:

   ```json
   {
     "message": "Attachment Document metadata is not provided",
     "field": "Emanifest.printedDocument"
   }
   ```

9. If one or more metadata fields is not provided, the service generates the following warning:

   ```json
   {
     "message": "Attachment Document metadata is not provided",
     "field": "Emanifest.printedDocument"
   }
   ```

10. If metadata is provided, but some of the fields values do not match the zipped content, the service generates the
    following warning(s):

    ```json
    {
      "message": "Attachment Document name/size does not match the actual file name/size",
      "field": "Emanifest.printedDocument",
      "value": "Emanifest.printedDocument.name/size value"
    }
    ```

11. If an incorrect MIME type is provided, the service generates the following error:

    ```json
    {
      "message": "Instance value <provided mime type> not found in enum (possible values: [APPLICATION_PDF, TEXT_HTML])",
      "field": "Emanifest.printedDocument.mimeType",
      "value": "Emanifest.printedDocument.mimeType value"
    }
    ```
