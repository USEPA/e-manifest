# eManifest

eManifest is a Python utility wrapper for accessing the eManifest API of the US Environmental Protection Agency's RCRAInfo national electronic hazardous waste management system.

## Contents
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [Functions](#functions)
  - [Help](#help)
- [Contact](#contact)
- [License](#license)

## Requirements

- Python 3.6

## Dependencies

- requests
- requests_toolbelt
- getpass
- pandas
- json
- zipfile
- io

## Installation

eManifest can be installed directly from the Python package directory using pip:

```bash
pip install emanifest
```

## Usage

### Getting Started

Before using the eManifest package, ensure you have a RCRAInfo user account and the necessary permissions to generate an API ID and key. Make note of your ID and key somewhere safe.

To add eManifest to your current Python environment and authenticate your account, peform the following commands:

```python
from emanifest import emanifest as em

em.eManAuth('YOUR_API_ID', 'YOUR_API_KEY', 'YOUR_ENVIRONMENT')
```

Your environment variable can be any of the following for which you have permission: "dev", "sandbox", "preprod", "prod"

Once you receive a "Successfully authenticated" message, you are ready to use the full functionality of the eManifest package. Functions designed for use by other groups, such as regulators or industry users, will return 'Access Denied' errors if you are not authorized to view this content in RCRAInfo.

### Functions

There are ten categories of functions in the eManifest package. For more information about these services, visit the Swagger page of your selected environment. ([DEV](https://rcrainfodev.com/rcrainfo/rest), [SANDBOX](https://sandbox.rcrainfodev.net/rcrainfo/rest/), [PREPROD](https://rcrainfopreprod.epa.gov/rcrainfo/rest/), [PROD](https://rcrainfo.epa.gov/rcrainfoprod/rest/))

1. [All users] Authentication services
2. [All users] eManifest Lookup Services
3. [All users] Lookup Services
4. [All users] Site Services
5. [Industry users] eManifest Services
6. [Industry users] eManifest UI Link Services
7. [Regulator users] CM&E Evaluation Services
8. [Regulator users] eManifest Services
9. [Regulator users] Handler Services
10. [Regulator users] User Services

Most content will be returned as a [Pandas Dataframe item](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html). To output this data as a CSV or Excel file, you will need to ensure the Pandas library is active in your current Python environment, select a desired eManifest function (e.g. GetSiteDetails), and perform one of the following commands:

```python
import pandas as pd # Unnecessary if you have imported Pandas elsewhere

em.GetSiteDetails('VATESTSD123').to_csv('your_new_file_name.csv')

em.GetSiteDetails('VATESTSD123').to_excel('your_new_file_name.xlsx')

```

More complicated results will be returned as a JSON object.

Functions that download file attachments will store these in the same folder as your Python document. Functions that update, correct, or save manifests by uploading new .json and/or .zip files must receive the specific location of these files on your computer. By default, these functions will assume the files are located in the same folder as your Python document.

### Help

If you are uncertain how to use a function, run help(em.FunctionName) in your Python environment. This will return a description of the function, any required inputs, and the formats of those inputs. For a list of all the functions contained in eManifest and additional information about this package, run help(emanifest) in your Python environment.

## Contact

Please direct questions to the EPA eManifest team at [USEPA/e-manifest](https://github.com/USEPA/e-manifest)

## License

eManifest is in the US Public Domain and licensed worldwide under CC0 1.0. [See LICENSE](https://github.com/USEPA/e-manifest/emanifest-py/blob/master/LICENSE) for details.