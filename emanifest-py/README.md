# e-Manifest

[![Downloads](https://pepy.tech/badge/emanifest)](https://pepy.tech/project/emanifest)
![PyPI](https://img.shields.io/pypi/v/emanifest)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

**emanifest** is a client library for accessing the e-Manifest REST APIs of the US Environmental Protection Agency's RCRAInfo national electronic hazardous waste management system.

**Note:** The **emanifest** package was substantially refactored after version 1.1.0 and was released as a new major version at 2.0.0. Code relying on version 1.1.0 should not upgrade to version 2.0.0 of this package without refactoring.

## Contents
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [Methods](#methods)
  - [Help](#help)
- [Contact](#contact)
- [License](LICENSE.txt)

## Requirements
- Python 3.6

## Dependencies
- requests
- requests_toolbelt

## Installation

**emanifest** can be installed directly from the Python package directory using pip:

```bash
pip install emanifest
```

## Usage

### Getting Started

Before using the **emanifest** package, ensure you have a RCRAInfo user account and the [necessary permissions](https://www.epa.gov/e-manifest/frequent-questions-about-e-manifest#user_question6) to generate an API ID and key.

All methods to access the e-Manifest APIs are implemented by the RcrainfoClient class which needs to be authenticated with your API ID and Key. A new instance of the class can be initiated with the ```new_client()``` convenience function like so:

```python
from emanifest import client as em

rcra_client = em.new_client('preprod')
rcra_client.Auth('YOUR_API_ID', 'YOUR_API_KEY')
```

```new_client()``` accepts a string, either **preprod**, **prod**, or a complete base URL. To register for a testing account in preproduction, visit the [preprod site](https://rcrainfopreprod.epa.gov/rcrainfo/action/secured/login). The RcrainfoClient stores the JSON web token and its expiration period (20 minutes). Currently, the **emanifest** python package does not automatically reauthenticate.

### Methods

After authenticating, you are ready to use the full functionality of the **emanifest** package. An introductory example script can be found [here](src/example.py). The RcrainfoClient class exposes a method for each API endpoint in one of the 10 service catagories. For more information about these services, visit the Swagger page of your selected environment. ([PREPROD](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/), [PROD](https://rcrainfo.epa.gov/rcrainfoprod/secured/swagger/)). API endpoints designed for use by other groups, such as regulators or industry users, will return 'Access Denied' errors if you are not authorized to access these resources in RCRAInfo.

1. [All users] Authentication services
2. [All users] e-Manifest Lookup Services
3. [All users] Lookup Services
4. [All users] Site Services
5. [All users] User Services
6. [Industry users] e-Manifest Services
7. [Industry users] e-Manifest UI Link Services
8. [Regulator users] CM&E Evaluation Services
9. [Regulator users] e-Manifest Services
10. [Regulator users] Handler Services
11. [Regulator users] User Services

Content will be returned as a RcraResponse object, which wraps around the [requests.Response](https://pypi.org/project/requests/) object. Methods that download file attachments are decoded and returned in the ```RcrainfoResponse.multipart_json``` and ```RcrainfoResponse.multipart_zip``` when appropriate. The entire ```request.Response``` object is returned in ```RcrainfoResponse.response```. Methods that update, correct, or save manifests by uploading new .json and/or .zip files require a file path.

### Examples:

```python
rcra_client.GetSiteDetails('VATEST000001')
```
Once you've confirmed this is the correct site, you might search for manifests in transit from that site:

```python
rcra_client.SearchMTN(siteId='VATEST000001', status='InTransit')
```
If one of those manifests didn't match your records, you could initiate a correction with the correct JSON information and optionally any attachments (.zip):

```python
rcra_client.Correct('manifest_file_name.json', 'optional_attachments.zip')
```

### Help

If you are uncertain how to use a function, run help(em.FunctionName) in your Python environment. This will return a description of the function, any required inputs, and the formats of those inputs. For a list of all the functions contained in **emanifest** and additional information about this package, run help(emanifest) in your Python environment.

## Contact

Please direct questions to the EPA e-Manifest team at [USEPA/e-manifest](https://github.com/USEPA/e-manifest)

## Disclaimer

The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use. EPA has relinquished control of the information and no longer has responsibility to protect the integrity, confidentiality, or availability of the information. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA. The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or the United States Government.
