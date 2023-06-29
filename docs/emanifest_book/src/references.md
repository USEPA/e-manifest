# Reference Material

## emanifest-py

[![Downloads](https://pepy.tech/badge/emanifest)](https://pepy.tech/project/emanifest)
![PyPI](https://img.shields.io/pypi/v/emanifest)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

**emanifest-py** is a client library (found on the Python Packaging Index under the name [`emanifest`](https://pypi.org/project/emanifest/))
for accessing the e-Manifest REST APIs of the US Environmental Protection Agency's RCRAInfo national electronic
hazardous waste management system.

## Remote Signer Policy

The Remote Signer memorandum is a policy issued by EPA that describes how users can sign manifests through a "remote signer".
The Remote Signer, an individual with sufficient permissions to sign electronic manifests for their site, is authorized to 
exeecute the electronic signature in e-Manifest on behalf of the field personnel who has first-hand knowledge of the hazardous waste shipment.
The field personnel does not need to be a registered user in RCRAInfo.

The Remote Signer policy allows field personnel to sign manifests through their sites hazardous waste management software
using the remote signer's API credentials (ID and Key). The Remote Signer policy also allows the field personnel to
contact a remote signer (e.g., via phone) and authorize the remote signer to sign electronic manifests on their behalf.
The remote signer can then execute the electronic signature manifests through
the RCRAInfo user interface or using their own software that has been configured to use the remote signer's API credentials.

The full policy can be read at [RCRA online](https://rcrapublic.epa.gov/files/14956.pdf)

## Haztrak

Haztrak is a free, open-source, "overkill proof of concept" web application that servers as a reference
for anyone looking for a working example of how waste management software can interface with RCRAInfo
to track hazardous waste shipments electronically cradle to grave. Haztrak is an  
It's built to use the e-Manifest RESTful APIs, designed to be cloud native,
and is available on GitHub under [USEPA/haztrak](https://github.com/USEPA/haztrak)

## Sample Java Client

section and link to java client on GitHub