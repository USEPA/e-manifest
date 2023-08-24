# e-Manifest Lookup Services

The e-Manifest Lookup Services are a set of services that can be used by industry and regulators to retrieve information
relevant to manifests, such as the list of possible waste codes (federal or state), DOT hazard classes, acceptable units
of measurement, and more.

## Hazardous classes

Returns the list of all Hazard Classes

#### Parameters

none

```http
GET /api/v1/emanifest/lookup/hazard-classes HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of DOT hazard classes.

#### Completed Response Example

```json
[
  "1.2H",
  "1.2J",
  "1.2K",
  "1.2L",
  "1.3C",
  "1.3G",
  "1.3H",
  "1.3J",
  "1.3K",
  "1.3L",
  "1.4B",
  "1.4C"
]
```

## Hazard class by shipping name and ID number

- Retrieve DOT Hazard Classes by DOT Proper Shipping name and ID Number

#### Parameters

1. Proper Shipping Name
2. ID Number

```http
GET /api/v1/emanifest/lookup/hazard-class-by-shipping-name-id-number/{shippingName}/{idNumber} HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of DOT hazard classes.

#### Completed Response Example

```json
["2.2", "2.3"]
```

## Printed tracking number suffixes

Returns the list of all Printed Manifest Tracking Number suffixes (e.g., ELC, JJK, FLE, etc.) and the Owner Companies

#### Parameters

None

```http
GET /api/v1/emanifest/lookup/printed-tracking-number-suffixes HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of manifest tracking number suffixes.

#### Completed Response Example

```json
[
  {
    "code": "ELC",
    "description": "Electronic Manifest"
  },
  {
    "code": "CTN",
    "description": "Nutmeg Environmental"
  },
  {
    "code": "DAT",
    "description": "Databar Inc."
  },
  {
    "code": "FLE",
    "description": "The Flesh Company"
  },
  {
    "code": "GBF",
    "description": "Genoa Business Forms"
  },
  {
    "code": "GRR",
    "description": "Giant Resource Recovery"
  },
  {
    "code": "JJK",
    "description": "J.J. Keller & Associates, Inc."
  },
  {
    "code": "MWI",
    "description": "RR Donnelley"
  },
  {
    "code": "PSC",
    "description": " PSC, LLC "
  }
]
```

## Container types

Returns the list of all Container Types and Container Type Descriptions.

#### Parameters

None

```http
GET /api/v1/emanifest/lookup/container-types HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of container types.

#### Completed Response Example

```json
[
  {
    "code": "BA",
    "description": "Burlap, cloth, paper, or plastic bags"
  },
  {
    "code": "DT",
    "description": "Dump truck"
  },
  {
    "code": "CF",
    "description": "Fiber or plastic boxes, cartons, cases"
  },
  {
    "code": "DW",
    "description": "Wooden drums, barrels, kegs"
  }
]
```

## Quantity units of measure

Returns the list of Quantity UOM Codes and Descriptions

#### Parameters

None

```http
GET /api/v1/emanifest/lookup/quantity-uom HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of quantity units of measurement .

#### Completed Response Example

```json
[
  {
    "code": "P",
    "description": "Pounds"
  },
  {
    "code": "K",
    "description": "Kilogram"
  },
  {
    "code": "M",
    "description": "Metric Tons (1000 Kilograms) "
  },
  {
    "code": "G",
    "description": "Gallons"
  },
  {
    "code": "L",
    "description": "Liters"
  },
  {
    "code": "Y",
    "description": "Cubic Yards "
  }
]
```

## Load Types

List of Polychlorinated biphenyl (PCB) load type

#### Parameters

None

```http
GET /api/v1/emanifest/lookup/load-types HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of PCB load types.

#### Completed Response Example

```json
[
  {
    "code": "ArticleInContainer",
    "description": "Article in Container"
  },
  {
    "code": "ArticleNotInContainer",
    "description": "Article Not in Container"
  },
  {
    "code": "BulkWaste",
    "description": "Bulk Waste"
  },
  {
    "code": "Container",
    "description": "Container"
  }
]
```

## Proper shipping names

Returns the list of all DOT Proper Shipping Names. Proper Shipping Name Comments and
Technical Name Indicators

#### Parameters

None

```http
GET /api/v1/emanifest/lookup/proper-shipping-names HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of all DOT proper shipping names.

#### Completed Response Example

```json
[
  {
    "psn": "1,1,1-Trifluoroethane or Refrigerant gas, R 143a",
    "technicalNameIndicator": false
  },
  {
    "psn": "1,1-Difluoroethane or Refrigerant gas R 152a",
    "technicalNameIndicator": false
  },
  {
    "psn": "1,1-Difluoroethylene or Refrigerant gas R 1132a",
    "technicalNameIndicator": false
  },
  {
    "psn": "Carbamate pesticides, liquid, toxic, flammable",
    "psnComments": ["flash point not less than 23 degrees C"],
    "technicalNameIndicator": true
  }
]
```

## Proper shipping names by ID number

Returns list of DOT Proper Shipping names by DOT ID Number

#### Parameters

1. ID Number

```http
GET /api/v1/emanifest/lookup/proper-shipping-names-by-id-number HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request

   - 2.1 The system will check if provided ID Number has valid format.
   - 2.2 Provided ID Number shall be compliant with the following format:
     - length: 6 characters
     - first 2 characters either "UN" of "NA"
     - last 4 characters are numeric
   - 2.3 if ID number is invalid, will return error
     `E_InvalidIdNumber: Invalid Id Number`
   - 2.4 If no ID number is found in the system, will return error
     `E_IdNumberNotFound: Id Number not found`

3. return the response. If successful, the response body will contain JSON encoded
   list of all DOT proper shipping names.

#### Completed Response Example

```json
[
  "Chemical kit",
  "Compounds, cleaning liquid",
  "Compounds, tree killing, liquid or Compounds, weed killing, liquid"
]
```

#### Validation Error Response Example

```json
{
  "code": " E_InvalidIdNumber ",
  "message": "Invalid Id Number",
  "errorId": "9v7a9808-s35a5-4874-928f-12fc3def4b56",
  "date": "2017-06-23T23:15:45.095+0000"
}
```

## ID numbers

Returns a list of DOT ID Numbers

#### Parameters

None

```http
GET /api/v1/emanifest/lookup/id-numbers HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of all DOT ID numbers.

#### Completed Response Example

```json
[
  "UN2035",
  "UN1030",
  "UN1959",
  "UN2517",
  "UN2044",
  "UN1001",
  "UN1950",
  "UN1950",
  "UN1011"
]
```

## ID numbers by shipping name

Returns the list of ID Numbers by the Proper Shipping Name.

#### Parameters

1. Proper Shipping Name

```http
GET /api/v1/emanifest/lookup/proper-shipping-names-by-id-number HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request

   - 2.1 if provided shipping name exceeds 300 characters, the system will return error
     `E_InvalidProperShippingName: Invalid Proper Shipping Name`
   - 2.2 f no ID Numbers were found the system stops processing and generates the following error:
     `E_ProperShippingNameNotFound: Proper Shipping Name Not Found`

3. return the response. If successful, the response body will contain JSON encoded
   list of all DOT ID numbers.

#### Completed Response Example

```json
["UN1339", "UN1340", "UN1341"]
```

#### Validation Error Response Example

```json
{
  "code": " E_InvalidProperShippingName ",
  "message": "Invalid Proper Shipping Name",
  "errorId": "9v7a9808-s35a5-4874-928f-12fc3def4b56",
  "date": "2017-06-23T23:15:45.095+0000"
}
```

## Packing groups

Returns list of all DOT Packing Groups

#### Parameters

None

```http
GET /api/v1/emanifest/lookup/packing-groups HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of all DOT Packing Groups.

#### Completed Response Example

```json
["I", "II", "III"]
```

## Packing groups by shipping name and ID

Returns list of DOT Packing Groups by DOT Proper Shipping name and ID Number

#### Parameters

1. Proper Shipping Name
2. ID Number

```http
GET /api/v1/emanifest/lookup/packing-groups-by-shipping-name-id-number/{shippingNmae}/{idNumber} HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request

   - 2.1 f the size of provided Proper Shipping Name exceeds 300 characters the system stops processing and generate
     the following error:
     `E_InvalidProperShippingName: Invalid Proper Shipping Name`
   - 2.2 The system will check if provided ID Number has valid format via the following rules:
     - length: 6 characters
     - first 2 characters either "UN" of "NA"
     - last 4 characters are numeric
       `E_InvalidIdNumber: Invalid Id Number`
   - 2.3 The system will obtain the Packing Group for the provided shipping name and ID number:
   - 2.4 If Proper Shipping Name was not found the system stops processing and generates following error:
     `E_ProperShippingNameNotFound: Proper Shipping Name Not Found`
   - 2.5 If ID Number was not found the system stops processing and generates following error:
     `E_IdNumberNotFound: ID Number Not Found`
   - 2.6 If combination of Proper Shipping Name and ID Number was not found the system stops processing and generates
     following error:
     `E_CombinationProperShippingNameIdNumberNotFound: combination of Proper Shipping Name and Id Number was not found`

3. return the response. If successful, the response body will contain JSON encoded
   list of the appropriate DOT packing group.

#### Completed Response Example

```json
["I", "II"]
```

#### Validation Error Response Example

```json
{
  "code": "E_CombinationProperShippingNameIdNumberNotFound",
  "message": "Combination of Proper Shipping Name and Id Number was not found",
  "errorId": "9v7a9808-s35a5-4874-928f-12fc3def4b56",
  "date": "2017-06-23T23:15:45.095+0000"
}
```
