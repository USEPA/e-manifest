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
