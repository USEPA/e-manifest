# e-Manifest

## Background
The overarching purpose of e-Manifest is to establish a national information technology system that will enable the Agency and the hazardous waste program’s industry and state stakeholders to transition the manifest system from one that is paper-intensive and burdensome to a system that is much more efficient, because it will rely on information technology to track hazardous waste shipments

## Recent Update - Frequently Asked Questions
The e-Manifest team has uploaded an **[Updated FAQ](https://www.epa.gov/e-manifest/frequent-questions-about-e-manifest)**. These are based on user questions through March 2018.

## What is going on
In March of 2018 the team updated the Schema and documentation please review the new documents.

In December of 2017 the web services were updated to include the update service.  Documentation will be updated in the coming weeks.  Registered users can visit the [Swagger](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/) page for more information

In November of 2017 the web services released in June were updated and now include the ability for industry testers to send manifests to EPA.

EPA strongly encourages testing of the services and has provided [sample JSON](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema/manifest-save-return-examples) to get testers started:

Services Available
* Authentication Services and ID/Key Registration
* GET manifest and handler services
* Data look up services
* POST manifest services

Tools for Testers
* [JSON Schema](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema)
* [sample JSON](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema/manifest-save-return-examples) for submitting manifests to EPA, including:

    A [valid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-valid-no-file-example.json) without the need to send an attachment

    A [valid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-valid-with-file-example.json) with the need to send an atachment

    An [invalid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-invalid-example.json) with several errors
    
* Swagger page for testing and documenting the services (See: https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/ (You must be registered as a site manager for a TSDF site to access this site, see Accessing the Test Environment, below.))
* Sample Client for accessing the services (See: https://github.com/USEPA/e-manifest/tree/master/Services-Information/sample-client)

Please note; The test environment for the most part mirrors the handler information in our production environment. When testing, please also make sure your site information is up to date, if it is not please use myRCRAid or your State’s paper notification process to update your site.

## Accessing the Test Environment
Registration:

In order to access the test environment, all users will be required to set up a test account at https://rcrainfopreprod.epa.gov/rcrainfo/.  If you are interested in testing services, please read https://github.com/USEPA/e-manifest/blob/master/Services-Information/Lookup%20and%20Get%20Services%20as%20of%2001%2010.pdf.  Please note, this account will be used for this review and all subsequent reviews and/or testing of e-Manifest software. 

User Registration:

Visit:  https://rcrainfopreprod.epa.gov/rcrainfo/ 
* Click the “Register” link.  
* Click the "Continue to Industry User Registration" button
* Fill out Title and Name and click the "Next" button.
* Create your username, password, and password retrieval questions
* Review and agree to the Terms and Conditions, and click the "Next" button
* Fill out the information for your Organization (not necessarily your site), Job title, phone and email address. 
* Click the "Send Verification Code via Email" button
* After entering the verification code from your email click the "Register" button
* You will be taken to the My Sites page to register your handler(s)

Handler Registration:

If your state is participating in approving e-Manifest test users, you may request access to your handler id(s).  Otherwise please register to use one of our test sites:

VAD000532119, "TEST TSDF OF VA", Virginia 22202 (Generator and TSDF, test site can be used for testing web services.)

VA988177803,  "HEATING AND OIL", Virginia 22033 (Generator Only)

VATEST000001, "TEST TRANSPORTER 1 OF VA", Virginia 22202 (Generator or Transporter)

VATEST000002, "TEST TRANSPORTER 2 OF VA", Virginia 22202 (Generator or Transporter)

VATEST000003, "TEST TSDF OF VA TWO", Virginia 22202  (Generator and TSDF, test site can be used for testing web services.)

VATEST000004, "TEST GENERATOR OF VA", Virginia 22202 (Generator Only)

* On the My Sites page click on the “Add Existing Site” button and search for your EPA ID number in the Site ID box  or a test site and then select that facility. (For example; VA000532119) 
* Request a role for the site.  The 'Site Manager' Role will allow you to use the services.  
* After you submit your request, the request will go to your state or an EPA administrator. Please understand this is not an instant access process and the administrator will need to manually activate your request during normal business hours.  EPA is continuing to work on the concept of a Site Manager which will allow users to manage their own users.

Once you have completed this registration you may use either https://test.epacdx.net/ or https://rcrainfopreprod.epa.gov/rcrainfo/ to log on to the application.

Obtaining an API Key

If you want to register for an API ID and Key to test the services, you may create one by clicking on the 'Tools' menu and API selection.  The API page will allow you to generate your unique API ID and Key.   The API ID and Key can be used to access our web services which are documented at: (https://github.com/USEPA/e-manifest/tree/master/Services-Information) and if logged into e-Manifest at:https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/

Upcoming Iterations

In the upcoming months, we will add more screens and request feedback from States, Brokers, and Transporters.  In addition, we will also release new versions of our Application Programming Interfaces (APIs) for users wishing to implement e-Manifest in their existing manifest systems.


 
## Reference

EPA's [Hazardous Waste Electronic Manifest System (E-Manifest)](https://www.epa.gov/hwgenerators/hazardous-waste-electronic-manifest-system-e-manifest) page 

All our [active cards and issues] (/issues) are posted in this GitHub Repository.  We will be posting additional documents as well as issues that we want user feedback on in the near future.  

Additional Resources: 

[Sample Paper Manifest](https://www.epa.gov/sites/production/files/2015-06/documents/newform.pdf) 

[Paper Manifest Instructions](https://www.epa.gov/sites/production/files/2015-06/documents/man-inst.pdf)


## Project History
In 2014 and 2015 EPA developed a technical architecture for e-Manifest.

Between July of 2015 and March of 2016 EPA developed an initial prototype.  The initial prototype has been decommissioned, but you can see the code for it at (https://github.com/18F/e-manifest).  If you want to see how the initial prototype was built see [the legacy Trello board »](https://e-manifest.epa.gov)

Since April of 2016 e-Manifest has been leveraging modules within the RCRAInfo V6 application, taking advantage of reusing the data and technology that already existed in RCRAInfo.

In February 2017, the team released functional mock ups in our test environment.  

In March and April of 2017, the team released a series of Generator and TSD Facility screens in the test environment.  These screens communicate with our test database.  This also marks the first time users can register to create test manifests for their own handler id.  

In June of 2017 the team released a series of web services, front end screens, and modifications based on responses from user experience testing.  Specifically, we released for user testing and feedback:

1) Changes based on user feedback
2)	Initial web services (See: https://github.com/USEPA/e-manifest/blob/master/Services-Information/Lookup%20and%20Get%20Services%20as%20of%2001%2010.pdf)
* Authentication Services and ID/Key Registration
* Get manifest and handler services
* Data look up services
* Swagger page for testing and documenting the services (See: https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/ (You must be registered to access this site.))
* Sample Client for accessing the services (See: https://github.com/USEPA/e-manifest/tree/master/Services-Information/sample-client)
3)	Generator and TSDF screens and workflow, including adding facilities not in our database
4)	Bulk Signing of manifests (using EPA standard signature services (CDX))

## Contact Information
Additional Questions: emanifest@epa.gov

Join the conversation and keep up on the latest e-Manifest news
The e-Manifest ListServ provides an open forum for the posting and discussion of news and information relating to the e-Manifest program. This Listserv can also be used to facilitate e-Manifest conversations amongst the stakeholder and user community.

General Program listserv

* Subscribe: Send a blank message to: eManifest-subscribe@lists.epa.gov

Developers only listserv (Are you a developer that will consume e-Manifest's APIs?)

* Subscribe: Send a blank message to: e-manifestdev-subscribe@lists.epa.gov
