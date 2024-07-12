# e-Manifest

**You can find our new services documentation
at [https://usepa.github.io/e-manifest/](https://usepa.github.io/e-manifest/)**

## Background

The purpose of e-Manifest is to establish a national information technology system that will enable the
Agency and the hazardous waste program’s industry and state stakeholders to transition the manifest system from one
that is paper-intensive and burdensome to a system that is much more efficient, because it will rely on information
technology to track hazardous waste shipments.

## What is going on

See
our [Release Calendar](https://calendar.google.com/calendar/u/0/htmlembed?src=cbg29nj98u94np3c4pp5vjdph8@group.calendar.google.com&ctz=America/New_York)
for an at-a-glance view of upcoming changes.

For more details on current issues see our [Issues page](https://github.com/USEPA/e-manifest/issues)

- Please see
  the [How e-Manifest uses GitHub Issues](https://github.com/USEPA/e-manifest/blob/master/Reference/How%20e-Manifest%20uses%20GitHub%20Issues.pdf)
  document to see how the e-Manifest team utilizes GitHub issues to communicate what we are working on with the user
  community.

## Tools for Developers and Testers

- [JSON Schema](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema)
- [Sample JSON](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema/manifest-save-return-examples)
  for submitting manifests to EPA, including:

  - A [valid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-valid-Data-and-Image-example.json)
    showing a Data+Image manifest

  - A [valid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-valid-Image-Only-Designated-Facility-example.json)
    showing an Image Only manifest

  - A [valid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/quicker%20sign%20example.json)
    demonstrating Quicker Sign which allows users to sign electronic manifests in their own systems

  - An [invalid example](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/manifest-save-return-examples/emanifest-save-invalid-example.json)
    with several errors

- [Swagger page](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/) for testing and documenting the services
  - You must be registered as a site manager for a TSDF site to access this site. See "Accessing the Test Environment"
    below.
- [Haztrak](https://github.com/USEPA/haztrak) open-source application for electronic manifesting
- [Sample Java application](https://github.com/USEPA/e-manifest/tree/master/sample-client) 
- [Python Client Library](https://github.com/USEPA/e-manifest/tree/master/emanifest-py) 
- [Typescript Client Library](https://github.com/USEPA/e-manifest/tree/master/emanifest-js)

## Accessing the Test Environment

In order to access the test environment, all users will be required to set up a test account on
the [test site](https://rcrainfopreprod.epa.gov/rcrainfo/). If you are interested in testing services, please
read [our services docs](https://usepa.github.io/e-manifest/Intro/registration.html#user-registration). Please note,
this test user account will be used for this review and all subsequent reviews and/or testing of e-Manifest software.

- Once you have completed this registration you may use either https://test.epacdx.net/
  or https://rcrainfopreprod.epa.gov/rcrainfo/ to log on to the application.

## Upcoming Iterations

In the upcoming months, we will add more screens and request feedback from States, Brokers, and Transporters. In
addition, we will also release new versions of our Application Programming Interfaces (APIs) for users wishing to
implement e-Manifest in their existing manifest systems.

## Reference

EPA's [e-Manifest homepage](https://www.epa.gov/e-manifest)

All our [active cards and issues](https://github.com/USEPA/e-manifest/issues) are posted in this GitHub Repository. We
will be posting additional documents as well as issues that we want user feedback on in the near future.

[Sample paper manifest, continuation sheet, and instructions](https://www.epa.gov/hwgenerators/uniform-hazardous-waste-manifest-instructions-sample-form-and-continuation-sheet)

## Contact Information

Additional Questions: [email emanifest@epa.gov](mailto:emanifest@epa.gov)

**Join the conversation and keep up on the latest e-Manifest news**

- Attend the
  next [e-Manifest webinar](https://www.epa.gov/e-manifest/monthly-webinars-about-hazardous-waste-electronic-manifest-e-manifest)

- Sign up for the e-Manifest mailing lists:

  - e-Manifest General
    Program: [Click here to subscribe](https://public.govdelivery.com/accounts/USEPAORCR/subscriber/new?topic_id=USEPAORCR_4)

  - e-Manifest Software
    Developers: [Click here to subscribe](https://public.govdelivery.com/accounts/USEPAORCR/subscriber/new?topic_id=USEPAORCR_9)
