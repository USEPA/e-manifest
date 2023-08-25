# Reference Material

## API Client Libraries

The e-Manifest maintains two API client library packages, both called _emanifest_, one for Python and one for
JavaScript/TypeScript.

These packages simplify the process of using the RCRAInfo/e-Manifest web services by abstracting away the details of
authentication, parsing and uploading multipart/mixed payloads, and provide an idiomatic interface for interacting with
the services.

## emanifest (Python)

[![Downloads](https://pepy.tech/badge/emanifest)](https://pepy.tech/project/emanifest)
![PyPI](https://img.shields.io/pypi/v/emanifest)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

The `emanifest` python package can be downloaded from the Python Packaging Index (PyPI).

Documentation and the source files can be found in
the [emanifest-py](https://github.com/USEPA/e-manifest/tree/master/emanifest-py) directory of
the USEPA/e-manifest repository on GitHub.

## emanifest (JavaScript)

[![npm](https://img.shields.io/npm/dt/emanifest.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![npm type definitions](https://img.shields.io/npm/types/emanifest)

The `emanifest` JavaScript/TypeScript package can be downloaded from the Node Package Manager (NPM). THe package also
bundles type declarations for TypeScript users.

Documentation and the source files can be found in
the [emanifest-js](https://github.com/USEPA/e-manifest/tree/master/emanifest-js) directory of the USEPA/e-manifest
repository on GitHub.

## Remote Signer Policy

The Remote Signer memorandum is a policy issued by EPA that describes how users can sign manifests through a "remote
signer". The Remote Signer, an individual with sufficient permissions to sign electronic manifests for their site, is
authorized to execute the electronic signature in e-Manifest on behalf of the field personnel who has first-hand
knowledge of the hazardous waste shipment. The field personnel does not need to be a registered user in RCRAInfo.

The Remote Signer policy allows field personnel to sign manifests through their sites hazardous waste management
software using the remote signer's API credentials (ID and Key). The Remote Signer policy also allows the field
personnel to contact a remote signer (e.g., via phone) and authorize the remote signer to sign electronic manifests on
their behalf. The remote signer can then execute the electronic signature manifests through the RCRAInfo user interface
or using their own software that has been configured to use the remote signer's API credentials.

The full policy can be read on [RCRA online](https://rcrapublic.epa.gov/files/14956.pdf)

## Haztrak

Haztrak is a free, open-source, "overkill proof of concept" web application that servers as a reference
for anyone looking for a working example of how waste management software can interface with RCRAInfo
to track hazardous waste shipments electronically cradle to grave. Haztrak is an  
It's built to use the e-Manifest RESTful APIs, designed to be cloud native,
and is available on GitHub under [USEPA/haztrak](https://github.com/USEPA/haztrak)

## Sample Java Client

section and link to java client on GitHub
