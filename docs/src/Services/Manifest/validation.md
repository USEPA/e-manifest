# Manifest Field Validations

The following validations are performed on the manifest fields:

## Section Validations

### Generator information validation for the Image submission type manifests

The manifest fee will be determined based on the Generator signature date (if provided).

1. Generator information and Generator signature date can be provided for Image submission type
   manifests for the save and update services. See modification details in sections Facility
   Information Validation for "Image" submission type, Generator Site Id and Site Information
   Validation and Paper Signature Info Validation. If Generator information and Generator printed
   signature date is provided and data is valid, the following applies

   1.1. The save and update services will store this data as a part of the manifest

   1.2. The services will set Emanifest.provideImageGeneratorInfo = true

   1.3. The manifest fee will be determined based on the Generator printed signature date upon electronic signature from
   the receiving facility

2. If Generator information and Generator printed signature date is not provided or some of the
   provided data is invalid, the following applies
   2.1. The save and update services will generate the following warning:

   ```json
   {
     "message": "Not all required Generator site and signature information is provided so system cannot determine which price to charge for this manifest. To ensure that this manifest is billed accurately, please update the manifest with all required generator site and signature information.",
     "field": "Emanifest.generator"
   }
   ```

   2.2. The save and update services will also generate warning(s)

   2.3. The services will not store Generator information as a part of the manifest data

   2.4. The services will set Emanifest.provideImageGeneratorInfo = false

   2.5. The manifest fee will be determined based on the receiving facility electronic signature date

### Facility Information Validation for "Image" submission type

1. For the Image submission type one of the following facility EPA Site Ids must be provided: Designated Facility EPA
   Site Id, Generator EPA Site Id or Alternate Designated Facility Site Id
2. The following Facility EPA site Ids shall be provided for the following scenarios:
   - Original Manifest, no Full Rejection: Designated Facility EPA Site Id shall be provided.
   - Original Manifest, Full Rejection to Alternate Designated Facility: Alternate Designated Facility EPA Site Id
     shall be provided.
   - Original Manifest, Full Rejection to the Generator: Designated Facility EPA site Id shall be provided.
   - New Manifest shipping waste back to original Generator (New Manifest is the manifest created as a "result" of the
     Original manifest rejection or residue): Generator Facility EPA Site Id shall be provided. This EPA Site Id shall
     contain the Original Designated Facility Site Id.
   - New Manifest shipping rejected waste to another Designated Facility: Designated Facility EPA Site Id shall be
     provided.
3. If one of the following Ids: Emanifest.designatedFacility.epaSiteId and Emanifest.generator.epaSiteId and
   Emanifest.rejectionInfo.alternateDesignatedFacility.siteId is not provided then the service will return an
   authorization error.
4. If the provided EPA Site Id is not registered, then the service will return an authorization error.
5. If Emanifest.designatedFacility.epaSiteId or Emanifest.generator.epaSiteId or
   Emanifest.rejectionInfo.alternateDesignatedFacility.siteId is provided, the following applies

   5.1. If any of the following Site information is provided then the service generates the following warning:

   - Site Name
   - Site Address
   - Mailing Address

   ```json
   {
     "message": "Registered site was found. Provided site information will be ignored and replaced with registered information",
     "field": "Emanifest.designatedFacility.name /siteAddress/mailingAddress",
     "value": "name/siteAddress/mailingAddress"
   }
   ```

   5.2. Validation of the Contact information is identical to #2 in section

   5.3. Designated Facility (TSDF)/Generator Site Id and Site Information Validation

   5.4. If Emanifest.wastes are provided then the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored.",
     "field": "Emanifest.wastes"
   }
   ```

   5.5. If Emanifest.residue == true then the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.residue = false will be assigned",
     "field": "Emanifest.residue",
     "value": "residue value"
   }
   ```

   5.6. If Emanifest.import == true then the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.import = false will be assigned",
     "field": "Emanifest.import",
     "value": "import value"
   }
   ```

   5.7. The service stores following information as a part of the manifest data:

   - Emanifest.residue = false
   - Emanifest.import = false

6. If Emanifest.designatedFacility.epaSiteId or Emanifest.generator.epaSiteId is provided then the
   following applies

   6.1. If Emanifest.rejection == true, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejection = false will be assigned",
     "field": "Emanifest.rejection",
     "value": " rejection value"
   }
   ```

   6.2. If any of the Emanifest.rejectionInfo fields are provided, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored.",
     "field": "Emanifest.rejectionInfo.{field}",
     "value": "field value"
   }
   ```

7. If Emanifest.designatedFacility.epaSiteId or Emanifest.rejectionInfo.alternateDesignatedFacility.siteId is provided,
   the following applies

   7.1. If Emanifest.containsPreviousRejectOrResidue == true, the service generates the following
   warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.containsPreviousRejectOrResidue = false will be assigned",
     "field": "Emanifest.containsPreviousRejectOrResidue",
     "value": "containsPreviousRejectOrResidue value"
   }
   ```

8. If Emanifest.rejectionInfo.alternateDesignatedFacility.siteId is provided, the following applies

   8.1. If Emanifest.rejection == false, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejection = true will be assigned",
     "field": "Emanifest.rejection",
     "value": " rejection value"
   }
   ```

   8.2. If Emanifest.rejectionInfo.transporterOnSite ==false, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejectionInfo.transporterOnSite = true will be assigned",
     "field": "Emanifest.rejectionInfo.transporterOnSite",
     "value": "rejectionInfo.transporterOnSite value"
   }
   ```

   8.3. If Emanifest.rejectionInfo.rejectionType =="PartiaReject", the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejectionInfo.rejectionType = 'FullReject' will be assigned",
     "field": "Emanifest.rejectionInfo.rejectionType",
     "value": "rejectionInfo.rejectionType value"
   }
   ```

   8.4. If Emanifest.rejectionInfo.alternateDesignatedFacilityType =="Generator" the service generates the following
   warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejectionInfo.alternateDesignatedFacilityType = 'Tsdf' will be assigned",
     "field": "Emanifest.rejectionInfo.alternateDesignatedFacilityType",
     "value": "rejectionInfo.alternateDesignatedFacilityType value"
   }
   ```

   8.5. If rejectionInfo.newManifestTrackingNumbers are provided, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. New Manifest(s) are not created if Transporter is On Site",
     "field": "Emanifest.rejectionInfo.newManifestTrackingNumbers",
     "value": "rejectionInfo.newManifestTrackingNumbers value"
   }
   ```

   8.6. The service stores following information as a part of the manifest data:

   - Emanifest.rejection = true
   - Emanifest.rejectionInfo.transporterOnSite = true
   - Emanifest.rejectionInfo.rejectionType = "FullReject"
   - Emanifest.rejectionInfo.alternateDesignatedFacilityType = "Tsdf"

### Designated Facility (TSDF)/Generator Site Id and Site Information Validation

1. If submissionType is "FullElectronic" and status >= Scheduled then the following applies
   1.1. If Emanifest.generator.epaSiteId is not provided then the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.generator.epaSiteId"
   }
   ```

   1.2. If Emanifest. generator.epaSiteId has an incorrect format then the service generates the following error:

   ```json
   {
     "message": "Invalid Field Format",
     "field": "Emanifest. generator.epaSiteId",
     "value": " epa site id value"
   }
   ```

   1.3. If Emanifest.generator.epaSiteId is not registered in RCRAInfo then the service generates the following error:

   ```json
   {
     "message": "Provided Generator Facility Id is not registered in RCRAInfo",
     "field": "Emanifest. generator.epaSiteId",
     "value": " epa site id value"
   }
   ```

2. If submissionType is "FullElectronic" or "Hybrid" and status >= Scheduled, or submissionType is "DataImage5Copy" then
   the following applies

   2.1. If Emanifest.designatedFacility.epaSiteId is not provided then the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.designatedFacility.epaSiteId"
   }
   ```

   2.2. If Emanifest.designatedFacility.epaSiteId has an incorrect format then service generates the following error:

   ```json
   {
     "message": "Invalid Field Format",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": " epa site id value"
   }
   ```

   2.3. If Emanifest.designatedFacility.epaSiteId is not registered in RCRAInfo then service generates the following
   error:

   ```json
   {
     "message": "Provided Designated Facility Id is not registered in RCRAInfo",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": " epa site id value"
   }
   ```

   2.4. If the Site Contact Phone number is not provided and registered in RCRAInfo Site does not contain the Site
   Contact Phone Number, the system generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.designatedFacility.contact.phone.number"
   }
   ```

   2.5. If the Site Contact Phone number is provided, the system will check the format.

   - If the provided phone number has a valid format the system will store site contact phone number into e-Manifest
     database
   - If the provided phone number has an incorrect format the system generates the following warning:

   ```json
   {
     "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
     "field": "Emanifest.designatedFacility.contact.phone.number",
     "value": "number value"
   }
   ```

   2.6. If the Site Contact Phone Extension is provided, the system will check the format.

   - If provided phone extension has a valid format, the system will store the site contact phone extension into
     e-Manifest database
   - If the provided phone has an incorrect format, the system generates the following warning:

   ```json
   {
     "message": "String \"{provided phone extension value}\" is too long (length: {provided phone value length}, maximum allowed: 6 )",
     "field": "Emanifest.designatedFacility.contact.phone.extension",
     "value": "extension value"
   }
   ```

   2.7. If any of the following TSDF Site Information entities were provided:

   - Site Name
   - Site Address
   - Mailing Address

   The system generates the following warning:

   ```json
   {
     "message": "Registered site was found. Provided site information will be ignored and replaced with registered information",
     "field": "Emanifest.designatedFacility.name /siteAddress",
     "value": "name/siteAddress"
   }
   ```

   2.8. If the user is authorized to use the e-Manifest Save service for the provided Generator Site ID (It means that
   TSDF acts as Generator), then the provided Site ID was already validated during authorization and the system will
   perform following steps:

   2.9. If the Site Contact Phone number is not provided in the JSON and site the is registered in RCRAInfo, the system
   checks if the site has a Contact Phone value registered for the site. If the Contact Phone is not registered in the
   system for that site, the system generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.designatedFacility.contact.phone.number"
   }
   ```

   2.10. If the Site Contact Phone number is provided and registered in RCRAinfo the system checks that the phone number
   is in the correct format.

   2.10.1. If the provided phone number has a valid format, the system will store site contact phone number into the
   e-Manifest database

   2.10.2. If provided phone number has an incorrect format, the system will store registered in RCRAInfo Contact Phone
   number into e-Manifest database and generate the following warning:

   ```json
   {
     "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
     "field": "Emanifest.designatedFacility.contact.phone.number",
     "value": "number value"
   }
   ```

   2.11. If the Site Contact Phone number is provided and registered in RCRAinfo site does not contain Contact Phone.

   2.11.1. If the provided phone number has valid format, the system will store site contact phone number into
   e-Manifest database

   2.11.2. If provided phone number has incorrect format, the system generates the following error:

   ```json
   {
     "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
     "field": "Emanifest.designatedFacility.contact.phone.number",
     "value": "number value"
   }
   ```

   2.12. Validate emergency phone

   2.12.1. If emergency phone number is not provided, the system generates the following error:

   ```json
   {
     "message": "Mandatory Field is not provided",
     "field": "Emanifest.designatedFacility.emergencyPhone.number"
   }
   ```

   2.12.2. If emergency phone number is provided and has an invalid format, the system generates the following error:

   ```json
   {
     "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
     "field": "Emanifest.designatedFacility.emergencyPhone.number ",
     "value": "phone number value"
   }
   ```

   2.12.3. If emergency phone extension is provided and has an invalid format, the system generates the following
   warning:

   ```json
   {
     "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 6)",
     "field": "Emanifest.generator.emergencyPhone.extension ",
     "value": "extension value"
   }
   ```

   2.13. If Site Name, Site Location, Site Mailing Address are provided, the system generates the following warning:

   ```json
   {
     "message": "Provided Values will be Ignored. RCRAInfo values will be used",
     "field": "Emanifest.generator.name/mailingAddress/siteAddress ",
     "value": "name/mailingAddress/siteAddress value"
   }
   ```

   2.14. If the contact email was provided, the system will check the format

   2.14.1. If provided contact email has a valid format the system will store site contact email into e-Manifest
   database

   2.14.2. If the provided contact email has an incorrect format the system generates the following warning:

   ```json
   {
     "message": "Invalid Field format. Valid email format is expected.",
     "field": "Emanifest.designatedFacility.contact.email",
     "value": "email value"
   }
   ```

### Generator Site Id and Site Information Validation

1. If submissionType is "FullElectronic" then the Generator is valid if the Generator Site ID is registered in RCRAInfo
   and the Generator has at least one User with the e-Manifest Certifier Role and this user has a Received ESA.
2. If submissionType is "FullElectronic" the following applies

   2.1. If the Generator Site ID is not provided, the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided. For FullElectronic submission type registered Generator Site Id must be provided",
     "field": "Emanifest.designatedFacility.epaSiteId"
   }
   ```

   2.2. If the Generator Site ID has an invalid format the service generates the following error:

   ```json
   {
     "message": "Invalid Field Format. For FullElectronic submission type registered Generator Site Id must be provided",
     "field": "Emanifest.generator.epaSiteId",
     "value": "Site ID value"
   }
   ```

   2.3. If the Generator Site ID is not registered in RCRAInfo the service generates the following error:

   ```json
   {
     "message": "Provided Generator Facility Id is not registered in RCRAInfo",
     "field": "Emanifest.generator.epaSiteId",
     "value": "Site ID value"
   }
   ```

   2.4. If the Generator Site ID is registered in RCRAInfo and there are no users with the e-Manifest Certifier role for
   the provided Generator the service generates the following error:

   ```json
   {
     "message": "Site doesn't have any users with Certifier role or with ESA status Received",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": "Site ID value"
   }
   ```

   2.5. If the Generator with the provided Site ID is registered and there are no users with a received ESA, the service
   generates the following error:

   ```json
   {
     "message": "Site doesn't have any users with Certifier role or with ESA status Received",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": "Site ID value"
   }
   ```

3. If submissionType is "DataImage5Copy" or "Hybrid", then registered and non-registered Generators are valid and the
   following cases are possible for the Generator Site ID and Generator Information:

   3.1. If the Generator is registered in RCRAInfo and service requester does not intend to provide different (than
   registered) Site Information, then only the epaSiteId shall be provided. All site information will be obtained from
   RCRAInfo.

   3.2. If the Generator is registered in RCRAInfo and service requester intends to provide different (than registered)
   Site Information, then the following site information entities must be provided:

   - Site ID
   - Site Name
   - Site Address (all fields)
   - Mailing Address (all fields)
   - Contact Phone
   - Provided Site Information will be validated and if valid will be stored in e-Manifest.

   3.3. If Generator is not registered in RCRAInfo, then following site information must be provided:

   - Site Name
   - Site Address (all fields)
   - Mailing Address (all fields)
   - Contact phone

     Requester also can provide Site ID which is an optional field for this case. If Site ID is provided,
     the system will check if there is a registered Generator for the provided Site ID

   3.4. For all above cases Emergency Phone Number must be provided

   3.5. If the manifest status is InTransit or thereafter then Generator information cannot be updated.

   3.6. If different than currently stored Generator information is provided, the service generates the following
   warning:

   ```json
   {
     "message": "Provided Generator information will be ignored. Generator Information cannot be updated if the manifest status is InTransit or thereafter",
     "field": "Emanifest.generator"
   }
   ```

   3.7. If the Site ID is not provided AND any of the mandatory Site information entities are not provided, the service
   generates the following error(s):

   ```json
   {
     "message": "Mandatory Field is not provided",
     "field": "Emanifest.generator.epaSiteId"
   }
   ```

   ```json
   {
     "message": "Mandatory Field is not provided",
     "field": "Emanifest.generator.siteAddress"
   }
   ```

   ```json
   {
     "message": "Mandatory Field is not provided",
     "field": "Emanifest.generator.mailingAddress"
   }
   ```

   3.8. If the Site ID is provided AND Site Address information is not provided, the system performs the following
   steps:

   - If Site ID is not valid the service generates the following error:

   ```json
   {
     "message": "Provided Value is not Valid. Does not match format of: Two Letter Activity Location Code + Up to 10 alphanumeric characters",
     "field": "Emanifest.generator.epaSiteId ",
     "value": "EPA site Id value"
   }
   ```

   - If Site ID is valid and found in RCRAInfo, the system will obtain the Site information from RCRAInfo and store it
     into the Manifest. System sets modified= false, registered = true
   - If the Site ID is not found, the service generates the following error:

   ```json
   {
     "message": "Provided Value is not Found",
     "field": "Emanifest.generator.epaSiteId",
     "value": "EPA Site ID value"
   }
   ```

   3.9. If the Site ID is provided and the Site Information entities are provided, the system performs the following
   steps:

   - If the site name is not provided, the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.generator.name"
   }
   ```

   - If the site name is not valid (exceeds maximum length), the service generates the following error:

   ```json
   {
     "message": "Provided Value is not Valid. Exceeded maximum length of 80",
     "field": "Emanifest.generator.name",
     "value": "name value"
   }
   ```

   - Validate the mandatory location address fields:

     - address1 (50 Character maximum)
     - city (25 Character maximum)
     - state.code (2 Character State abbreviation)
     - zip (14 Character maximum)

   - If any of the mandatory location address fields are not provided or invalid, the service generates the following
     error:

   ```json
   {
     "message": "Value is not Provided/Provided Value is not Valid",
     "field": "Emanifest.generator.siteAddress.address1/city/state/zip",
     "value": "address1/city/state/zip value"
   }
   ```

   - Validate the mailing address fields. If country is not provided, the service generates the following warning:

   ```json
   {
     "message": "Field not Provided. Other mailing address fields will be validated assuming this site is located in the US",
     "field": "Emanifest.generator.mailingAddress.country"
   }
   ```

   - If the provided country == US then Following address fields must be provided:

   - address1 (50 Character maximum)
   - city (25 Character Maximum)
   - state.code (2 Character State Abbreviation)
   - zip (14 Character Maximum)

     If any of the mandatory mailing address fields are not provided or invalid, the service generates the following
     error:

   ```json
   {
     "message": "Value is not Provided/Provided Value is not Valid",
     "field": "Emanifest.generator.mailingAddress.address1/city/state/zip",
     "value": "address1/city/state/zip provided value"
   }
   ```

   - If provided country == Canada or Mexico then following applies address fields must be provided:

     - address1 (50 Character maximum)
     - city (25 Character Maximum)
     - zip (50 Character Maximum)

   If any of the mandatory mailing address fields are not provided or invalid, the service generates the following
   error:

   ```json
   {
     "message": "Value is not Provided/Provided Value is not Valid",
     "field": "Emanifest.generator.mailingAddress.address1/city/zip",
     "value": "address1/city/zip provided value"
   }
   ```

   - If provided state.code is not valid, the service generates following warning:

   ```json
   {
     "message": "Provided Value is not Valid",
     "field": "Emanifest.generator.mailingAddress.state.code",
     "value": "address1/city/zip provided value"
   }
   ```

   - If provided country != "United States", "Canada" or "Mexico" then following fields must be provided:

     - address1 (50 Character maximum)
     - city (25 Character Maximum)
     - zip (50 Character Maximum)
       If any of the mandatory mailing address fields are not provided or invalid, the service generates the
       following error:

   ```json
   {
     "message": "Value is not Provided/Provided Value is not Valid",
     "field": "Emanifest.generator.mailingAddress.address1/city/zip",
     "value": "address1/city/zip provided value"
   }
   ```

   3.10. Validate provided Site ID

   - If Site ID is not valid, the service generates the following warning:

   ```json
   {
     "message": "Provided value is not valid. Two Letter Activity Location Code + Up to 10 alphanumeric characters",
     "field": "Emanifest.generator.epaSiteId",
     "value": "EPA Site ID value"
   }
   ```

   - If the Site ID is valid the system checks if the site is registered
   - If the site is registered, the system validates if the provided site address state code matches Site ID activity
     location.

   - If the state code does not match the Site ID activity location, the service generates the following error:
     ```json
     {
       "message": "Location State Code is different than Site Id Activity Location",
       "field": "Emanifest.generator.siteAddress.state.code",
       "value": "site address state code value"
     }
     ```
   - If the site is not registered, the service generates a warning:

   ```json
   {
     "message": "Site with provided EPA Site ID is not registered",
     "field": "Emanifest.generator.epaSiteId",
     "value": "Site ID value"
   }
   ```

   - Store provided Site Information (if no other manifest errors were found)

4. If the Site ID is not provided AND the Site Information is provided, the system performs the
   following steps:
   4.1. Validate the provided Site Information.
   4.1.1. Validate the site name
   4.1.2. If the site name is not valid the service generates the following error:
   {
   "message": "Provided Value is not Valid",
   "field": "Emanifest.generator.name",
   "value": "name value"
   }
   4.1.3. Validate the mandatory site location address fields:
   - address1
   - city
   - state.code
   - zip
     4.1.4. If any of the mandatory location address fields are not provided or invalid, the
     service generates the following error:
     {
     "message": "Value is not Provided/Provided Value is not Valid",
     "field": "Emanifest.generator.siteAddress.address1/city/state/zip",
     "value": "address1/city/state/zip value"
     }
     4.1.5. Validate the mandatory mailing address fields:
   - address1
   - city
   - state.code
   - zip

4.1.6. If any of the mandatory mailing address fields are not provided or invalid, the
service generates the following error:
{
"message": "Value is not Provided/Provided Value is not Valid",
"field": "Emanifest.generator.mailingAddress.address1/city/state/zip",
"value": "address1/city/state/zip provided value"
}
4.2. If the provided Site Information is valid, but the Site ID is not provided, the system
performs the following steps:
4.2.1. The service generates the following warning:
{
"message": "Value is not Provided",
"field": "Emanifest.generator.epaSiteId"
}
4.2.2. Store the provided Site Information (if no other manifest errors were found)
4.3. If the Site Contact Phone number is not provided and site is registered in RCRAInfo, the
system checks if the site has a Contact Phone value registered for the site. If the Contact
Phone is not registered in the system for that site, the system generates the following
error:
{
"message": "Mandatory Field is not provided"
"field": "Emanifest.generator.contact.Phone.number"
}
4.4. If the Site Contact Phone number is provided and registered in RCRAinfo the system checks
that the phone number is in the correct format.
4.4.1. If the provided phone number has valid format the, system will store site contact
phone number into e-Manifest database
4.4.2. If the provided phone number has an incorrect format, the system will store
registered in RCRAInfo Contact Phone number into e-Manifest database and
generates the following warning:
{
"message": "String \"{provided phone value}\" is too long (length: { provided phone value
length}, maximum allowed: 12)",
"field": "Emanifest.generator.contact.phone.number ",
"value": "number value"
}
4.5. If the Site Contact Phone number is provided and registered in RCRAinfo the system checks
that the phone number is in the correct format.
4.5.1. If the provided phone number has valid format, the system will store site contact
phone number into the e-Manifest database
4.5.2. If the provided phone number has an incorrect format, the system generates the
following error:

```

```

```

```
