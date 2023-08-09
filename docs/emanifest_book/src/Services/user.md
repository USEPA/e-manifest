# User Services

The user services are a set of endpoints retrieve information about users, which can be used by both industry and
regulators, and an authentication service that can be used by only state regulators.

## User Search

A service that allows user to search for other users by user ID, siteId(s).
example HTTP request

```http
POST /api/v1/users/user-search HTTP/1.1
Host: rcrainfo.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
  "userId": "user1",
  "siteIds": ["site1", "site2"]
}
```

Both fields, `userId` and `siteIds` are optional. If you know the user ID, you can use this service to return the user's
information, such as what site's they have access to and the permissions in RCRAInfo they have for each site.

<details>
    <summary>Example HTTP Response</summary>

```json
{
  "totalNumberOfUsers": 1,
  "totalNumberOfPages": 1,
  "currentPageNumber": 1,
  "warnings": [],
  "searchedParameters": [
    {
      "field": "userId",
      "value": "myUserId123"
    }
  ],
  "users": [
    {
      "userId": "myUserId123",
      "firstName": "John",
      "lastName": "Doe",
      "email": "foobar@gmail.com",
      "phone": {
        "number": "555-555-5555"
      },
      "esaStatus": "Received",
      "lastLoginDate": "2023-08-09T18:15:30.849+00:00",
      "sites": [
        {
          "siteId": "VAB000535062",
          "siteName": "TEST BROKER 5-28-2020",
          "permissions": [
            {
              "module": "SiteManagement",
              "level": "Active"
            },
            {
              "module": "AnnualReport",
              "level": "Certifier"
            },
            {
              "module": "BiennialReport",
              "level": "Certifier"
            },
            {
              "module": "eManifest",
              "level": "Certifier"
            },
            {
              "module": "myRCRAid",
              "level": "Certifier"
            },
            {
              "module": "WIETS",
              "level": "Certifier"
            }
          ]
        },
        {
          "siteId": "VATESTGEN001",
          "siteName": "VA TEST GEN 2021",
          "permissions": [
            ...
          ]
        }
      ]
    }
  ]
}
```

</details>

Conversely, the user search service can be used to find all users that have access to a site by the site's EPA ID
number (e.g., `"VATESTGEN001"`).

<details>
    <summary>Example HTTP Response</summary>

```json
{
  "totalNumberOfUsers": 8,
  "totalNumberOfPages": 1,
  "currentPageNumber": 1,
  "warnings": [],
  "searchedParameters": [
    {
      "field": "siteIds",
      "value": "[VATESTGEN001]"
    }
  ],
  "users": [
    {
      "userId": "myUserId123",
      "firstName": "John",
      "lastName": "Doe",
      "email": "foobar@gmail.com",
      "phone": {
        "number": "555-555-5555"
      },
      "esaStatus": "Received",
      "lastLoginDate": "2023-08-09T18:15:30.849+00:00",
      "sites": [
        ...
      ]
    }
    ...
  ]
}
```

</details>

## State Regulator Authentication

This service is available for state regulators only.

Please contact the RCRAInfo team with questions.
