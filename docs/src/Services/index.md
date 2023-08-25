# Services Information

The RCRAInfo provides a set of services that can be used by industry and regulators.
The services are available via a RESTful API, and are categorized by the type of user that can access them and the
resource.

1. [All users] [Authentication services](authentication.md)
2. [All users] e-Manifest Lookup Services
3. [All users] Lookup Services
4. [All users] Site Services
5. [All users] User Services
6. [Industry users] [e-Manifest Services](Manifest/save.md)
7. [Industry users] e-Manifest UI Link Services
8. [Regulator users] CM&E Evaluation Services
9. [Regulator users] [e-Manifest Services](Manifest/states.md)
10. [Regulator users] Handler Services
11. [Regulator users] User Services

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
