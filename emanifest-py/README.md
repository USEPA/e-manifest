# e-Manifest

[![Downloads](https://pepy.tech/badge/emanifest)](https://pepy.tech/project/emanifest)
![PyPI](https://img.shields.io/pypi/v/emanifest)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

**emanifest** is a client library for accessing the e-Manifest REST APIs of the US Environmental Protection Agency's
RCRAInfo national electronic hazardous waste management system.

## Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Authentication](#authentication)
  - [Methods](#methods)
  - [Regulator Usage](#regulators)
  - [Advanced Usage](#advanced-usage-and-help)
- [Contact](#contact)
- [License](LICENSE.txt)

## Requirements

- Python 3.7

## Installation

**emanifest** can be installed directly from the Python package Index (PyPI) using pip:

```shell
$ pip install emanifest
```

## Getting Started

Before using the **emanifest** package, ensure you have a RCRAInfo user account and
the [necessary permissions](https://www.epa.gov/e-manifest/frequent-questions-about-e-manifest#user_question6) to
generate an API ID and key.

All methods to access the e-Manifest APIs are implemented by the `RcrainfoClient` class which needs your API ID and key
to authenticate. A new instance of the class can be initiated like so:

```python
from emanifest import new_client

rcrainfo = new_client('preprod', api_id='YOUR_API_ID', api_key='YOUR_API_KEY')
```

That's it! You're ready to start using the RCRAInfo Restful web services.

The RcrainfoClient class requires one positional argument, a string, either `'preprod'`, or `'prod'`.

### Authentication

The `RcrainfoClient` can be explicit configured to automatically authenticate as needed with the `auto_renew` keyword
argument. By default, this behavior is disabled. If `auto_renew` is disabled, you must explicitly call
the `authenticate` method.

```python
from emanifest import new_client

rcrainfo = new_client('preprod', api_id='my_api_id', api_key='my_api_key', auto_renew=True)
rcrainfo.get_site('VATEST000001')  # This will automatically authenticate if needed.
print(rcrainfo.is_authenticated)  # True
```

The RcrainfoClient stores the security token, its expiration (20 minutes), and will request a new token once expired.

### Methods

After providing your API credentials, you are ready to use the full functionality of the emanifest package. The
RcrainfoClient class exposes a method for each API endpoint following an `<action>_<resource>` naming convention.

#### Examples:

RCRAInfo endpoints that require a URL parameter should be passed as a string to the RcrainfoClient method.

```python
from emanifest import new_client

rcrainfo = new_client('preprod', api_id='YOUR_API_ID', api_key='YOUR_API_KEY')

# Use the rcrainfo auth service to retrieve a security token.
if not rcrainfo.is_authenticated:
    rcrainfo.authenticate()

# Any endpoint with URL parameters will take that parameter as a positional, string argument.
site_resp = rcrainfo.get_site('VATEST000001')
```

Many of the POST request use keyword arguments to compose the http request's body. For example:

```python
from emanifest import new_client

rcrainfo = new_client('preprod', api_id='YOUR_API_ID', api_key='YOUR_API_KEY', auto_renew=True)

resp = rcrainfo.search_mtn(siteId='VATEST000001', status='InTransit')
```

would send a http requests with the following body to the manifest tracking number (mtn) search endpoint.

```json
{
  "siteId": "VATEST000001",
  "status": "InTransit"
}
```

Keyword arguments use the same naming convention seen in the RCRAInfo Swagger pages and services documentation.

`multipart/mixed` payloads (
e.g., [JSON of a manifest](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema/manifest-save-return-examples)
and [.zip file of attachments](https://github.com/USEPA/e-manifest/tree/master/Services-Information)) can be uploaded to
RCRAInfo
by passing a dictionary and the bytes of the optional attachment like so:

```python
from emanifest import new_client
import json

rcrainfo = new_client('preprod', api_id='YOUR_API_ID', api_key='YOUR_API_KEY', auto_renew=True)

# The dictionary and .zip file could come from a database, filesystem, an external service,
# or json.load({'manifestTrackingNumber': '0123456789ELC', ... })
with open('./attachments.zip', 'rb') as f:
    attachment = f.read()
with open('./manifest.json', 'r') as f:
    manifest_json = json.loads(f.read())

resp = rcrainfo.update_manifest(manifest_json, attachment)
```

Responses are returned as a RcraResponse object, which wraps around
the [requests library](https://pypi.org/project/requests/)
Response object. Methods that download file attachments can be accessed via the
`RcrainfoResponse.json()` method and `RcrainfoResponse.zip` property when appropriate. The
entire `request.Response` object is returned in `RcrainfoResponse.response`.

```python
from emanifest import new_client

rcrainfo = new_client('preprod', api_id='YOUR_API_ID', api_key='YOUR_API_KEY', auto_renew=True)

resp = rcrainfo.get_manifest_attachments('123456789ELC')

# RcraInfoResponse re-exports a couple attributes of the requests.Response object.
print(resp.ok)
# Or you can access the full Response like such...
print(resp.response.json())
# For endpoints that return multipart/mixed bodies, you can access JSON with the resp.json()
downloaded_json = resp.json()
# The .zip file can be accessed in the resp.zip property.
downloaded_attachment = resp.zip
```

### Regulators

Starting with version 3.0 and above of this package, regulatory users can use the same methods as industry but with
the `reg` keyword argument set to `True`. For example:

```python
from emanifest import new_client

rcrainfo = new_client('preprod', api_id='YOUR_API_ID', api_key='YOUR_API_KEY')

resp = rcrainfo.get_manifest('123456789ELC', reg=True)
```

The `reg` keyword argument is set to `False` by default.
The following methods have regulator options:

1. get_manifest_attachments
2. search_mtn
3. get_correction
4. get_correction_version
5. get_site_mtn
6. get_manifest
7. get_sites

The following methods are for regulatory users only:

1. get_handler
2. get_cme_lookups
3. get_cme_indicators
4. get_cme_types

API endpoints designed for use by other groups, such as regulators or industry users, will return 'Access Denied' errors
if you are not authorized to access these resources in RCRAInfo.

### Advanced Usage and Help

As of version 3.0, the RcrainfoClient is a subclass of
the [requests library](https://requests.readthedocs.io/en/latest/)
[Session Class](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) which allows you to take
advantage of its functionality.

RcrainfoClient can be also customized by subclassing and overriding. For example:

```python
from emanifest import RcrainfoClient


class MyClass(RcrainfoClient):
    def retrieve_id(self, api_id=None) -> str:
        # Custom behavior to retrieve your RCRAInfo API ID
        my_api_id = 'api_id_from_someplace_secure'
        return super().retrieve_id(my_api_id)
```

For RcrainfoClient method specific documentation, you can use the `help()` function from the Python console to get a
description of each method and its inputs.

```
>>> from emanifest import RcrainfoClient
>>> help(RcrainfoClient.get_bill)
```

For more information about the RCRAInfo services, see the documentation
in the [root directory of the e-Manifest GitHub repo](https://github.com/USEPA/e-manifest), and the Swagger page of your
selected
environment ([Preproduction](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/), [Production](https://rcrainfo.epa.gov/rcrainfoprod/secured/swagger/)).
Do not use the RCRAInfo Production environment for testing. To register for a testing
account in preproduction, visit the [preprod site](https://rcrainfopreprod.epa.gov/rcrainfo/action/secured/login).

## Contact

Please direct questions to the EPA e-Manifest team at [USEPA/e-manifest](https://github.com/USEPA/e-manifest/issues)

## Disclaimer

The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user
assumes responsibility for its use. EPA has relinquished control of the information and no longer has responsibility to
protect the integrity, confidentiality, or availability of the information. Any reference to specific commercial
products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply
their endorsement, recommendation or favoring by EPA. The EPA seal and logo shall not be used in any manner to imply
endorsement of any commercial product or activity by EPA or the United States Government.
