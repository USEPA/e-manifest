# e-Manifest Services for states

The way that industry and regulators use the e-Manifest is, in large part, the same.
States authenticate in the same method described in the [Authentication](../authentication.md) section
and use the same [security tokens](../authentication.md#security-tokens) to access the services.
However, there are a few categories of services that are specific to states.

All the services described in this section can be tested in the Open API (swagger) page for
which you can find the at the following URL: <https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger>.

## Compliance Monitoring & Enforcement (CM&E) Services

This category of endpoints contains services that are used by states to monitor and enforce compliance.

## Manifest Services

Regulators use the Manifest Services to search and view manifests. They cannot create, update, delete, or sign manifests
through the services, like industry. All endpoints in this start with `/api/v1/state/emanifest` as opposed to
`/api/v1/emanifest` for industry.

## Handler Services

This category contains one endpoint that is used to get the details of a hazardous waste handler.
It takes 2 parameters, supplied in the URL path:

1. The handler ID: the unique EPA ID of the handler
2. details requested: a boolean, cast as a string (e.g., `"true"` or `"false"`), that indicates whether to return
   greater amounts of the handler's details

## User Services
