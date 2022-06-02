# e-Manifest

## Background
The overarching purpose of e-Manifest is to establish a national information technology system that will enable the Agency and the hazardous waste program’s industry and state stakeholders to transition the manifest system from one that is paper-intensive and burdensome to a system that is much more efficient, because it will rely on information technology to track hazardous waste shipments.

## Frequently Asked Questions
The e-Manifest team has uploaded an **[Updated FAQ](https://www.epa.gov/e-manifest/frequent-questions-about-e-manifest)**. 

## What is going on
The release calendar can be found here: **[Release Calendar](https://calendar.google.com/calendar/u/0/htmlembed?src=cbg29nj98u94np3c4pp5vjdph8@group.calendar.google.com&ctz=America/New_York)**

For more details on current issues see our [Issues page](https://github.com/USEPA/e-manifest/issues)
* Please see the [How e-Manifest uses GitHub Issues](https://github.com/USEPA/e-manifest/blob/master/Reference/How%20e-Manifest%20uses%20GitHub%20Issues.pdf) document to see how the e-Manifest team utilizes GitHub issues to communicate what we are working on with the user community.

## How to test and what is available
There are ten categories of services available based on your user status:

1. [All users] Authentication services
2. [All users] e-Manifest Lookup Services
3. [All users] Lookup Services
4. [All users] Site Services
5. [Industry users] e-Manifest Services
6. [Industry users] e-Manifest UI Link Services
7. [Regulator users] CM&E Evaluation Services
8. [Regulator users] e-Manifest Services
9. [Regulator users] Handler Services
10. [Regulator users] User Services

**Tools for Testers**
* [JSON Schema](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema)
* [Sample JSON](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema/manifest-save-return-examples) for submitting manifests to EPA, including:

  - A [valid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-valid-Data-and-Image-example.json) showing a Data+Image manifest

  - A [valid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-valid-Image-Only-Designated-Facility-example.json) showing an Image Only manifest

  - An [invalid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-invalid-example.json) with several errors
    
* [Swagger page](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/) for testing and documenting the services
  - You must be registered as a site manager for a TSDF site to access this site. See "Accessing the Test Environment" below.
* [Sample Client](https://github.com/USEPA/e-manifest/tree/master/Services-Information/sample-client) for accessing the services
* Python [**emanifest**](https://github.com/USEPA/e-manifest/tree/master/emanifest-py) package for accessing the services

Please note: The test environment for the most part mirrors the handler information in our production environment. When testing, please also make sure your site information is up to date. If it is not, please use myRCRAid or your state’s paper notification process to update your site in the production environment.

## Accessing the Test Environment
**Registration:**

In order to access the test environment, all users will be required to set up a test account on the [test site](https://rcrainfopreprod.epa.gov/rcrainfo/).  If you are interested in testing services, please read [our services documentation](https://github.com/USEPA/e-manifest/tree/master/Services-Information). Please note, this test user account will be used for this review and all subsequent reviews and/or testing of e-Manifest software. 

**User Registration:**

Visit the [test site](https://rcrainfopreprod.epa.gov/rcrainfo/) 
* Click the “Register” link.  
* Click the "Continue to Industry User Registration" button
* Fill out Title and Name and click the "Next" button.
* Create your username, password, and password retrieval questions
* Review and agree to the Terms and Conditions, and click the "Next" button
* Fill out the information for your Organization (not necessarily your site), Job title, phone and email address. 
* Click the "Send Verification Code via Email" button
* After entering the verification code from your email click the "Register" button
* You will be taken to the My Sites page to register your handler(s)

**Handler Registration:**

If your state is participating in approving e-Manifest test users, you may request access to your handler ID(s).  Otherwise, please register to use one of our test sites:

|    Site ID   |         Site Name        |  State   |  Zip  |      Type of Site      |                 Notes                |
| ------------ | ------------------------ | -------- | ----- | ---------------------- | ------------------------------------ |
| VA988177803  | HEATING AND OIL          | Virginia | 22033 | Generator only         |                                      |
| VATEST000001 | TEST TRANSPORTER 1 OF VA | Virginia | 22202 | Generator, Transporter |                                      |
| VATEST000002 | TEST TRANSPORTER 2 OF VA | Virginia | 22202 | Generator, Transporter |                                      |
| VAD000532119 | TEST TSDF OF VA          | Virginia | 22202 | Generator, TSDF        | Can be used for testing web services |
| VATEST000003 | TEST TSDF OF VA TWO      | Virginia | 22202 | Generator, TSDF        | Can be used for testing web services |
| VATEST000004 | TEST GENERATOR OF VA     | Virginia | 22202 | Generator only         |                                      |

* On the My Sites page, click on the “Add Existing Site” button
* Search for your EPA ID number in the Site ID box or a test site and then select that facility. (For example: VA000532119) 
* Request a role for the site
  - The 'Site Manager' Role will allow you to use the API services.
* After you submit your request, the request will go to your state or an EPA administrator. Please understand this is not an instant access process and the administrator will need to manually activate your request during normal business hours.

* Once you have completed this registration you may use either https://test.epacdx.net/ or https://rcrainfopreprod.epa.gov/rcrainfo/ to log on to the application.

**Obtaining an API Key**

If you want to register for an API ID and key to test the services, you may create one by clicking on the 'Tools' menu and selecting API. The API page will allow you to generate your unique API ID and key. The API ID and Key can be used to access our web services which are documented on the [Services Information page](https://github.com/USEPA/e-manifest/tree/master/Services-Information) and, if logged into e-Manifest, on [Swagger](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/)

**Upcoming Iterations**

In the upcoming months, we will add more screens and request feedback from States, Brokers, and Transporters.  In addition, we will also release new versions of our Application Programming Interfaces (APIs) for users wishing to implement e-Manifest in their existing manifest systems.
 
## Reference

EPA's [Hazardous Waste Electronic Manifest System (E-Manifest)](https://www.epa.gov/hwgenerators/hazardous-waste-electronic-manifest-system-e-manifest) page 

All our [active cards and issues](https://github.com/USEPA/e-manifest/issues) are posted in this GitHub Repository.  We will be posting additional documents as well as issues that we want user feedback on in the near future.  

Additional Resources: 

[Sample Paper Manifest](https://www.epa.gov/sites/production/files/2018-05/documents/uniform_hazardous_waste_manifest.pdf) 

[Paper Manifest Instructions](https://www.epa.gov/sites/production/files/2018-05/documents/instructions_for_completing_the_uniform_hazardous_waste_manifest.pdf)

## Contact Information
Additional Questions: emanifest@epa.gov

If you're interested in contributing to this project, see [CONTRIBUTING.md](https://github.com/USEPA/e-manifest/blob/master/CONTRIBUTING.md)

**Join the conversation and keep up on the latest e-Manifest news**

The e-Manifest ListServ provides an open forum for the posting and discussion of news and information relating to the e-Manifest program. This Listserv can also be used to facilitate e-Manifest conversations amongst the stakeholder and user community.

General Program listserv

* Subscribe: Send a blank message to: join-eManifest@lists.epa.gov

Developers only listserv (Are you a developer that will consume e-Manifest's APIs?)

* Subscribe: Send a blank message to: join-e-manifestdev@lists.epa.gov

Attend the next [e-Manifest webinar](https://www.epa.gov/e-manifest/monthly-webinars-about-hazardous-waste-electronic-manifest-e-manifest)
