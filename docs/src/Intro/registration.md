# User Registration

EPA allows industry and states to access the RCRAInfo Pre-Production environment to try new features, and test things.
You may see this site referred to as the "test" environment.

- For testing, use RCRAInfo Pre-Production
  - <https://rcrainfopreprod.epa.gov>
- For Production, use RCRAInfo
  - <https://rcrainfo.epa.gov>

You will need to create a separate account for each environment.

## Registration Process

The registration process for both environments is identical, the general process includes creating a user account, then
requesting access to the EPA sites that you are working for.

1. Visit the RCRAInfo [pre-production site](https://rcrainfopreprod.epa.gov)
2. Click on the "Register" link and select _"Industry User"_
3. Register, verify your email, and log in

### Obtain Site Access

If your state is participating in approving e-Manifest test users, you may request access to your handler ID(s).
Otherwise, please register to use one of our test sites:

| Site ID      | Site Name                | State    | Zip   | Type of Site           | Notes                                |
| ------------ | ------------------------ | -------- | ----- | ---------------------- | ------------------------------------ |
| VA988177803  | HEATING AND OIL          | Virginia | 22033 | Generator only         |                                      |
| VATEST000001 | TEST TRANSPORTER 1 OF VA | Virginia | 22202 | Generator, Transporter |                                      |
| VATEST000002 | TEST TRANSPORTER 2 OF VA | Virginia | 22202 | Generator, Transporter |                                      |
| VAD000532119 | TEST TSDF OF VA          | Virginia | 22202 | Generator, TSDF        | Can be used for testing web services |
| VATEST000003 | TEST TSDF OF VA TWO      | Virginia | 22202 | Generator, TSDF        | Can be used for testing web services |
| VATEST000004 | TEST GENERATOR OF VA     | Virginia | 22202 | Generator only         |                                      |

- On the My Sites page, click on the "Add Existing Site" button

- Search for your EPA ID number in the Site ID box or a test site and then select that facility. (For example:
  VA000532119)

- Request a role for each module for this site. The roles are:
  - Site Manager (can use our web services)
  - Certifier
  - Preparer
  - Viewer

The Site Manager role is the equivalent to having the Certifier role in each RCRAInfo module, and also has the ability
to add and remove users from the site, and generate an API ID and key.

After you submit your request, the request will go to your state or an EPA administrator. Please understand this is
not an instant access process and the administrator will need to manually activate your request during normal business
hours.

### Obtaining an API ID and Key

If you want to register for an API ID and key to test the services, you may create one by clicking on the 'Tools' menu
and selecting API. You can use the [Swagger](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/) page to test 
without your API ID and key.

{{#include ../components/footer.md}}
