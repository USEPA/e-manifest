# User Registration

In order to access the test environment, all users will be required to set up a test account on the RCRAInfo test
environment.

- For testing, use RCRAInfo Pre-Production
  - <https://rcrainfopreprod.epa.gov>
- For Production, use RCRAInfo
  - <https://rcrainfo.epa.gov>

For the remainder of this chapter, we assume that you are using the pre-production (test) deployment as testing should
never be done in the RCRAInfo Production deployment.

## Registration Process

The registration process for both environments is identical, the general process includes creating a user account, then
requesting access to EPA sites. The process is described in detail below.

### User Registration

1. Visit the RCRAInfo [pre-production site](https://rcrainfopreprod.epa.gov)
2. Click on the "Register" link
3. Click the "Continue to Industry User Registration" button.
4. Fill out Title and Name and click the "Next" button.
5. Create your username, password, and password retrieval questions
6. Review and agree to the Terms and Conditions, and click the "Next" button
7. Fill out the information for your Organization (not necessarily your site), Job title, phone and email address.
8. Click the "Send Verification Code via Email" button
9. After entering the verification code from your email click the "Register" button
10. You will be taken to the My Sites page to register your handler(s)

### Obtain Site Access

The RCRAInfo test site has a number of EPA sites that you can request access to for testing purposes. The following
table sites are available for testing:

| Site ID      | Site Name                | State    | Zip   | Site Type              | Notes |
| ------------ | ------------------------ | -------- | ----- | ---------------------- | ----- |
| VA988177803  | HEATING AND OIL          | Virginia | 22033 | Generator only         |       |
| VATEST000001 | TEST TRANSPORTER 1 OF VA | Virginia | 22202 | Generator, Transporter |       |
| VATEST000002 | TEST TRANSPORTER 2 OF VA | Virginia | 22202 | Generator, Transporter |       |
| VAD000532119 | TEST TSDF OF VA          | Virginia | 22202 | Generator, TSDF        |       |
| VATEST000003 | TEST TSDF OF VA TWO      | Virginia | 22202 | Generator, TSDF        |       |
| VATEST000004 | TEST GENERATOR OF VA     | Virginia | 22202 | Generator only         |       |

- On the My Sites page, click on the “Add Existing Site” button

- Search for your EPA ID number in the Site ID box or a test site and then select that facility. (For example:
  VA000532119)

- Request a role for the site

  - The 'Site Manager' Role will allow you to use the API services.

- After you submit your request, the request will go to your state or an EPA administrator. Please understand this is
- not an instant access process and the administrator will need to manually activate your request during normal business
  hours.

- Once you have completed this registration you may use either <https://test.epacdx.net/> or
  <https://rcrainfopreprod.epa.gov/rcrainfo/> to log on to the application.

## Obtaining an API ID and Key

Generating an API ID and key is a function confined to users that have the 'Site Manager' role for at least one site.

If you want to register for an API ID and key to test the services, you may create one by clicking on the 'Tools' menu
and selecting API. The API page will allow you to generate your unique API ID and key. The API ID and Key can be used
to access our web services which are documented on the [Services](../Services/index.md) chapter
and, if logged into e-Manifest, on [Swagger](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/)

{{#include ../components/footer.md}}
