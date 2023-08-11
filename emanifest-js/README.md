[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# e-Manifest NPM package

## Intro

The [emanifest npm package](https://www.npmjs.com/package/emanifest) is an API client library.
It simplifies the task of using the RCRAInfo/e-Manifest web services by abstracting the
authentication process, providing developer friendly API, and exporting TypeScript types.
It's built on top of the [Axios](https://axios-http.com/) library, and can be used in both Node and browser
runtime environments (EPA has discussed making some public API available that do not need authentication in the near
future).

For additional information about e-Manifest, check out the below links

- [USEPA/eManifest Github](https://github.com/USEPA/e-manifest)
- [RCRAInfo](https://rcrainfo.epa.gov)
- [RCRAifno PreProduction](https://rcrainfopreprod.epa.gov)
- [About e-Manifest](https://www.epa.gov/e-manifest)
- [e-Manifest PreProd OpenAPI page](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger)

For a python alternative see the [emanifest package on PyPI](https://pypi.org/project/emanifest/)

## Installation

```bash
  $ npm install emanifest
  or
  $ yarn add emanifest
```

## Basic Usage

The primary export of the `emanifest` package is the `newClient` function.
A constructor that accepts a configuration object and returns a new `RcraClient`
instance.

```typescript
import { AxiosResponse } from 'axios';
import { newClient, RCRAINFO_PREPROD, AuthResponse } from 'emanifest';

// The newClient accepts an instance of the RcraClientConfig which follows this interface
// interface RcraClientConfig {
// apiBaseURL?: RcrainfoEnv; // default: RCRAINFO_PREPROD
// apiID?: string;
// apiKey?: string;
// authAuth?: Boolean; // default: false
// validateInput?: Boolean; // default: false
// }

const rcrainfo = newClient({ apiBaseURL: RCRAINFO_PREPROD, apiID: 'my_api_id', apiKey: 'my_api_key' });
const authResponse: AxiosResponse<AuthResponse> = await rcrainfo.authenticate();
console.log(authResponse.data);
```

### Other Exports

The emanifest package also exports the `RCRAINFO_PREPROD` and `RCRAINFO_PROD` constants which can be used to set
the `apiBaseURL` property of the `RcraClientConfig` object.

### Types

The emanifest package exports a types/interfaces that can be used in statically typed projects.
The types follow the OpenAPI schema definitions that can be found in
the [USEPA/e-manifest schema directory](https://github.com/USEPA/e-manifest/tree/master/Services-Information/Schema)
however, some names have been modified for clarity (for example `RcraCode` instead of simply `Code`).

## Auto-Authentication

The `emanifest` package can be explicitly configured to automatically authenticate when needed.

```typescript
import { AxiosResponse } from 'axios';
import { newClient, RCRAINFO_PREPROD, AuthResponse, RcraClientClass, RcraCode } from 'emanifest';

const rcrainfo = newClient({
  apiBaseURL: RCRAINFO_PREPROD,
  apiID: 'my_api_id',
  apiKey: 'my_api_key',
  autoAuth: true, // Set the RcraClient to automatically authenticate as needed
});

// the authenticate method is NOT explicitly called
const resp: AxtiosResponse<RcraCode> = await rcrainfo.getStateWasteCodes('VA');

console.log(resp.data); // [ { code: 'BCRUSH', description: 'Bulb or Lamp Crusher' } ]

console.log(rcrainfo.isAuthenticated()); // true
```

## Input Validation

The `emanifest` package can be explicitly configured to provide some simple input validation. This behavior is disabled
by default. It must be explicitly enabled by setting the `validateInput` property of the `RcraClientConfig` on
initiation.

1. `siteID` must be a string of length 12
2. `stateCode` must be a string of length 2
3. `siteType` must be one of the following: ['Generator', 'Tsdf', 'Transporter', 'Rejection_AlternateTsdf']
4. `dateType` (a search parameter) must be one of the
   following: ['CertifiedDate', 'ReceivedDate', 'ShippedDate', 'UpdatedDate']

Upon validation failure, the `RcraClient` will throw an error which can be caught and handled the same as an error
received from the axios library.

```typescript

```

## Disclaimer

The United States Environmental Protection Agency (EPA) GitHub project code
is provided on an "as is" basis and the user assumes responsibility for its
use. EPA has relinquished control of the information and no longer has
responsibility to protect the integrity, confidentiality, or availability
of the information. Any reference to specific commercial products,
processes, or services by service mark, trademark, manufacturer, or
otherwise, does not constitute or imply their endorsement, recommendation
or favoring by EPA. The EPA seal and logo shall not be used in any manner
to imply endorsement of any commercial product or activity by EPA or
the United States Government.
