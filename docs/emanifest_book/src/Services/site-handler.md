# Site and Handler Services

RCRAInfo exposes the following services for retrieving details on sites (industry and regulators) and handlers (
regulators only):

## Site Services

1. Site details
   - Retrieve details on a site, such as ID number, addresses, and whether they have registered users who can
     electronically sign manifests.
2. Site Exists
   - Check if a site exists in RCRAInfo by site ID. Unless an internal system occurs (5xx), this service will always
     return a 200 response code.
3. Site Search
   - Search for sites by criteria.
   ```json
   {
     "$schema": "http://json-schema.org/draft-04/schema#",
     "description": "Schema for site-search service",
     "$ref": "#/definitions/SiteSearch",
     "definitions": {
       "SiteSearch": {
         "type": "object",
         "properties": {
           "epaSiteId": {
             "type": "string",
             "description": "max. length 12"
           },
           "name": {
             "type": "string",
             "description": "max. length 80"
           },
           "streetNumber": {
             "type": "string",
             "description": "max. length 12"
           },
           "address1": {
             "type": "string",
             "description": "max. length 50"
           },
           "city": {
             "type": "string",
             "description": "max. length 25"
           },
           "state": {
             "type": "string",
             "description": "max. length 2 min. length 2"
           },
           "zip": {
             "type": "string",
             "description": "max. length 14"
           },
           "siteType": {
             "type": "string",
             "description": "following site types can be provided: Tsdf, Generator, Transporter, Broker"
           },
           "pageNumber": {
             "type": "number",
             "description": "positive numbers can be provided "
           }
         },
         "additionalProperties": false
       }
     }
   }
   ```
