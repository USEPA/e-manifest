1. The System will validate the Security Token

   1.1 If Web Security Token is invalid, the system stops the submission and generates the following error:

   - `E_SecurityApiTokenInvalid: Invalid Security Token`

   1.2. If Web Security Token expired, the system stops the submission and generates the following
   error:

   - `E_SecurityApiTokenExpired: Security Token is Expired`

   1.3. If Account was inactivated after the token was issued, the system stops the submission and
   generates the following error:

   - `E_SecurityApiInvalidStatus: This API ID is no longer active`
