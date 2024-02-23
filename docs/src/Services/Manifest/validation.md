# Manifest Field Validations

The following validations are performed on the manifest fields:

## Generator information validation for the Image submission type manifests

The manifest fee will be determined based on the Generator signature date (if provided).

1. Generator information and Generator signature date can be provided for Image submission type
   manifests for the save and update services. See modification details in sections Facility
   Information Validation for `Image` submission type, Generator Site ID and Site Information
   Validation and Paper Signature Info Validation. If Generator information and Generator printed
   signature date is provided and data is valid, the following applies

   - 1.1. The save and update services will store this data as a part of the manifest

   - 1.2. The services will set `Emanifest.provideImageGeneratorInfo = true`

   - 1.3. The manifest fee will be determined based on the Generator printed signature date upon electronic signature
     from
     the receiving facility

2. If Generator information and Generator printed signature date is not provided or some of the
   provided data is invalid, the following applies

   - 2.1. The save and update services will generate the following warning:

   ```json
   {
     "message": "Not all required Generator site and signature information is provided so system cannot determine which price to charge for this manifest. To ensure that this manifest is billed accurately, please update the manifest with all required generator site and signature information.",
     "field": "Emanifest.generator"
   }
   ```

   - 2.2. The save and update services will also generate warning(s)

   - 2.3. The services will not store Generator information as a part of the manifest data

   - 2.4. The services will set `Emanifest.provideImageGeneratorInfo` = false

   - 2.5. The manifest fee will be determined based on the receiving facility electronic signature date

## Facility Information Validation for "Image" submission type

1. For the Image submission type, one of the following facility EPA Site IDs must be provided: Designated Facility EPA
   Site ID, Generator EPA Site ID, or Alternate Designated Facility Site ID
2. The following Facility EPA site IDs shall be provided for the following scenarios:
   - Original Manifest, no Full Rejection: Designated Facility EPA Site ID shall be provided.
   - Original Manifest, Full Rejection to Alternate Designated Facility: Alternate Designated Facility EPA Site ID
     shall be provided.
   - Original Manifest, Full Rejection to the Generator: Designated Facility EPA site ID shall be provided.
   - New Manifest shipping waste back to original Generator (New Manifest is the manifest created as a "result" of the
     Original manifest rejection or residue): Generator Facility EPA site ID shall be provided. This EPA site ID shall
     contain the Original Designated Facility Site ID.
   - New Manifest shipping rejected waste to another Designated Facility: Designated Facility EPA site ID shall be
     provided.
3. If one of the following IDs: `Emanifest.designatedFacility.epaSiteID` and `Emanifest.generator.epaSiteId` and
   `Emanifest.rejectionInfo.alternateDesignatedFacility.siteId` is not provided then the service will return an
   authorization error.
4. If the provided EPA SiteIDis not registered, then the service will return an authorization error.
5. If `Emanifest.designatedFacility.epaSiteId` or `Emanifest.generator.epaSiteId` or
   `Emanifest.rejectionInfo.alternateDesignatedFacility.siteId` is provided, the following applies

   - 5.1. If any of the following Site information is provided then the service generates the following warning:

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

   - 5.2. Validation of the Contact information is identical to #2 in section

   - 5.3. Designated Facility (TSDF)/Generator Site ID and Site Information Validation

   - 5.4. If `Emanifest.wastes` are provided then the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored.",
     "field": "Emanifest.wastes"
   }
   ```

   - 5.5. If `Emanifest.residue == true` then the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.residue = false will be assigned",
     "field": "Emanifest.residue",
     "value": "residue value"
   }
   ```

   - 5.6. If `Emanifest.import == true` then the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.import = false will be assigned",
     "field": "Emanifest.import",
     "value": "import value"
   }
   ```

   - 5.7. The service stores following information as a part of the manifest data:

   - `Emanifest.residue = false`
   - `Emanifest.import = false`

6. If `Emanifest.designatedFacility.epaSiteId` or `Emanifest.generator.epaSiteId` is provided then the
   following applies

   - 6.1. If `Emanifest.rejection == true`, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejection = false will be assigned",
     "field": "Emanifest.rejection",
     "value": " rejection value"
   }
   ```

   - 6.2. If any of the `Emanifest.rejectionInfo` fields are provided, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored.",
     "field": "Emanifest.rejectionInfo.{field}",
     "value": "field value"
   }
   ```

7. If `Emanifest.designatedFacility.epaSiteId` or `Emanifest.rejectionInfo.alternateDesignatedFacility.siteId` is
   provided, the following applies

   - 7.1. If `Emanifest.containsPreviousRejectOrResidue == true`, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.containsPreviousRejectOrResidue = false will be assigned",
     "field": "Emanifest.containsPreviousRejectOrResidue",
     "value": "containsPreviousRejectOrResidue value"
   }
   ```

8. If `Emanifest.rejectionInfo.alternateDesignatedFacility.siteId` is provided, the following applies

   - 8.1. If `Emanifest.rejection == false`, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejection = true will be assigned",
     "field": "Emanifest.rejection",
     "value": " rejection value"
   }
   ```

   - 8.2. If `Emanifest.rejectionInfo.transporterOnSite == false`, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejectionInfo.transporterOnSite = true will be assigned",
     "field": "Emanifest.rejectionInfo.transporterOnSite",
     "value": "rejectionInfo.transporterOnSite value"
   }
   ```

   - 8.3. If `Emanifest.rejectionInfo.rejectionType == "PartiaReject"`, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejectionInfo.rejectionType = 'FullReject' will be assigned",
     "field": "Emanifest.rejectionInfo.rejectionType",
     "value": "rejectionInfo.rejectionType value"
   }
   ```

   - 8.4. If `Emanifest.rejectionInfo.alternateDesignatedFacilityType == "Generator"` the service generates the
     following
     warning:

   ```json
   {
     "message": "Provided Value will be Ignored. Emanifest.rejectionInfo.alternateDesignatedFacilityType = 'Tsdf' will be assigned",
     "field": "Emanifest.rejectionInfo.alternateDesignatedFacilityType",
     "value": "rejectionInfo.alternateDesignatedFacilityType value"
   }
   ```

   - 8.5. If rejectionInfo.newManifestTrackingNumbers are provided, the service generates the following warning:

   ```json
   {
     "message": "Provided Value will be Ignored. New Manifest(s) are not created if Transporter is On Site",
     "field": "Emanifest.rejectionInfo.newManifestTrackingNumbers",
     "value": "rejectionInfo.newManifestTrackingNumbers value"
   }
   ```

   - 8.6. The service stores following information as a part of the manifest data:

     - `Emanifest.rejection = true`
     - `Emanifest.rejectionInfo.transporterOnSite = true`
     - `Emanifest.rejectionInfo.rejectionType = "FullReject"`
     - `Emanifest.rejectionInfo.alternateDesignatedFacilityType = "Tsdf"`

## Transporter Information Validation

1. If `submissionType` is `FullElectronic` or `Hybrid`, then the Transporter is valid if the Transporter is registered
   in RCRAInfo and the Transporter has at least one User with the e-Manifest Certifier Role and this user has a Received
   ESA.

   - 1.1. If the Transporter Site ID is not provided, the service generates schema validation error.
   - 1.2. If the Transporter Site ID has an invalid format, the service generates schema validation error.
   - 1.3. If the Transporter Site ID is not registered, the service generates the following error:
     ```json
     {
       "message": "For FullElectronic submission type registered Transporter Site Id must be provided",
       "field": "Emanifest.transporter.epaSiteId",
       "value": "Site ID value"
     }
     ```
   - 1.4. If the Transporter Site ID is registered and there are no users with the e-Manifest Certifier role for the
     provided Transporter, the service generates the following error:
     ```json
     {
       "message": "Site doesn't have any users with Certifier role or with ESA status 'Received",
       "field": "Emanifest.transporter.epaSiteId",
       "value": "Site ID value"
     }
     ```
   - 1.5. If the Transporter Site ID is registered and there are no users with a received ESA, the service generates
     the following error:
     ```json
     {
       "message": "Site doesn't have any users with Certifier role or with ESA status 'Received",
       "field": "Emanifest.transporter.epaSiteId",
       "value": "Site ID value"
     }
     ```

2. If `submissionType` is `DataImage5Copy`, then registered and non-registered Transporters are valid.

   - 2.1. If the Transporter is registered in RCRAInfo as a Transporter, then only the `epaSiteId` must be provided.
     All
     the site information will be obtained from RCRAInfo. If other site information is provided it will be ignored with
     warnings.
   - 2.2. If the Transporter is not registered in RCRAInfo, then the following site information must be provided:
     - Site Address
     - Site Name
     - Contact phone
   - 2.3. If Site ID AND Site Information are not provided, the system generates errors.

     ```json
     {
       "message": "Value is not provided",
       "field": "Emanifest.transporter.epaSiteId"
     }
     ```

     ```json
     {
       "message": "Value is not provided",
       "field": "Emanifest.transporter.siteAddress"
     }
     ```

     ```json
     {
       "message": "Mandatory field is not provided",
       "field": "Emanifest.transporter.name"
     }
     ```

     ```json
     {
       "message": "Value is not provided",
       "field": "Emanifest.transporter.contact.phone.number"
     }
     ```

   - 2.4. If Site ID is provided AND Site Information is not provided, the system performs the following steps:

     - 2.4.1. Validate Site ID format.
     - 2.4.2. If Site ID is not valid, the service generates the following error:

     ```json
     {
       "message": "Provided Value is not Valid. Does not match format of: Two Letter Activity Location Code + Up to 10 alphanumeric characters",
       "field": "Emanifest.transporter.epaSiteId"
     }
     ```

     - 2.4.3. If the Site ID is valid, the system will search in RCRAInfo by Site ID. - 2.4.4. If the site is found,
       the system obtains Site Information from RCRAInfo and stores it into the Manifest. - 2.4.5. If the site is not
       found, the service generates the following error:

     ```json
     {
       "message": "Site with the provided EPA Site ID is not registered",
       "field": "Emanifest.transporter.epaSiteId"
     }
     ```

   - 2.5. If the Site ID is provided AND Site Information is provided, the site information will be ignored with
     warnings,
     and the system will perform the following steps:

     - 2.5.1. Validate provided Site ID.
     - 2.5.2. If Site ID is not valid, the service generates an error:
       ```json
       {
         "message": "Provided value is not valid. Does not match format of: Two Letter Activity Location Code + Up to 10 alphanumeric characters",
         "field": "Emanifest.transporter.epaSiteId",
         "value": "EPA Site ID value"
       }
       ```
     - 2.5.3. If Site ID is valid, check if the site is registered.
     - 2.5.4. If the site is not registered, the service generates a warning:

       ```json
       {
         "message": "Site with provided EPA Site ID is not registered",
         "field": "Emanifest.transporter.epaSiteId",
         "value": "Site ID value"
       }
       ```

   - 2.6. If Site ID is not provided AND Site Information is provided, the system will perform the following
     steps:

     - 2.6.1. Validate the provided Site Information.
     - 2.6.2. Validate the Site Name.
     - 2.6.3. If the Site Name is not valid, the service generates the following error:

       ```json
       {
         "message": "Provided Value is not Valid",
         "field": "Emanifest.transporter.name",
         "value": "site name value"
       }
       ```

     - 2.6.4. Validate the mandatory site address fields: - address1 (50 Character maximum) - city (25
       Character
       maximum) - state.code (2 Character State Abbreviation) - zip (14 Character maximum)
     - 2.6.5. If any of the mandatory location address fields are not provided or invalid, the service generates
       the following error:

       ```json
       {
         "message": "Value is not Provided/Provided Value is not Valid",
         "field": "Emanifest.transporter.siteAddress.address1/city/state/zip",
         "value": "address1/city/state/zip value"
       }
       ```

   - 2.7. If `Emanifest.submissionType` is `Hybrid` or `FullElectronic` and `Emanifest.status > Scheduled` and provided
     transporter information is different from currently stored, the service generates the following warning:

     ```json
     {
       "message": "Provided Transporter information will be ignored. Transporter Information cannot be updated if the manifest status is InTransit or thereafter",
       "field": "Emanifest.transporter.epaSiteId"
     }
     ```

## Designated Facility (TSDF)/Generator Site Information Validation

1. If `submissionType` is `FullElectronic` and `status >= Scheduled` then the following applies

   - 1.1. If `Emanifest.generator.epaSiteId` is not provided then the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.generator.epaSiteId"
   }
   ```

   - 1.2. If `Emanifest.generator.epaSiteId` has an incorrect format then the service generates the following error:

   ```json
   {
     "message": "Invalid Field Format",
     "field": "Emanifest. generator.epaSiteId",
     "value": " epa siteIDvalue"
   }
   ```

   - 1.3. If `Emanifest.generator.epaSiteId` is not registered in RCRAInfo then the service generates the following
     error:

   ```json
   {
     "message": "Provided Generator FacilityIDis not registered in RCRAInfo",
     "field": "Emanifest. generator.epaSiteId",
     "value": " epa siteIDvalue"
   }
   ```

2. If `submissionType` is `FullElectronic` or `Hybrid` and `status >= Scheduled`, or `submissionType`
   is `DataImage5Copy`
   then
   the following applies

   - 2.1. If `Emanifest.designatedFacility.epaSiteId` is not provided then the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.designatedFacility.epaSiteId"
   }
   ```

   - 2.2. If `Emanifest.designatedFacility.epaSiteId` has an incorrect format then service generates the following
     error:

   ```json
   {
     "message": "Invalid Field Format",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": " epa siteIDvalue"
   }
   ```

   - 2.3. If `Emanifest.designatedFacility.epaSiteId` is not registered in RCRAInfo then service generates the
     following error:

   ```json
   {
     "message": "Provided Designated FacilityIDis not registered in RCRAInfo",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": " epa siteIDvalue"
   }
   ```

   - 2.4. If the Site Contact Phone number is not provided and registered in RCRAInfo Site does not contain the Site
     Contact Phone Number, the system generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.designatedFacility.contact.phone.number"
   }
   ```

   - 2.5. If the Site Contact Phone number is provided, the system will check the format.

     - If the provided phone number has a valid format the system will store site contact phone number into
       e-Manifest
       database
     - If the provided phone number has an incorrect format the system generates the following warning:

   ```json
   {
     "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
     "field": "Emanifest.designatedFacility.contact.phone.number",
     "value": "number value"
   }
   ```

   - 2.6. If the Site Contact Phone Extension is provided, the system will check the format.

     - 2.6.1 If provided phone extension has a valid format, the system will store the site contact phone extension
       into e-Manifest database
     - 2.6.2 If the provided phone has an incorrect format, the system generates the following warning:

       ```json
       {
         "message": "String \"{provided phone extension value}\" is too long (length: {provided phone value length}, maximum allowed: 6 )",
         "field": "Emanifest.designatedFacility.contact.phone.extension",
         "value": "extension value"
       }
       ```

   - 2.7. If any of the following TSDF Site Information entities were provided:

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

   - 2.8. If the user is authorized to use the e-Manifest Save service for the provided Generator SiteID(It means that
     TSDF acts as Generator), then the provided SiteIDwas already validated during authorization and the system will
     perform following steps:

   - 2.9. If the Site Contact Phone number is not provided in the JSON and site the is registered in RCRAInfo, the
     system checks if the site has a Contact Phone value registered for the site. If the Contact Phone is not
     registered in the system for that site, the system generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.designatedFacility.contact.phone.number"
   }
   ```

   - 2.10. If the Site Contact Phone number is provided and registered in RCRAinfo the system checks that the phone
     number is in the correct format.

     - 2.10.1. If the provided phone number has a valid format, the system will store site contact phone number into
       the e-Manifest database

     - 2.10.2. If provided phone number has an incorrect format, the system will store registered in RCRAInfo Contact
       Phone number into e-Manifest database and generate the following warning:

     ```json
     {
       "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
       "field": "Emanifest.designatedFacility.contact.phone.number",
       "value": "number value"
     }
     ```

   - 2.11. If the Site Contact Phone number is provided and registered in RCRAinfo site does not contain Contact Phone.

     - 2.11.1. If the provided phone number has valid format, the system will store site contact phone number into
       e-Manifest database
     - 2.11.2. If provided phone number has incorrect format, the system generates the following error:

     ```json
     {
       "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
       "field": "Emanifest.designatedFacility.contact.phone.number",
       "value": "number value"
     }
     ```

   - 2.12. Validate emergency phone

     - 2.12.1. If emergency phone number is not provided, the system generates the following error:

     ```json
     {
       "message": "Mandatory Field is not provided",
       "field": "Emanifest.designatedFacility.emergencyPhone.number"
     }
     ```

     - 2.12.2. If emergency phone number is provided and has an invalid format, the system generates the following
       error:

     ```json
     {
       "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 12)",
       "field": "Emanifest.designatedFacility.emergencyPhone.number ",
       "value": "phone number value"
     }
     ```

     - 2.12.3. If emergency phone extension is provided and has an invalid format, the system generates the following
       warning:

     ```json
     {
       "message": "String \"{provided phone value}\" is too long (length: { provided phone value length}, maximum allowed: 6)",
       "field": "Emanifest.generator.emergencyPhone.extension ",
       "value": "extension value"
     }
     ```

     - 2.13. If Site Name, Site Location, Site Mailing Address are provided, the system generates the following
       warning:

     ```json
     {
       "message": "Provided Values will be Ignored. RCRAInfo values will be used",
       "field": "Emanifest.generator.name/mailingAddress/siteAddress ",
       "value": "name/mailingAddress/siteAddress value"
     }
     ```

   - 2.14. If the contact email was provided, the system will check the format

     - 2.14.1. If provided contact email has a valid format the system will store site contact email into e-Manifest
       database
     - 2.14.2. If the provided contact email has an incorrect format the system generates the following warning:

     ```json
     {
       "message": "Invalid Field format. Valid email format is expected.",
       "field": "Emanifest.designatedFacility.contact.email",
       "value": "email value"
     }
     ```

## New Manifest Information Validation

1. If the New Manifest is created for shipping the waste to another TSDF or back to the Generator

   - If `Emanifest.status >= "ReadyForSignature"` and `Emanifest.containsPreviousRejectOrResidue` is not provided then
     the service generates the following error:
     ```json
     {
       "message": "Mandatory Field is not Provided.",
       "field": "Emanifest.containsPreviousRejectOrResidue"
     }
     ```
   - If `Emanifest.containsPreviousRejectOrResidue == true` and `Emanifest.additionalInfo.newManifestDestination` is
     not provided then the service generates the following error:
     ```json
     {
       "message": "Mandatory Field is not Provided.",
       "field": "Emanifest.additionalInfo.newManifestDestination"
     }
     ```
   - If `Emanifest.containsPreviousRejectOrResidue == true`
     and`Emanifest.additionalInfo.originalManifestTrackingNumbers` are not valid the service generates the following
     warning:
     ```json
     {
       "message": "Invalid value provided. Provided Field will be ignored.",
       "field": "Emanifest.additionalInfo.originalManifestTrackingNumbers",
       "value": "provided value"
     }
     ```
   - If `Emanifest.additionalInfo.newManifestDestination == "OriginalGenerator"` and
     `Emanifest.rejection == true` the service generates the following errors:
     ```json
     {
       "message": "New Manifest cannot be rejected if shipped back to the original Generator",
       "field": "Emanifest.additionalInfo.newManifestDestination",
       "value": "newManifestDestination value"
     }
     ```
     ```json
     {
       "message": "New Manifest cannot be rejected if shipped back to the original Generator",
       "field": "Emanifest.rejection",
       "value": "rejection value"
     }
     ```

## Generator Site Information Validation

1. If `submissionType` is `FullElectronic` then the Generator is valid if the Generator SiteIDis registered in RCRAInfo
   and the Generator has at least one User with the e-Manifest Certifier Role and this user has a Received ESA.
2. If `submissionType` is `FullElectronic` the following applies

   - 2.1. If the Generator SiteIDis not provided, the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided. For FullElectronic submission type registered Generator SiteIDmust be provided",
     "field": "Emanifest.designatedFacility.epaSiteId"
   }
   ```

   - 2.2. If the Generator SiteID has an invalid format the service generates the following error:

   ```json
   {
     "message": "Invalid Field Format. For FullElectronic submission type registered Generator SiteIDmust be provided",
     "field": "Emanifest.generator.epaSiteId",
     "value": "SiteIDvalue"
   }
   ```

   - 2.3. If the Generator SiteIDis not registered in RCRAInfo the service generates the following error:

   ```json
   {
     "message": "Provided Generator FacilityIDis not registered in RCRAInfo",
     "field": "Emanifest.generator.epaSiteId",
     "value": "SiteIDvalue"
   }
   ```

   - 2.4. If the Generator SiteIDis registered in RCRAInfo and there are no users with the e-Manifest Certifier role
     for
     the provided Generator the service generates the following error:

   ```json
   {
     "message": "Site doesn't have any users with Certifier role or with ESA status Received",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": "SiteIDvalue"
   }
   ```

   - 2.5. If the Generator with the provided SiteIDis registered and there are no users with a received ESA, the
     service
     generates the following error:

   ```json
   {
     "message": "Site doesn't have any users with Certifier role or with ESA status Received",
     "field": "Emanifest.designatedFacility.epaSiteId",
     "value": "SiteIDvalue"
   }
   ```

3. If `submissionType` is `DataImage5Copy` or `Hybrid`, then registered and non-registered Generators are valid and the
   following cases are possible for the Generator SiteID and Generator Information:

   - 3.1. If the Generator is registered in RCRAInfo and service requester does not intend to provide different (than
     registered) Site Information, then only the epaSiteId shall be provided. All site information will be obtained
     from
     RCRAInfo.

   - 3.2. If the Generator is registered in RCRAInfo and service requester intends to provide different (than
     registered)
     Site Information, then the following site information entities must be provided:

   - Site ID
   - Site Name
   - Site Address (all fields)
   - Mailing Address (all fields)
   - Contact Phone
   - Provided Site Information will be validated and if valid will be stored in e-Manifest.

     - 3.3. If Generator is not registered in RCRAInfo, then following site information must be provided:

   - Site Name
   - Site Address (all fields)
   - Mailing Address (all fields)
   - Contact phone

     Requester also can provide SiteID which is an optional field for this case. If Site ID is provided,
     the system will check if there is a registered Generator for the provided Site ID

     - 3.4. For all above cases Emergency Phone Number must be provided

     - 3.5. If the manifest status is InTransit or thereafter then Generator information cannot be updated.

     - 3.6. If different from currently stored Generator information is provided, the service generates the following
       warning:

   ```json
   {
     "message": "Provided Generator information will be ignored. Generator Information cannot be updated if the manifest status is InTransit or thereafter",
     "field": "Emanifest.generator"
   }
   ```

   - 3.7. If the Site ID is not provided AND any of the mandatory Site information entities are not provided, the
     service
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

   - 3.8. If the Site ID is provided AND Site Address information is not provided, the system performs the following
     steps:

   - If Site ID is not valid the service generates the following error:

   ```json
   {
     "message": "Provided Value is not Valid. Does not match format of: Two Letter Activity Location Code + Up to 10 alphanumeric characters",
     "field": "Emanifest.generator.epaSiteId ",
     "value": "EPA siteIDvalue"
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

   - 3.9. If the Site ID is provided and the Site Information entities are provided, the system performs the following
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

   - If the provided `country == US` then Following address fields must be provided:

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

   - If provided `country == Canada` or Mexico then following applies address fields must be provided:

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

## Paper Signature Info Validation

1. If `submissionType` is `FullElectronic` and any (Transporter(s), designatedFacility) of the paperSignature
   Information (printedName or signatureDate) is provided, the service generates a warning:

   ```json
   {
     "message": "Provided Field will be ignored. Paper Signature Information is not applicable for FullElectronic/Image submission type",
     "field": "Emanifest. transporter/designatedFacility.paperSignatureInfo",
     "value": "printedName or signatureDate value"
   }
   ```

2. If `submissionType` is `Hybrid` and `Emanifest.status > Scheduled` and `generator.PaperSignature` is provided, the
   service
   generates the following warning:

   ```json
   {
     "message": "Provided value will be ignored. Generator paper signature Date/Printed Name shall not be provided after Scheduled status.",
     "field": "emanifest.generatorPaperSignature.signatureDate/printedName",
     "value": " value"
   }
   ```

3. If `submissionType` is `Image`, the following applies:

   - 3.1. If Generator Printed Name is not provided, the service generates a warning:

   ```json
   {
     "message": "Field is not Provided",
     "field": "Emanifest.generator.paperSignature.printedName"
   }
   ```

   - 3.2. If the Generator Printed Name is provided, validate the format. If an invalid format is provided, the service
     generates the following warning:

   ```json
   {
     "message": "String \"{provided printed name value}\" is too long (length: { provided printed name length}, maximum allowed: 255)",
     "field": "Emanifest.generator.paperSignature.printedName",
     "value": "value"
   }
   ```

   - 3.3. If the Generator Signature Date is not provided, the service generates the following warning:

   ```json
   {
     "message": "Field is not Provided",
     "field": "Emanifest.generator.paperSignatureInfo.signatureDate"
   }
   ```

   - 3.4. If Generator Signature Date is provided, validate format. If format is invalid the service generates the
     following warning:

   ```json
   {
     "message": "String \"{provided signature date}\" is invalid against requested date format(s) [yyyy-MM-dd'T'HH:mm:ssZ, yyyy-MM-dd'T'HH:mm:ss.SSSZ]",
     "field": "Emanifest.generator.paperSignatureInfo. signatureDate",
     "value": "value"
   }
   ```

   - 3.5. If provided Generator Signature Date is later than `Emanifest.createdDate` the service generates the
     following
     warning:

   ```json
   {
     "message": "Provided Generator Signature Date is later than manifest created Date",
     "field": "Emanifest.generator.paperSignatureInfo.signatureDate",
     "value": "value"
   }
   ```

4. If `submissionType` is "`DataImage5Copy`", the following applies:

   - 4.1. If Generator/Transporter/designatedFacility Printed Names are not provided, the service generates a warning:

   ```json
   {
     "message": "Field is not Provided",
     "field": "Emanifest.generator/transporter/designatedFacility.paperSignature.printedName"
   }
   ```

   - 4.2. If the Generator/Transporter/designatedFacility Printed Names are provided, validate the format. If an
     invalid
     format is provided, the service generates the following error:

   ```json
   {
     "message": "String \"{provided printed name value}\" is too long (length: { provided printed name length}, maximum allowed: 255)",
     "field": "Emanifest.generator/transporter/designatedFacility.paperSignature.printedName",
     "value": "value"
   }
   ```

   - 4.3. If the Generator/Transporter/designatedFacility Signature Dates are not provided, the service generates the
     following error

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.generator/transporter/designatedFacility.paperSignatureInfo.signatureDate"
   }
   ```

   - 4.4. If Generator/Transporter/TSDF Signature Dates are provided, validate format. If format is invalid the service
     generates the following error (for this example: TSDF is used)

   ```json
   {
     "message": "String \"{provided signature date}\" is invalid against requested date format(s) [yyyy-MM-dd'T'HH:mm:ssZ, yyyy-MM-dd'T'HH:mm:ss.SSSZ]",
     "field": "Emanifest.generator/transporter/designatedFacility.paperSignatureInfo.signatureDate",
     "value": "value"
   }
   ```

5. The system will perform the following validation for consecutive of Signature Dates for `DataImage5Copy`:

   - 5.1. If the signature dates for Generator, all Transporters, and designated Facility are provided and have a valid
     format, and more than one transporter is provided, the system performs the following steps:

   - Check if Generator signatureDate <= First Transporter signature date (Transporter.order will be used to determine
     consecutive of transporters). If not, the service generates the following error:

   ```json
   {
     "message": "Transporter Signature date must be on or after Generator Signature date",
     "field": "Emanifest.generator.paperSignatureInfo.signatureDate",
     "value": "Generator Signature Date value"
   }
   ```

   ```json
   {
     "message": "Generator Signature Date must be earlier or the same date as the first Transporter Signature Date",
     "field": "Emanifest.transporter.paperSignatureInfo.signatureDate",
     "value": "Transporter Signature Date value"
   }
   ```

   - Check the order of the Transporters signature dates. If there is more than one Transporter provided, check if
     signature dates of transporters are in order or the same. For example, if there are two transporters and the
     signature date of transporter which has order = 2 is earlier than signature date of transporter with order = 1,
     the service generates the following error:

   ```json
   {
     "message": "Signature Date of previous transporter must be before this transporter's signature date",
     "field": "Emanifest.transporters[1].paperSignatureInfo.signatureDate",
     "value": " Second Transporter Signature Date value "
   }
   ```

   - 5.1.3. Check if the Designated Facility signature date >= Last Transporter signature date. If not, the service
     generates the following error:

   ```json
   {
     "message": "Signature of designated facility must be on or after the last transporter's signature date",
     "field": "Emanifest.designatedFacility.paperSignatureInfo.signatureDate",
     "value": "Designated Facility Signature Date value "
   }
   ```

   - 5.1.4. If any of the Signature Dates > current date the service generates the following error:

   ```json
   {
     "message": "Generator/Transporter/Designated Facility Signature Date cannot be in the future",
     "field": "Emanifest.generator/transporter/designatedFacility.paperSignatureInfo.signatureDate",
     "value": "Signature Date value"
   }
   ```

   - 5.2. If `Emanifest.rejectionInfo.rejectionType = "FullReject"`
     and `Emanifest.rejectionInfo.transporterOnsite == true`
     the following applies

   - If `Emanifest.rejectionInfo.alternateDesignatedFacilityType == "Tsdf"` the following applies
   - If `Emanifest.rejectionInfo.alternateDesignatedFacility.paperSignatureInfo.signatureDate` is not provided, the
     service generates the following error:

   ```json
   {
     "message": "Mandatory field is not provided",
     "field": "Emanifest.rejectionInfo.alternateDesignatedFacility.paperSignatureInfo.signatureDate"
   }
   ```

   - If `Emanifest.rejectionInfo.alternateDesignatedFacility.paperSignatureInfo.printed` Name is not provided, the
     service generates the following error:

   ```json
   {
     "message": "Mandatory field is not provided",
     "field": "Emanifest.rejectionInfo.alternateDesignatedFacility.paperSignatureInfo.printedName"
   }
   ```

   - If `Emanifest.rejectionInfo.alternateDesignatedFacility.paperSignatureInfo.signatureDate` is invalid the service
     generates the following error:

   ```json
   {
     "message": "String \"{provided signature date}\" is invalid against requested date format(s) [yyyy-MM-dd'T'HH:mm:ssZ, yyyy-MM-dd'T'HH:mm:ss.SSSZ]",
     "field": "Emanifest.rejectionInfo.alternateDesignatedFacility.paperSignatureInfo.signatureDate",
     "value": "value"
   }
   ```

   - If `Emanifest.rejectionInfo.alternateDesignatedFacility.paperSignatureInfo.signatureDate <
Emanifest.designatedFacility.paperSignatureInfo.signatureDate` then the service generates the following error:

   ```json
   {
     "message": "Signature of alternate designated facility must be on or after the designated facility’s signature date",
     "field": "Emanifest.designatedFacility.paperSignatureInfo.signatureDate",
     "value": "Alternate Designated Facility Signature Date value "
   }
   ```

   - If `Emanifest.rejectionInfo.alternateDesignatedFacilityType == "Generator"` the following applies

   - If Emanifest.rejectionInfo.generator.paperSignatureInfo.signatureDate is not provided, the service generates the
     following error:

   ```json
   {
     "message": "Mandatory field is not provided",
     "field": "Emanifest.rejectionInfo.generator.PaperSignatureInfo.signatureDate"
   }
   ```

   - If Emanifest.rejectionInfo.generator.paperSignatureInfo.printedName is not provided, the service generates the
     following error:

   ```json
   {
     "message": "Mandatory field is not provided",
     "field": "Emanifest.rejectionInfo. generator.paperSignatureInfo.printedName"
   }
   ```

   - If Emanifest.rejectionInfo.generator.paperSignatureInfo.signatureDate is invalid the service generates the
     following error:

   ```json
   {
     "message": "String \"{provided signature date}\" is invalid against requested date format(s) [yyyy-MM-dd'T'HH:mm:ssZ, yyyy-MM-dd'T'HH:mm:ss.SSSZ]",
     "field": "Emanifest.rejectionInfo.generator.paperSignatureInfo.signatureDate",
     "value": "value"
   }
   ```

   - If Emanifest.rejectionInfo.generator.paperSignatureInfo.signatureDate <
     Emanifest.designatedFacility.paperSignatureInfo.signatureDate then the service generates the following error:

   ```json
   {
     "message": "Invalid Value. Generator Signature Date must be the same or later than Designated Facility Signature Date",
     "field": " Emanifest.rejectionInfo. generator.paperSignatureInfo.signatureDate",
     "value": "value"
   }
   ```

## Waste Validation

1. If the waste field is not provided for a manifest with status >= `Scheduled`. The service generates the following
   error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.waste"
   }
   ```

2. If the waste element is provided, the system will perform the following steps:

   - 2.1. If `waste.dotHazardous` is not provided, the service generates the following error:
     ```json
     {
       "message": "Object has missing required properties (['dotHazardous'])",
       "field": "Emanifest.wastes.{i}.dotHazardous"
     }
     ```
   - 2.2. If `waste.epaWaste` is not provided, the service generates the following error:
     ```json
     {
       "message": "Object has missing required properties (['epaWaste'])",
       "field": "Emanifest.waste.{i}.epaWaste"
     }
     ```
   - 2.3. If `waste.pcb` is not provided, the service generates the following error:
     ```json
     {
       "message": "Object has missing required properties (['pcb'])",
       "field": "Emanifest.waste.{i}.pcb"
     }
     ```
   - 2.4. If `waste.pcb` is true, then the system will validate `pcbInfos`. See details in PCB Information Validation
     section.
   - 2.5. If `waste.br` is not provided, the service generates the following error:
     ```json
     {
       "message": "Object has missing required properties (['br'])",
       "field": "Emanifest.waste.{i}.br"
     }
     ```
   - 2.6. If the `waste.br` is true, the system will validate `brInfo`. See details in Biennial Report Information
     Validation section.
   - 2.7. Validate `dotInformation/wasteDescription`.

     - 2.7.1. If the element `dotHazardous` is true, the waste must contain `dotInformation`.
     - 2.7.2. If the element `dotHazardous` is false, the waste must contain `wasteDescription`.
     - 2.7.3. If the element `dotHazardous` is true, and `dotInformation` is not provided, the service generates the
       following error:
       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.waste.dotInformation"
       }
       ```
     - 2.7.4. If the element `dotHazardous` is true and `dotInformation` is provided, the service will validate
       the `dotInformation` fields. See section DOT Information fields validation for details.
     - 2.7.5. If the element `dotHazardous` is false and `dotInformation` is provided, the service generates the
       following warning:
       ```json
       {
         "message": "For non-hazardous Waste Dot Information will be ignored.",
         "field": "Emanifest.waste.dotInformation"
       }
       ```
     - 2.7.6. If the element `dotHazardous` is false and the element `wasteDescription` is not provided, then the
       service
       generates the following error:
       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.waste.wasteDescription"
       }
       ```
     - 2.7.7. If the element `dotHazardous` is false and the element `wasteDescription` is provided, then the service
       validates `wasteDescription`. If `wasteDescription` is not valid, the service generates the following error:
       ```json
       {
         "message": "Invalid Field format. Value of no longer than 500 characters is expected",
         "field": "Emanifest.waste.wasteDescription",
         "value": "wasteDescription value"
       }
       ```
     - 2.7.8. If the element `dotHazardous` is true and the element `wasteDescription` is provided, the service
       generates
       the following warning:

       ```json
       {
         "message": "For hazardous Waste, wasteDescription will be ignored.",
         "field": "Emanifest.waste.wasteDescription"
       }
       ```

   - 2.8 Validate Management Method Code. See section Management Method Code Validation for details
   - 2.9 Validate Waste.consentNumber
     - 2.9.1 if Emanifest.import is true, Waste.consentNumber can be provided at any status.
     - 2.91. if Emanifest.import is false, Waste.consentNumber shall not be provided.
   - 2.10 Validate DOT Information. See that section for further details
   - 2.11 Validate Containers and Quantity. See that section for further details
   - 2.12 Validate Hazardous Waste Codes. See that section for further details
   - 2.13Validate Instructions and Additional Information. See that section for further details
   - 2.14 Validate Biennial Report Information. See that section for further details

## DOT Information Fields Validation

The system will perform the following steps on the DOT Information fields:

1. Validate ID Number
   - There are Proper Shipping Names which do not have corresponding ID Numbers in the DOT specifications. For these
     Proper Shipping Names the Emanifest requires ID Number value of
     "NOID"
   - If dotInformation.IdNumber is not provided, the service generates the following error:
   ```json
   {
     "message": "Mandatory Field is Not Provided",
     "field": "Emanifest.wastes.dotInformation.idNumber "
   }
   ```
   - If dotInformation.IdNumber is provided and not found in Id Number Lookup, the service generates the following
     error:
   ```json
   {
     "message": "Provided Value is not Found",
     "field": "Emanifest.wastes.dotInformation.IdNumber",
     "value": "value ofIDNumber"
   }
   ```
2. Validate Printed Dot Information.
   - If printedDotInformation is not provided, the service generates the following error:
   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.wastes.dotInformation.printedDotInformation "
   }
   ```
   - If printedDotInformation exceeds the 500-character limit, the service generates the following error:
   ```json
   {
     "message": "Invalid Field Format. Printed Dot Information exceeds the 500 character length",
     "field": "Emanifest.wastes.dotInformation.printedDotInformation ",
     "value": "value of printedDotInformation"
   }
   ```

## Containers and quantity fields validation

1. Containers and Quantity fields are mandatory
2. If the quantity entity is not provided, the system generates the following error:
   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.waste.quantity"
   }
   ```
3. If any of the Containers and Quantity fields are not provided, the service generates the following error:
   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.waste.quantity.containerNumber/containerType/quantity/quantityUnitOfMeasurement"
   }
   ```
4. If the element containerNumber is provided, the service validates containerNumber format. If
   format is not valid the service generates the following error:
   ```json
   {
     "message": "Numeric instance is greater than the required maximum (maximum: 9999, found:{provided container number})",
     "field": "Emanifest.wastes.quantity.containerNumber",
     "value": "value of container number"
   }
   ```
5. If the element containerType code is provided, the service validates the containerType code. If
   containerType code is not valid the service generates the following error:
   ```json
   {
     "message": "Instance value (\"AB\") not found in enum (possible values: [\"BA\",\"DT\",\"CF\",\"DW\",\"CM\",\"HG\",\"CW\",\"TC\",\"CY\",\"TP\",\"DF\",\"TT\",\"DM\"])",
     "field": "Emanifest.wastes.quantity.containerType.code",
     "value": "value of container type code "
   }
   ```
6. If the element quantity is provided, the service validates the quantity format. If the format is not valid the
   service generates the following error:
   ```json
   {
     "message": " Numeric instance is greater than the required maximum (maximum: 99999999999, found: {provided quantity})",
     "field": "Emanifest.wastes.quantity.quantity ",
     "value": "value of quantity "
   }
   ```
7. If the quantityUnitOfMeasurement code is provided, the service validates the quantityUnitOfMeasurement code. If the
   quantityUnitOfMeasurement code is not valid, the service generates the following error:

```json
{
  "message": "Instance value (\"{provided code}\") not found in enum (possible values: [\"P\",\"T\",\"K\",\"M\",\"G\",\"L\",\"Y\",\"N\"])",
  "field": "Emanifest.wastes.quantity.quantityUnitOfMeasurement.code ",
  "value": "value of container type"
}
```

## Waste Additional Information Validation

1. All Additional Information fields are optional. If any of the fields are invalid, they will be ignored with a
   warning.
2. Handling Instructions Validation.

   - If handling instructions is invalid, the service generates the following warning:

   ```json
   {
     "message": "Invalid Field format. Text can be no longer than 4000 characters",
     "field": "Emanifest.wastes.additionalInformation.handlingInstructions",
     "value": "value of handling instructions"
   }
   ```

3. Comments Validation

   - 3.1. handlerId validation
     - 3.1.1. If the handler Id is not provided, then the comment will be ignored and generate the following warning:
       ```json
       {
         "message": "Comment will be ignored. Field is not Provided",
         "field": "Emanifest.wastes[i].additionalInfo.comments.handlerId"
       }
       ```
     - 3.1.2. If the handlerId has an invalid format provided, then the comment will be ignored and generate the
       following warning:
       ```json
       {
         "message": "Comment will be ignored, due to an invalid Site ID format being submitted",
         "field": "Emanifest.wastes[i].additionalInfo.comments.handlerId",
         "value": "Handler ID value"
       }
       ```
     - 3.1.3. If the provided handlerId does not match the Generator or TSDF or any of Transporter Site IDs in the
       manifest, the comment will be ignored and generate the following warning:
       ```json
       {
         "message": "Comment will be ignored. Provided handlerId does not match Generator or TSDF or any of Transporter Site IDs",
         "field": "Emanifest.wastes[i].additionalInfo.comments.handlerId",
         "value": "Handler ID value"
       }
       ```
   - 3.2. Label validation

     - 3.2.1. If the label element is not provided, then the comment will be ignored and generate the following
       warning:
       ```json
       {
         "message": "Comment will be ignored. Field is not Provided",
         "field": "Emanifest.wastes[i].additionalInfo.comments.label"
       }
       ```
     - 3.2.2. If the label element has an invalid format provided, then the comment will be ignored and generate the
       following warning:

       ```json
       {
         "message": "Comment will be ignored. Invalid Value. Text can be no longer than 250 characters.",
         "field": "Emanifest.wastes[i].additionalInfo.comments.label",
         "value": "Label value"
       }
       ```

   - 3.3. Description validation

     - 3.3.1. If the description element is not provided, then the comment will be ignored and generate the following
       warning:
       ```json
       {
         "message": "Comment will be ignored. Field is not Provided",
         "field": "Emanifest.wastes[i].additionalInfo.comments.description"
       }
       ```
     - 3.3.2. If the description element has an invalid format, the provided comment will be ignored and generate the
       following warning:

       ```json
       {
         "message": "Comment will be ignored. Invalid Value. Text can be no longer than 250 characters.",
         "field": "Emanifest.wastes[i].additionalInfo.comments.description",
         "value": "Description value"
       }
       ```

   - 3.4. If originalManifestTrackingNumbers are provided then the service generates the following warning:
     ```json
     {
       "message": "originalManifestTrackingNumbers will be ignored. This field shall not be provided for the Waste.additionalInfo",
       "field": "Emanifest.wastes[i].additionalInfo.originalManifestTrackingNumbers",
       "value": "originalManifestTrackingNumbers value"
     }
     ```
   - 3.5. If newManifestDestination is provided then the service generates the following warning:

   ```json
   {
     "message": "newManifestDestination will be ignored. This field shall not be provided for the Waste.additionalInfo",
     "field": "Emanifest.wastes[i].additionalInfo.newManifestDestination",
     "value": "newManifestDestination value"
   }
   ```

## PCB Information Validation

1. If `pcb` is `false` and any of the `pcbInfos` entities or fields are provided, the service generates the following
   warning:

   ```json
   {
     "message": "Provided value will be ignored. PcbInfos provided but pcb flag equals false",
     "field": "Emanifest.waste.pcbInfos",
     "value": "pcbsInfo value"
   }
   ```

2. If `pcb` is `true` and `pcbInfos` are not provided, the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided",
     "field": "Emanifest.waste.pcbInfos"
   }
   ```

3. If at least one `PcbInfos` element is provided, then the service validates pcbInfo fields

   - 3.1. Validate `PcbInfos.loadType.code`

     - 3.1.1. If `PcbInfos.loadType` is not provided, the service generates the following error:
       ```json
       {
         "message": "Mandatory Field is not Provided",
         "field": "Emanifest.wastes.pcbInfos.loadType.code"
       }
       ```
     - 3.1.2. If `pcbInfos.loadType.code` is provided, the service validates it against LoadType lookup. If the field
       is not valid, the service generates the following error:
       ```json
       {
         "message": "Invalid Field Format. One of the following values is expected: 'Container', 'ArticleInContainer', 'ArticleNotInContainer', 'BulkWaste'",
         "field": "Emanifest.waste.pcbInfos.loadType.code",
         "value": "loadType.code value"
       }
       ```

   - 3.2. Validate `pcbInfos.articleContainerId`

     - 3.2.1. If `pcbInfos.loadType.code` is "Container", "ArticleInContainer", or "ArticleNotInContainer"
       and `PcbInfos.articleContainerId` is not provided, the service generates the following error:
       ```json
       {
         "message": "Mandatory Field is not Provided. Fields must be provided if PCB load type is 'Container', 'ArticleInContainer', or 'ArticleNotInContainer'",
         "field": "Emanifest.waste.pcbInfos.articleContainerId"
       }
       ```
     - 3.2.2. If `pcbInfos.articleContainerId` is provided, the service checks the field length. If the field is
       invalid, the service generates the following error:
       ```json
       {
         "message": "Invalid Field Format. Text no longer than 255 characters is expected",
         "field": "Emanifest.waste.pcbInfos.articleContainerId",
         "value": "articleContainerId value"
       }
       ```
     - 3.2.3. If `pcbInfos.loadType.code` is "BulkWaste" and `articleContainerId` is provided, then the service
       generates the following warning:
       ```json
       {
         "message": "Field will be ignored",
         "field": "Emanifest.waste.pcbInfos.articleContainerId",
         "value": "articleContainerId value"
       }
       ```

   - 3.3. Validate `PcbInfo.dateOfRemoval`

     - 3.3.1. If `pcbInfos.dateOfRemoval` is not provided, the service generates the following error:
       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.waste.pcbInfos.dateOfRemoval"
       }
       ```
     - 3.3.2. If `PcbInfos.dateOfRemoval` is provided, the service validates field format. If the field format is
       invalid, the service generates the following error:
       ```json
       {
         "message": "Invalid Field Format.",
         "field": "Emanifest.waste.pcbInfos.dateOfRemoval",
         "value": "dateOfRemoval value"
       }
       ```

   - 3.4. Validate `pcbInfos.weight`

     - 3.4.1. If `pcbInfos.weight` is not provided, the service generates the following error:
       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.waste.pcbInfos.weight"
       }
       ```
     - 3.4.2. If `PcbInfos.weight` is provided, the service validates field format. If the field format is invalid,
       the
       service generates the following error:
       ```json
       {
         "message": "Invalid Field Format. Value containing no more than 11 whole digit(s) and 6 decimal digit(s) is expected",
         "field": "Emanifest.waste.pcbInfo.weight",
         "value": "weight value"
       }
       ```

   - 3.5. Validate `PcbInfos.wasteType`

     - 3.5.1. If `pcbInfos.loadType` is "Container" or "ArticleInContainer" and `wasteType` is not provided, the
       service
       generates the following error:
       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.waste.pcbInfos.wasteType"
       }
       ```
     - 3.5.2. If `PcbInfos.loadType` is "BulkWaste" and `wasteType` is provided, the service generates the following
       warning:
       ```json
       {
         "message": "Field will be ignored",
         "field": "Emanifest.waste.pcbInfos.wasteType",
         "value": "containerType value"
       }
       ```
     - 3.5.3. If `PcbInfos.wasteType` is provided, the service checks the field length. If the field is invalid, the
       service generates the following error:
       ```json
       {
         "message": "Invalid Field Format. Text no longer than 255 characters is expected",
         "field": "Emanifest.waste.pcbInfos.wasteType",
         "value": "containerType value"
       }
       ```

   - 3.6. Validate `PcbInfos.bulkIdentity`
     - 3.6.1. If `PcbInfos.loadType` is "BulkWaste" and `bulkIdentity` is not provided, the service generates the
       following error:
       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.waste.pcbInfos.bulkIdentity"
       }
       ```
     - 3.6.2. If `PcbInfos.loadType` is "Container" or "ArticleInContainer" and `bulkIdentity` is provided, the
       service
       generates the following warning:
       ```json
       {
         "message": "Field will be ignored",
         "field": "Emanifest.waste.pcbInfos.bulkIdentity",
         "value": "bulkIdentity value"
       }
       ```
     - 3.6.3. If `PcbInfos.bulkIdentity` is provided, the service checks the field length. If the field is invalid,
       the
       service generates the following error:
       ```json
       {
         "message": "Invalid Field Format. Text no longer than 255 characters is expected",
         "field": "Emanifest.waste.pcbInfos. bulkIdentity",
         "value": "bulkIdentity value"
       }
       ```

## Management Method Code Validation

1. If `submissionType` is `DataImage5Copy` the following applies

   - 1.1. If `epaWaste` is `true` and `Waste.managementMethod.code` is not provided, the service generates the
     following error:
     ```json
     {
       "message": "Field is Not Provided",
       "field": "Emanifest.wastes.managementMethod.code"
     }
     ```
   - 1.2. If the `Waste.managementMethod.code` is provided, validate if the code is in the lookup. If the provided code
     is not found, the service generates the following error:
     ```json
     {
       "message": "Provided Value not Found",
       "field": "Emanifest.wastes.managementMethod.code",
       "value": "code value"
     }
     ```

2. If `submissionType` is `FullElectronic` or `Hybrid` the following applies

   - 2.1. If `Emanifest.status` is "Scheduled," "InTransit," or "ReadyForSignature," the following applies

     - 2.1.1. If the `Waste.managementMethod.code` is provided, validate if the code is in the lookup. If the
       provided code is not found, the service generates a warning:
       ```json
       {
         "message": "Provided Value not Found",
         "field": "Emanifest.wastes.managementMethod.code",
         "value": "code value"
       }
       ```

   - 2.2. If `Emanifest.status` is "Signed," the following applies
     - 2.2.1. If the `Waste.managementMethod.code` is provided, then the service updates `Emanifest.validationStatus`
       to `true`
     - 2.2.2. If the `Waste.managementMethod.code` is not provided, the service generates the following error:
       ```json
       {
         "message": "Field is Not Provided",
         "field": "Emanifest.wastes.managementMethod.code"
       }
       ```
     - 2.2.3. If the `Waste.managementMethod.code` is provided, validate if the code is in the lookup. If the
       provided code is not found, the service generates the following error:
       ```json
       {
         "message": "Provided Value not Found",
         "field": "Emanifest.wastes.managementMethod.code",
         "value": "code value"
       }
       ```

## Rejection Information Validation

1. If an Original Manifest is rejected then Emanifest.rejection shall be specified as "true".

2. Emanifest.rejection and RejectionInfo shall be provided at the "ReadyForSignature" status. If provided for earlier
   statuses these fields will be ignored.

   - 2.1 If Emanifest.status < "ReadyForSignature" and either Emanifest.rejection or RejectionInfo fields are provided
     then the service generates the following warning:
     ```json
     {
       "message": "Provided Field will be ignored. Rejection information shall be provided at ReadyForSignature status",
       "field": "Emanifest.rejection",
       "value": "provided value"
     }
     ```

3. If submissionStatus >= "ReadyForSignature" and Emanifest.rejection is not provided then the service generates the
   following error:

   ```json
   {
     "message": "Mandatory Field is not Provided.",
     "field": "Emanifest.rejection"
   }
   ```

4. Emanifest.containsPreviousRejectOrResidue is not provided then the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided.",
     "field": "Emanifest.containsPreviousRejectOrResidue"
   }
   ```

5. If `Emanifest.rejection == true` then the following applies

   - 5.1. If `RejectionInfo.rejectionComments` is not provided then the service generates the following error:

     ```json
     {
       "message": "Mandatory Field is not Provided.",
       "field": "Emanifest.RejectionInfo. rejectionComments"
     }
     ```

   - 5.2. If RejectionInfo.rejectionComments are not valid then the service generates the following error:

     ```json
     {
       "message": "String \"{provided rejection comments value}\" is too long (length: { provided rejection comments length}, maximum allowed: 255)",
       "field": "Emanifest.RejectionInfo.rejectionComments",
       "vale": "rejectionComments value"
     }
     ```

   - 5.3. If RejectionInfo.transporterOnSite is not provided then the service generates the following error:

     ```json
     {
       "message": "Mandatory Field is not Provided.",
       "field": "Emanifest.RejectionInfo.transporterOnSite"
     }
     ```

   - 5.4. If RejectionInfo.transporterOnSite is provided and not valid then the service generates the following error:

     ```json
     {
       "message": "Invalid Field Format. Boolean value is expected",
       "field": "Emanifest.RejectionInfo.transporterOnSite",
       "value": "transporterOnSite value"
     }
     ```

   - 5.4. If `Emanifest.submissionType == "DataImage5Copy"` and `RejectionInfo.transporterOnSite == true` the following
     applies

   - 5.4.1. If `RejectionInfo.rejectionType == "PartialReject"` then the service
     sets `RejectionInfo.rejectionType = "FullReject"` and generates the following warning:

     ```json
     {
       "message": "Provided value will be Ignored. If Transporter is On Site rejection type must be 'FullReject'",
       "field": "Emanifest.RejectionInfo.rejectionType",
       "value": "rejectionType value"
     }
     ```

   - 5.4.2. e-Manifest sets rejectionInfo.rejectionType as "FullReject" in the e-Manifest database

   - 5.4.3. If RejectionInfo.newManifestTrackingNumbers is provided then the service generates the following warning:

     ```json
     {
       "message": "Provided Field will be Ignored. New Manifest(s) are not created if Transporter is On Site",
       "field": "Emanifest.RejectionInfo.newManifestTrackingNumbers"
     }
     ```

   - 5.4.4. If RejectionInfo.alternateDesignatedFacilityType is not provided then the service generates the following
     error:

     ```json
     {
       "message": "Mandatory Field is not Provided.",
       "field": "Emanifest.RejectionInfo.alternateDesignatedFacilityType"
     }
     ```

   - 5.4.5. If `RejectionInfo.alternateDesignatedFacilityType == "Generator` then the following applies

     - 5.4.5.1. If `generatorPaperSignatureInfo.printedName` is not provided then the service generates the following
       warning:

       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.RejectionInfo.generatorPaperSignature.printedName "
       }
       ```

     - 5.4.5.2. If generatorPaperSignature.printedName has an invalid format then the service generates the following
       warning:

       ```json
       {
         "message": "String \"{provided printed name value}\" is too long (length: {provided printed name length}, maximum allowed: 255)",
         "field": "Emanifest.RejectionInfo.generatorPaperSignature.printedName ",
         "value": "printedName value"
       }
       ```

     - 5.4.5.3. If generatorPaperSignature.signatureDate is not provided then the service generates the following
       error:

       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.RejectionInfo.generatorPaperSignature.signatureDate "
       }
       ```

     - 5.4.5.4. If generatorPaperSignature.signatureDate < Emanifest.designatedFacility.paperSignature.signatureDate
       then the service generates the following error:

       ```json
       {
         "message": "Invalid Value Provided. Generator signature date (signing as alternate Facility) shall be on or later than TSDF signature",
         "field": "Emanifest.RejectionInfo.generatorPaperSignature.signatureDate ",
         "value": "signatureDate value"
       }
       ```

     - 5.4.5.5. If generatorPaperSignature.signatureDate > current Date then the service generates the following
       error:

       ```json
       {
         "message": "Invalid Value Provided. Generator signature date (signing as alternate Facility) cannot be in the future",
         "field": "Emanifest.RejectionInfo.generatorPaperSignature.signatureDate ",
         "value": "signatureDate value"
       }
       ```

   - 5.4.6. If `RejectionInfo.alternateDesignatedFacilityType == "Tsdf"` the following applies

     - 5.4.6.1. If `RejectionInfo.alternateDesignatedFacility.epaSiteId` is not provided then the service generates
       the
       following error:

       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.RejectionInfo. alternateDesignatedFacility.epaSiteId"
       }
       ```

     - 5.4.6.2. If RejectionInfo.alternateDesignatedFacility.epaSiteId has an invalid format then the service
       generates
       the following error:

       ```json
       {
         "message": "Provided Value is not Valid. Does not match the format of: Two Letter Activity Location Code + Up to 10 alphanumeric characters",
         "field": "Emanifest.RejectionInfo.alternateDesignatedFacility.epaSiteId",
         "value": "epaSiteId value"
       }
       ```

     - 5.4.6.3. If epaSiteId is valid, the system will search RCRAInfo by Site ID. If the Site ID is found the system
       will obtain the Site information from RCRAInfo and store it into the Manifest.

     - 5.4.6.4. If the epaSiteId is not found, the service generates the following error:

       ```json
       {
         "message": "Provided Value is not Found",
         "field": "Emanifest.RejectionInfo.alternateDesignatedFacility.epaSiteId",
         "value": "epaSiteId value"
       }
       ```

     - 5.5. If `Emanifest.submissionType` is `FullElectronic` or `Hybrid` and provided
       `RejectionInfo.transporterOnSite == true`
       then the service generates the following warning:

     ```json
     {
       "message": "Provided Value will be ignored",
       "field": "Emanifest.rejectionInfo.transporterOnSite",
       "value": "transporterOnSite value"
     }
     ```

   - 5.6. If `RejectionInfo.transporterOnSite == false` the following applies

     - 5.6.1. If `RejectionInfo.rejectionType` is not provided then the service generates the following error:

       ```json
       {
         "message": "Mandatory Field is not Provided.",
         "field": "Emanifest.RejectionInfo.rejectionType"
       }
       ```

     - 5.6.2. If RejectionInfo.newManifestTrackingNumber(s) is provided and not valid, the service generates the
       following error:

       ```json
       {
         "message": "Invalid Field Format. 9 digits followed by 3 upper case letters is expected",
         "field": "Emanifest.RejectionInfo.newManifestTrackingNumbers",
         "value": "newManifestTrackingNumber value"
       }
       ```

     - 5.6.3. If manifestTrackingNumber has a valid format, the service checks if the provided manifestTrackingNumber
       suffix is valid. If the suffix is invalid, the service generates the following error:

       ```json
       {
         "message": "Invalid Manifest Tracking Number Suffix is Provided",
         "field": "Emanifest.RejectionInfo.newManifestTrackingNumber",
         "value": "manifestTrackingNumber value"
       }
       ```

     - 5.6.4. If any of the following fields are provided:

       - RejectionInfo.alternateDesignatedFacilityType
       - RejectionInfo.generatorPaperSignature
       - RejectionInfo.alternateDesignatedFacility
         the service generates the following warning:

       ```json
       {
         "message": "Provided Field will be Ignored. alternateDesignatedFacilityType/generatorPaperSignature/alternateDesignatedFacility not applicable if Transporter is Off Site",
         "field": "Emanifest.RejectionInfo.alternateDesignatedFacilityType/generatorPaperSignature/alternateDesignatedFacility",
         "value": "alternateDesignatedFacilityType/generatorPaperSignature/alternateDesignatedFacility value"
       }
       ```

6. If `Emanifest.rejection == false` and If any of the following `RejectionInfo` fields are provided:

   - RejectionInfo.rejectionType
   - RejectionInfo.transporterOnSite
   - RejectionInfo.alternateDesignatedFacilityType
   - RejectionInfo.generatorPaperSignature
   - RejectionInfo.alternateDesignatedFacility
     the service generates the following warning:

   ```json
   {
     "message": "Provided Field will be Ignored. {Field} not applicable if Manifest is not Rejected",
     "field": "Emanifest.RejectionInfo.rejectionType /transporterOnSite/alternateDesignatedFacilityType/generatorPaperSignature/alternateDesignatedFacility",
     "value": "rejectionType/transporterOnSite/alternateDesignatedFacilityType/generatorPaperSignature/alternateDesignatedFacility value"
   }
   ```

## Discrepancy Information Validation

1. If status >= ReadyForSignature and DiscrepancyResidueInfo.wasteQuantity is not provided then the service generates
   the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided.",
     "field": "Emanifest.discrepancyResidueInfo.wasteQuantity"
   }
   ```

2. If status >= ReadyForSignature and DiscrepancyResidueInfo.wasteType is not provided then the service generates the
   following error:

   ```json
   {
     "message": "Mandatory Field is not Provided.",
     "field": "Emanifest.discrepancyResidueInfo.wasteType"
   }
   ```

3. If `DiscrepancyResidueInfo.wasteQuantity == true` or `DiscrepancyResidueInfo.wasteType == true` and
   `DiscrepancyResidueInfo.discrepancyComments` is not provided then the service generates the following error:

   ```json
   {
     "message": "Mandatory Field is not Provided.",
     "field": "Emanifest.discrepancyResidueInfo.discrepancyComments"
   }
   ```

4. If DiscrepancyResidueInfo.discrepancyComments has an invalid format then the service generates the following error:

   ```json
   {
     "message": "String \"{provided discrepancyComments value}\" is too long (length: {provided discrepancyComments value length}, maximum allowed: 255)",
     "field": "Emanifest.discrepancyResidueInfo.discrepancyComments",
     "value": "discrepancyComments value"
   }
   ```

5. If `DiscrepancyResidueInfo.wasteQuantity == false` and `DiscrepancyResidueInfo.wasteType == false` and
   `DiscrepancyResidueInfo.discrepancyComments` is provided then the service generates the following warning:

   ```json
   {
     "message": "Provided Field will be Ignored.",
     "field": "Emanifest.discrepancyResidueInfo.discrepancyComments",
     "value": "discrepancyComments value"
   }
   ```

6. If `DiscrepancyResidueInfo.wasteQuantity == true` or `DiscrepancyResidueInfo.wasteType == true` then the service sets
   `Emanifest.discrepancy = true`

7. If `DiscrepancyResidueInfo.wasteQuantity == false` and `DiscrepancyResidueInfo.wasteType == false` then the service
   sets `Emanifest.discrepancy`

## Residue Information Validation

1. If status >= ReadyForSignature and DiscrepancyResidueInfo.residue is not provided, then the service generates the
   following error:

   ```json
   {
     "message": "Mandatory Field is not Provided.",
     "field": "Emanifest.discrepancyResidueInfo.residue"
   }
   ```

2. If `DiscrepancyResidueInfo.residue == true` and `DiscrepancyResidueInfo.residueComments` is provided, the service
   validates if `DiscrepancyResidueInfo.residueComments` has valid format. If `DiscrepancyResidueInfo.residueComments`
   has
   invalid format, the service generates the following error:

   ```json
   {
     "message": "String \"{provided residueComments value}\" is too long (length: {provided residueComments value length}, maximum allowed: 255)",
     "field": "Emanifest.discrepancyResidueInfo.residueComments",
     "value": "residueComments value"
   }
   ```

3. If `DiscrepancyResidueInfo.residue == false` and `DiscrepancyResidueInfo.residueComments` is provided, then the
   service
   generates the following warning:

   ```json
   {
     "message": "Provided Field will be Ignored.",
     "field": "Emanifest.discrepancyResidueInfo.residueComments",
     "value": "residueComments value"
   }
   ```

4. If `DiscrepancyResidueInfo.residue == true` then the service sets `Emanifest.residue = true`
5. If `DiscrepancyResidueInfo.residue == true` then the `Emanifest.residueNewManifestTrackingNumber(s)` can be provided.

   - 5.1. If no `Emanifest.residueNewManifestTrackingNumber(s)` is provided, the service generates the following
     warning:

     ```json
     {
       "message": "One of the Waste has residue. Manifest Tracking Number(s) for shipping waste to another Facility(ies) is not provided",
       "field": "Emanifest.residueNewManifestTrackingNumber",
       "value": "residueNewManifestTrackingNumber value"
     }
     ```

   - 5.2. If Emanifest.residueNewManifestTrackingNumber(s) are provided then the service validates the format of
     residueNewManifestTrackingNumber(s). If it has an invalid format, the service generates the following warning:

     ```json
     {
       "message": "Field will be ignored. Invalid Field Format. 9 digits followed by 3 upper case letters is expected",
       "field": "Emanifest.residueNewManifestTrackingNumbers",
       "value": "residueNewManifestTrackingNumbers value"
     }
     ```

   - 5.3. If the residueNewManifestTrackingNumber has a valid format, the service checks if the provided
     residueNewManifestTrackingNumber suffix is valid. If the suffix is invalid, the service generates the following
     warning:
     ```json
     {
       "message": "Field will be ignored. Invalid Manifest Tracking Number Suffix is Provided",
       "field": "Emanifest.residueNewManifestTrackingNumber",
       "value": "residueNewManifestTrackingNumber value"
     }
     ```

## Biennial Report Validation

# JSON

1. If the `Waste.br == true` and the Waste.brInfo is not provided or empty, then the following applies

   - 1.1. The system generates the following warning:
     ```json
     {
       "message": "If brInfo is not Provided/Provided brInfo contains no fields, provided br shall be false",
       "field": "Emanifest.waste.br",
       "value": "Emanifest.waste.br value"
     }
     ```
   - 1.2. The system sets `Waste.br = false` and stores it as a part of the manifest

2. If the `Waste.br == true` and none of the provided `Waste.brInfo` fields are valid, then the following applies

   - 2.1. The system generates the following warning:
     ```json
     {
       "message": "None of the provided brInfo are valid, provided br will be set to false",
       "field": "Emanifest.waste.br",
       "value": "Emanifest.waste.br value"
     }
     ```
   - 2.2. The system sets Waste.br = false and stores it as a part of the manifest

3. If `Waste.br == false` or not provided and at least one of the provided Waste.brInfo fields is valid, then the
   following applies:

   - 3.1. The system generates the following warning:
     ```json
     {
       "message": "Provided brInfo is valid, provided br will be set to true",
       "field": "Emanifest.waste.br",
       "value": "Emanifest.waste.br value"
     }
     ```
   - 3.2. The system sets Waste.br = true and stores it as a part of the manifest

4. If `Waste.br == true` and Waste.brInfo fields are provided, then the following applies:

5. Source Codes

   - 5.1. Validate Source Code

     - 5.1.1. If the Source Code is not provided, the service generates the following warning:
       ```json
       {
         "message": "Field is not Provided",
         "field": "Emanifest.waste.brInfo.sourceCode.code"
       }
       ```

   - 5.2. Validate Form Code

     - 5.2.1. If Form Code is not provided, the service generates the following warning:
       ```json
       {
         "message": "Field is not Provided",
         "field": "Emanifest.waste.brInfo.formCode.code"
       }
       ```

   - 5.3. Validate Waste Minimization Code

     - 5.3.1. If Waste Minimization is not provided, the service generates the following warning:
       ```json
       {
         "message": "Field is not Provided",
         "field": "Emanifest.waste.brInfo.wasteMinimization.code"
       }
       ```

   - 5.4. Validate Density and Density Units Of Measurement

     - 5.4.1. If Waste.UnitOfMeasurement.code is not G, L, Y, or N (volumes), then the following applies:

       - 5.4.1.1. If Density is provided, the service generates the following warning:
         ```json
         {
           "message": "Provided field will be ignored. Density shall be provided only if the quantity units of measurement is the volume (G, L, N, Y)",
           "field": "Emanifest.waste.brInfo.density",
           "value": "density value"
         }
         ```
       - 5.4.1.2. If Density Units Of Measurement is provided, the service generates the following warning:

         ```json
         {
           "message": "Provided field will be ignored. Units Of Measurement shall be provided only if the quantity units of measurement is the volume (G, L, N, Y)",
           "field": "Emanifest.waste.brInfo.densityUnitOfMeasurement",
           "value": "densityUnitOfMeasurement value"
         }
         ```

       - 5.4.2. If Waste.UnitOfMeasurement.code is G, L, Y, or N (volumes), then the following applies:

         - 5.4.2.1. The service will store the provided density and the densityUnitOfMeasurement.code if both are
           valid.
         - 5.4.2.2. The service will not store the valid density if densityUnitOfMeasurement.code is not provided
           or
           provided densityUnitOfMeasurement.code is not valid.
         - 5.4.2.3. The service will not store the valid densityUnitOfMeasurement.code if density is not provided
           or
           provided density is not valid.
         - 5.4.2.4. If Density and densityUnitOfMeasurement.code are not provided, the system will generate a
           warning:

           ```json
           {
             "message": "Density and densityUnitOfMeasurement.code are not provided. Both fields – Density and densityUnitOfMeasurement.code fields shall be provided",
             "field": "Emanifest.waste.brInfo.density densityUnitOfMeasurement.code"
           }
           ```

       - 5.4.2.5. If either Density or densityUnitOfMeasurement.code is not provided, the system will generate a
         warning:

         ```json
         {
           "message": "Density.densityUnitOfMeasurement.code is not provided. Both fields – Density and densityUnitOfMeasurement.code fields shall be provided",
           "field": "Emanifest.waste.brInfo.density"
         }
         ```

       - 5.4.2.6. If provided Density is invalid, the service generates the following warning:

         ```json
         {
           "message": "Invalid Field Format. Numeric value containing no more than 3 whole digit(s) and 2 decimal digit(s) expected",
           "field": "Emanifest.waste.brInfo.density",
           "value": "density value"
         }
         ```

       - 5.4.2.7. If provided densityUnitOfMeasurement.code is not valid, the service generates the following
         warning:

         ```json
         {
           "message": "Invalid Field Format. Numeric value 1 ('lbs/gal') or 2 ('sg') shall be provided",
           "field": "Emanifest.waste.brInfo.densityUnitOfMeasurement.code",
           "value": "code value"
         }
         ```
