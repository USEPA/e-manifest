# Lookup Services

The Lookup Services are a set of services that can be used by industry and regulators to retrieve information directly
related to RCRA.

## State waste codes by state

Returns the list of State Waste Codes and State Waste Code Descriptions by State Code.

#### Parameters

1. state waste code

#### Request

```http
GET /api/v1/lookup/state-waste-codes/VA HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Accept: application/json
```

### Sequence of Steps

1. Authentication and Authorization.
2. The system will process the request
   - 2.1. The system will check if provided State Code is valid. If the provided State Code is invalid the system will
     stop the processing and generate the following error:
     `E_InvalidStateCode: Provided State Code is invalid`
   - 2.2 If no state waste codes are defined for the provided State Code the system will stop the processing and
     generate the following error:
     `E_StateCodesUndefined: State Waste Codes are Not Defined for this State`
3. The system will return the response. If successful, the response body will contain JSON encoded list of state waste
   code for the requested state.

### Completed Response Example

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

### Error response example

```json
{
  "code": "E_InvalidStateCode ",
  "message": "Provided State Code was not Found",
  "errorId": "9v7a9808-s35a5-4874-928f-12fc3def4b56",
  "date": "2017-06-23T23:15:45.095+0000"
}
```

## Federal waste codes

- List of federal waste codes

## Density units of measure

- List of acceptable EPA Density Units of Measure

## Form codes

- List of EPA Form Codes

## Management method codes

- List of codes used to signify how the waste is managed

## Waste minimization codes

- List of codes used to signify how the waste is minimized

## Port of entry codes

- List of codes describing ports where waste can be imported into the United States.
