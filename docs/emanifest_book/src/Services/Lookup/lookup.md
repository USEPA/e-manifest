# Lookup Services

The Lookup Services are a set of services that can be used by industry and regulators to retrieve information directly
related to RCRA.

## State waste codes by state

Returns the list of State Waste Codes and State Waste Code Descriptions by State Code.

#### Parameters

1. state waste code: 2 character state code (e.g., AL, AK, AZ, etc.)

```http
GET /api/v1/lookup/state-waste-codes/{stateCode} HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request
   - 2.1. The system will check if provided State Code is valid. If the provided State Code is invalid the system will
     stop the processing and generate the following error:
     `E_InvalidStateCode: Provided State Code is invalid`
   - 2.2 If no state waste codes are defined for the provided State Code the system will stop the processing and
     generate the following error:
     `E_StateCodesUndefined: State Waste Codes are Not Defined for this State`
3. The system will return the response. If successful, the response body will contain JSON encoded list of state waste
   code for the requested state.

#### Completed Response Example

```json
[
  {
    "code": " PCB5",
    "description": "state defined - polychlorinated biphenyls article container "
  },
  {
    "code": "020L",
    "description": "Part 121,Liquid Industrial Waste of Michigan's Natural Resources and Environmental"
  },
  {
    "code": "040U",
    "description": " Clonitralid (Chemical Abstract Services Number 1420-04-8)"
  },
  {
    "code": "051U ",
    "description": "Diazinon (Chemical Abstract Services Number 333-41-5)"
  }
]
```

#### Error response example

```json
{
  "code": "E_InvalidStateCode ",
  "message": "Provided State Code was not Found",
  "errorId": "9v7a9808-s35a5-4874-928f-12fc3def4b56",
  "date": "2017-06-23T23:15:45.095+0000"
}
```

## Federal waste codes

Returns the list of Federal Waste Codes and Federal Waste Code Descriptions

#### Parameters

none

```http
GET /api/v1/lookup/federal-waste-codes HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of federal waste codes.

#### Completed Response Example

```json
[
  {
    "code": "D001",
    "description": "IGNITABLE WASTE"
  },
  {
    "code": "D002",
    "description": "CORROSIVE WASTE"
  },
  {
    "code": "D003",
    "description": "REACTIVE WASTE"
  },
  {
    "code": "D004",
    "description": "ARCENIC"
  }
]
```

## Density units of measure

- List of EPA Density Units of Measure codes and descriptions

#### Parameters

none

```http
GET /api/v1/lookup/density-uom HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of density units of measurement.

#### Completed Response Example

```json
[
  {
    "code": "1",
    "description": "lbs/gal"
  },
  {
    "code": "2",
    "description": "sg"
  }
]
```

## Form codes

Returns the list of Form Codes and Form Code Descriptions

#### Parameters

none

```http
GET /api/v1/lookup/form-codes HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of form codes.

#### Completed Response Example

```json
[
  {
    "code": "W101",
    "description": "VERY DILUTE AQUEOUS WASTE CONTAINING MORE THAN 99% WATER"
  },
  {
    "code": "W200",
    "description": "STILL BOTTOMS IN LIQUID FORM "
  },
  {
    "code": "W001",
    "description": "LAB PACKS FROM ANY SOURCE NOT CONTAINING ACUTE HAZARDOUS WASTE"
  },
  {
    "code": "W002",
    "description": "CONCENTRATED HALOGENATED (E.G.CHLORINATED) SOLVENT"
  }
]
```

## Management method codes

Returns the list of Management Method Codes and Management Method Code Descriptions

#### Parameters

none

```http
GET /api/v1/lookup/managment-method-codes HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of management method codes.

#### Completed Response Example

```json
[
  {
    "code": "H061",
    "description": "FUEL BLENDING"
  },
  {
    "code": "H040",
    "description": "INCINERATION"
  },
  {
    "code": "H020",
    "description": "SOLVENTS RECOVERY"
  },
  {
    "code": "H132",
    "description": "LANDFILL OR SURFACE IMPOUNDMENT"
  }
]
```

## Waste minimization codes

Returns the list of Waste Minimization Codes and Waste Minimization Code Descriptions

#### Parameters

none

```http
GET /api/v1/lookup/waste-minimization-codes HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of waste minimization codes.

#### Completed Response Example

```json
[
  {
    "code": "X",
    "description": "No waste minimization efforts were implemented"
  },
  {
    "code": "N",
    "description": "Efforts economically or technically impracticable"
  },
  {
    "code": "S",
    "description": "Began to ship waste off-site for recycling"
  },
  {
    "code": "R",
    "description": "Recycling on-site was implemented"
  },
  {
    "code": "Y",
    "description": "Waste minimization efforts were successful"
  },
  {
    "code": "A",
    "description": "Cont. initiative to reduce qty and/or toxicity"
  },
  {
    "code": "B",
    "description": "Cont. initiative to recycle waste on- or off-site"
  },
  {
    "code": "C",
    "description": "Impl. new initiative to reduce qty and/or toxicity"
  }
]
```

## Port of entry codes

Returns the list of import Ports of Entry by City, State name, and State code

#### Parameters

none

```http
GET /api/v1/lookup/ports-of-entry HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

#### Sequence of Steps

1. [Authentication and Authorization](../authentication.md#sequence-of-steps).
2. The system will process the request return the response. If successful, the response body will contain JSON encoded
   list of ports of entry where waste can be imported.

#### Completed Response Example

```json
[
  {
    "cityPort": "ANCHORAGE",
    "state": {
      "code": "AK",
      "name": "ALASKA"
    }
  },
  {
    "cityPort": "PELICAN",
    "state": {
      "code": "AK",
      "name": "ALASKA"
    }
  }
]
```
