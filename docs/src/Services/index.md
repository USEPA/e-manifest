# Web Services

RCRAInfo exposes a set of web services that allow industry and regulators to interact with the system programmatically.
These services implement a RESTful design and can be categorized by the resource exposed and the type of user accessing
The service. The services are secured using a [token-based authentication system](./authentication.md).

1. [All users] [Authentication services](authentication.md)
2. [All users] [e-Manifest Lookup Services](./Lookup/e-manifest-lookup.md)
3. [All users] [Lookup Services](./Lookup/lookup.md)
4. [All users] [Site Services](./Site)
5. [All users] [User Services](./user.md)
6. [Industry users] [e-Manifest Services](Manifest/save.md)
7. [Industry users] [e-Manifest UI Link Services](./Manifest/ui-link.md)
8. [Regulator users] CM&E Evaluation Services
9. [Regulator users] [e-Manifest Services](Manifest/states.md)
10. [Regulator users] [Handler Services](./site-handler.md)
11. [Regulator users] [User Services](./user.md)

## Base URL

Developers can access the services on both the Production and Pre-Production environments using the following base URLs:

### Production

- Hostname: `https://rcrainfo.epa.gov`
- Base Path: `/rcrainfoprod/rest`
- example: `https://rcrainfo.epa.gov/rcrainfoprod/rest/api/v1/lookup/federal-waste-codes`

### Pre-Production

- Hostname: `https://rcrainfopreprod.epa.gov`
- Base Path: `/rcrainfo/rest`
- example: `https://rcrainfopreprod.epa.gov/rcrainfo/rest/api/v1/lookup/federal-waste-codes`

The RCRAInfo Production services should not be used for testing. Conversely, actions performed in the Pre-Production
environment will not be reflected in the Production environment, cannot be used to satisfy regulatory requirements.
e-Manifest user fees cannot be paid through the Pre-Production environment.

We use the pre-production environment when referencing services URLs in this documentation.

## Tools for Testers

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
- [Sample Client](https://github.com/USEPA/e-manifest/tree/master/Services-Information/sample-client) for accessing the
  services
- Python [**emanifest**](https://github.com/USEPA/e-manifest/tree/master/emanifest-py) package for accessing the
  services

Please note: The test environment for the most part mirrors the handler information in our production environment.
When testing, please also make sure your site information is up-to-date. If it is not, please use myRCRAid or your
state’s paper notification process to update your site in the production environment.

## Accessing the Test Environment

See the [Registration](../Intro/registration.md) page for information on how to register for the test environment.
