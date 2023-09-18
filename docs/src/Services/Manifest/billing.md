# e-Manifest Billing Service

These services to retrieve e-Manifest user fee billing information.

- [Bill Service](#bill-service)
- [Bill History Service](#bill-history-service)
- [Bill Search Service](#bill-search-service)

## Bill Service

The service returns bill information either by the combination of the billing account and bill id or by the combination
of the billing account and month and the year of the bill.

### Parameters

- [Security Token](../authentication.md#security-tokens)
- The following service parameters will be passed as JSON compliant to the JSON schema defined
  in [bill-request.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/bill-request.json)
  - Billing Account AND Bill ID
    or
  - Billing Account AND Month/Year

If billId and monthYear is provided the service validates provided billId. If the billId is valid the service returns
data based on billId. If billId is not valid the service validates provided monthYear. If the monthYear is valid the
service returns data based on monthYear

### Examples

```http
POST /rcrainfo/rest/api/v1/emanifest/manifest/bill HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService
Content-Type: application/json

{
    "billingAccount": "123456789",
    "billId": "123456789",
}
```

### Example Valid JSON

1. Supplying both `billingAccount` and the `billId`

   ```json
   {
     "billingAccount": "VATESTTSDF001",
     "billId": "123456789"
   }
   ```

2. Supplying both `billingAccount` and the `monthYear`

   ```json
   {
     "billingAccount": "VATESTTSDF001",
     "monthYear": "01/2021"
   }
   ```

3. If `monthYear` is provided along with `billingAccount` and `billId`, the `monthYear` argument is ignored.

   ```json
   {
     "billingAccount": "VATESTTSDF001",
     "billId": "123456789",
     "monthYear": "01/2021"
   }
   ```

### Response Schema

See [bill.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/bill.json) for the response
schema.

### Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will process the request

   - 3.1. If Billing account of the facility (EPA Site ID) is not provided the schema validation exception will be
     returned:
     - `Object has missing required properties (["billingAccount"]): null`
   - 3.2. If no additional parameters provided (either billId or monthYear) the processing will be stopped and system
     will generate the following error:
     - `E_NoAdditionalParametersProvided: No additional parameters are provided`
   - 3.3. If the provided `billingAccount` (EPA Site ID) is invalid the processing will be stopped and system will
     generate the following error:
     - `E_InvalidBillingAccount: Provided Billing Account has invalid format`
   - 3.4. If the provided `billingAccount` is not registered the processing will be stopped and system will generate
     the
     following error:
     - `E_NoBillingAccount: Billing account doesn't exist`
   - 3.5. If the provided `billingAccount` is not active the processing will be stopped and system will generate the
     following error:
     - `E_BillingAccountNotActive: Billing Account is not active`
   - 3.6. If the User does not have permission to the site with provided billing account the system will stop the
     processing and generates the following error:
     - `E_BillingAccountPermissions: The user does not have Industry Permissions to the site with provided billing account`
   - 3.7. If `billingAccount` was found and the `billId` is either erroneous or was not provided and the monthYear is
     either erroneous or was not provided the system will generate JSON containing the following information:
     - billingAccount: provided billing account
     - report: see details in the report table
   - 3.8. If the billStatus is "Active" the processing will be stopped and system will generate the following error:
     - `E_BillStatusActive: Bill Status is Active. Cannot be viewed by the industry`

4. The service will generate JSON containing:

   - `billingAccount`: EPA Site ID
   - `billId`: unique bill id
   - `monthYear`: Contains month number and year of the requested bill if provided.
   - report: Contains service report. Following reports are possible:

     - The service returning bill by `monthYear`. Valid `monthYear` is provided, bill id is not provided
     - The service returning bill by bill id. Valid bill id is provided, valid `monthYear` is provided
     - The service returning bill by `monthYear`. Invalid bill id is provided, valid monthYear is provided
     - The service returning bill by monthYear. provided bill id is not found, valid `monthYear` is provided
     - The service returning bill by bill id. Valid bill id is provided, invalid `monthYear` is provided
     - The service returning bill by bill id. Valid bill id is provided, provided `monthYear` is out of date range
     - `billStatus`: Following values can be returned: "Active", "Unpaid", "InProgress",
       "ReadyForPayment", "Paid", "SentToCollections", "Credit", "ZeroBalance"
     - `totalAmount`: if the billStatus is Credit then a negative value will be returned. If the billStatus
       is ZeroBalance then 0 value will be returned
     - `currentAmount`: The amount for manifests invoiced for the current billing period
     - `previousAmount`: The total for all manifests not paid or sent to collections from billing
       periods before the current period
     - `previousInterestAmount`: The total of interest fees occurred on the previous amounts for all
       manifests not paid or sent to collections from billing periods before the current period
     - `previousPenaltyAmount`: for invoices that are being sent to collections, the penalty amount
       for that invoice
     - `previousLateFeeAmount`: Total of the flat fee, penalty, and interest charges for all manifests
       and invoices not paid or sent to collections from billing periods before the current period
     - `dueDate`: The date the invoice is due
     - `paidBy`: Contains the bill payee user id, for invoices that were marked as paid by the EPA, this element is
       not returned
     - `paymentType`: Contains bill status, Following values can be returned: "Credit", "Ach", for invoices that were
       marked as paid by the EPA, this element is not returned
     - `createdDate`: The date the first manifest for this invoice was signed and placed on the invoice
     - `updatedDate`
     - `billItems` containing the following information:
       - `manifestTrackingNumber`
       - `amount`: Amount charged for each manifest
       - `submissionType`: "FullElectronic", "Hybrid", "DataImage5Copy", "Image"
       - `originType`: "Web", "Services", "Mail"
       - `certifiedDate`: Date the manifest was certified and placed on this invoice
       - `generatorSiteId`: The site ID of the generator on the manifest
     - late fees (when applicable) containing the following information:
       - `lateFeeBillId`: Bill ID which Late Fee is calculated for
       - `interestAmount`: the total interest amount for this lateFeeBillId
       - `penaltyAmount`: the total penalty amount for this lateFeeBillId
       - `lateFeeAmount`: the total interest, penalty, and flat fee amounts for this lateFeeBillId
       - `flatFeeAmount`: the total flat fee amount for this lateFeeBillId
       - `status`: the status of the invoice; please note that invoices sent to collection will be
         marked as inactive
     - revisions (when applicable) containing the following information:
       - `amount`: Amount of adjustment on the invoice
       - `amountType`: `Current`, `LateFee`
       - `adjustmentType`: `Increase`, `Decrease`, `FullPayment`
       - `publicComments`:
       - `createdDate`

5. On success, the system returns JSON generated in section 4
6. If any system errors were encountered during processing, the system will return:

- error: containing error code, error message, error id, and

## Bill History Service

The service returns billing summary information either by the provided billing account or by the combination of the
billing account and date range. Following information will be returned about all bills for the provided billing account:

- `billingAccount`: EPA Site ID
- `startMonthYear`: Contains month number and year for the date range start, if provided in the request. If
  only `startMonthYear` provided the service return bill history from the start until current mm/yyyy. If
  invalid `startMonthYear` is provided bill history from inception to the `endMonthYear` is returned.
- `endMonthYear`: Contains month number and year for the date range end. If only `endMonthYear` provided the service
  return bill history from inception to the `endMonthYear`. If invalid `endMonthYear` is provided bill history
  from `startMonthYear` to the current date is returned.
- `billsInfo`: contains individual bills for the billing account. For each bill it contains following information
  - `billId`: unique bill id
  - `billStatus`: Following values can be returned: `Active`, `Unpaid`, `InProgress`,
    `ReadyForPayment`, `Paid`, `SentToCollections`, `Credit`, `ZeroBalance`. Industry will not
    see bills where billStatus = Active
  - `totalAmount`: if the `billStatus` is Credit then negative value will be returned. If the `billStatus`
    is `ZeroBalance` then 0 value will be returned
  - `paidBy`: Contains the bill payee user id
  - `paymentType`: Contains bill status, Following values can be returned: `Credit`, `Ach`,
    `OutOfBand`
  - `dueDate`
  - `createdDate`
  - `updatedDate`

## Parameters

- [Security Token](../authentication.md#security-tokens)
- The following service parameters will be passed as JSON compliant to the JSON schema defined
  in [bill-history-request.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/bill-history.json)
  - `billingAccount`: Billing account of the facility (EPA Site ID). Required parameter. If date range parameters are
    not provided the service return bill history from inception to the current date
  - `startMonthYear`: Contains month number and year for the date range start. Format 'mm/yyyy'. If only
    `startMonthYear` provided the service return bill history from the start until current mm/yyyy. If invalid
    `startMonthYear` is provided bill history from inception to the `endMonthYear` is returned.
  - `endMonthYear`: Contains month number and year for the date range end. Format 'mm/yyyy'. If only `endMonthYear`
    provided the service return bill history from inception to the `endMonthYear`. If invalid `endMonthYear` is
    provided
    bill history from `startMonthYear` to the current date is returned.

## Examples

```http
POST /rcrainfo/rest/api/v1/emanifest/manifest/get-bill-history HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService

{
    "billingAccount": "VATESTTSDF001",
    "startMonthYear": "01/2021",
    "endMonthYear": "02/2021"
}
```

See [bill-history.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/bill-history.json)
for the response schema.

### Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will process the request

   - 3.1. If the provided billingAccount is invalid, the processing will be stopped, and the system will
     generate the following error:
     - E_InvalidBillingAccount: Provided Billing Account has an invalid format
   - 3.2. If the User does not have permission to the site with the provided billing account, the system
     will stop the processing and generates the following error:
     - E_BillingAccountPermissions: The user does not have Industry Permissions to the site with
       provided billing account
   - 3.3. If the provided billingAccount is not registered, the processing will be stopped, and the system
     will generate the following error:
     - E_NoBillingAccount: Billing account doesn't exist
   - 3.4. If the provided billingAccount is not active, the processing will be stopped, and the system will
     generate the following error:
     - E_BillingAccountNotActive : Billing Account is not active

4. If the provided Billing Account is valid, the service will generate bill history depending on date range
   parameters according to the following:

   - 4.1. If date range parameters are not provided or invalid date range parameters are provided,
     the service generates bill history from inception to the current date. If invalid dates are provided,
     the service will specify the invalid dates in the generated JSON response as follows:
     - invalid date, returning bill history since inception date (07/2018)
     - invalid date, returning bill history to [current MM/current YYYY]
   - 4.2. If a valid startMonthYear is provided and endMonthYear is not provided or valid startMonthYear
     provided and endMonthYear is invalid, the service generates bill history from the start until
     the current mm/yyyy. If an invalid endMonthYear is provided, the service will specify the invalid
     endMonthYear in the generated JSON response (identical to 4.1)
   - 4.3. If an invalid startMonthYear is provided and valid endMonthYear is provided or startMonthYear
     is not provided and valid endMonthYear is provided, the service generates bill history from
     inception to the endMonthYear. If an invalid startMonthYear is provided, the service will specify
     the invalid startMonthYear in the generated JSON response (identical to 4.1).

5. The service will generate JSON containing:

   - billingAccount: EPA Site Id
   - billId: unique bill id
   - If invalid dates are provided, the service will specify the invalid dates
   - billStatus: Following values can be returned: "Active", "Unpaid", "InProgress", "ReadyForPayment",
     "Paid", "SentToCollections", "Credit", "ZeroBalance". Industry will not see bills where billStatus = Active
   - totalAmount: if the billStatus is Credit then a negative value will be returned. If the billStatus is
     ZeroBalance then 0 value will be returned
   - paidBy: Contains the bill payee user id, for invoices that were marked as paid by the EPA, this
     element is not returned
   - paymentType: Contains bill status, Following values can be returned: "Credit", "Ach", for invoices that
     were marked as paid by the EPA, this element is not returned.
   - dueDate
   - createdDate: The date the first manifest for this invoice was signed and placed on the invoice
   - updatedDate

6. On success, the system returns JSON generated in section 4
7. If any system errors were encountered during processing, the system will return:
   - error: containing error code, error message, error id, and error date

## Bill Search Service

The service searches bill information either by the single parameter or by combination of several parameters. The
service uses database paging for performance. If any optional parameters are invalid the service returns JSON with
warnings. It can be used by OCFO users and Industry users.

### Parameters

- [Security Token](../authentication.md#security-tokens)
- The following service parameters will be passed as JSON compliant to the JSON schema defined
  in [bill-search-request.json](https://github.com/USEPA/e-manifest/blob/master/Services-Information/Schema/bill-search-request.json)

- `billingAccount`: optional parameter, billing account of the facility (EPA Site ID):
- `billStatus`: optional parameter, one of the following values shall be provided:
  - `Unpaid`
  - `InProgress`
  - `ReadyForPayment`
  - `Paid`
  - `SentToCollections`
  - `Credit`
  - `ZeroBalance`
- `startDate`: Required parameter, retrieves bills based on the value of `bill.updatedDate`.
- `endDate`: Required parameter, retrieves bills based on the value of `bill.updatedDate`.
- `amountChanged`: optional parameter, if provided value is true the service will check conditions for retrieving bills
  where totalAmount has been changed from the original calculated amount at the beginning of the month.
- `pageNumber`: optional parameter, the system will return bills for the requested page. If `pageNumber` is not provided
  or invalid the system will return bills for the 1st page.

### Examples

```http
POST /rcrainfo/rest/api/v1/emanifest/manifest/search-bill HTTP/1.1
Host: rcrainfopreprod.epa.gov
Authorization: Bearer theSecurityTokenObtainedFromTheAuthService

{
    "billingAccount": "VATESTTSDF001",
    "billStatus": "Unpaid",
    "startDate": "2021-10-01T00:00:00.000-0400",
    "endDate": "2021-12-01T00:00:00.000-0400",
    "amountChanged": true,
    "pageNumber": 3
}
```

### Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).

   - If security token is for a state account and the user does not have billing admin permission,
     the system stops the processing and generates the following error:
     ```json
     {
       "error": "E_BillingAdminPermissions",
       "message": "The user does not have billing administration permission"
     }
     ```

2. [User Authorization](../authentication.md#user-authorization).
3. The System will validate Security Token

   - 3.1. If the Web Security Token is invalid, the system stops the processing and generates the
     following error:

     ```
     - E_SecurityApiTokenInvalid: Invalid Security Token
     ```

   - 3.2. If the Web Security Token expired, the system stops the processing and generates the
     following error:

     ```
     - E_SecurityApiTokenExpired: Security Token is Expired
     ```

   - 3.3. If Account was Inactivated after the token was issued, the system stops the processing and
     generates the following error:

     ```
     - E_SecurityApiInvalidStatus: This API Id is no longer active
     ```

   - 3.4. If security token is for a state account and the user does not have billing admin permission,
     the system stops the processing and generates the following error:
     ```
     - E_BillingAdminPermissions: The user does not have billing administration permission
     ```

4. The system will perform User Authorization.

   - 4.1. If the Industry User does not have industry permissions for any Site, the system will stop the
     processing and generates the following error:

     ```
     - E_IndustryPermissions: The industry user does not have industry permissions for any Site
     ```

   - 4.2. The System will check if the Security token is for the Industry account or if the Security
     token is for a state account with Billing Admin permission (OCFO/Compass).

     - 4.2.1 If the Security token is for a state account with Billing Admin permission
       (OCFO/Compass) the system will return data for all billingAccounts meeting
       specified search criteria.

     - 4.2.2 If the Security token is for an industry the system will return data only for
       billingAccounts that the account has access to and that meet specified search
       criteria.

5. The system will process the request

   - 5.1. If provided billingAccount is invalid, not registered, not active, or not found, the service will
     do the following

     - 5.1.1. The service will return an empty "bills" array.
     - 5.1.2. If the provided billingAccount is invalid, the service will return the following
       warning:
       ```
       {
           "message": "Provided billingAccount is invalid",
           "field": "billingAccount",
           "value": "[value of billingAccount] "
       }
       ```
     - 5.1.3. If provided billingAccount is not active, the service will return the following warning:
       ```
       {
           "message": "Provided billingAccount is not active ",
           "field": "billingAccount",
           "value": "[value of billingAccount] "
       }
       ```
     - 5.1.4. If provided billingAccount is not found, the service will return the following warning:
       ```
       {
           "message": "Provided billingAccount is not found ",
           "field": "billingAccount",
           "value": "[value of billingAccount] "
       }
       ```
     - 5.1.5. If the service was invoked by the Industry user, the service will list all valid billing
       accounts. The service will return following warning(s):
       ```
       {
           "message": " Valid billing account ",
           "field": "billingAccount",
           "value": "[value of billingAccount] "
       }
       ```

   - 5.2. If startDate and endDate are provided, the system will check if startDate and endDate are
     valid, and will determine the time range for the bills to return.

     - 5.2.1. The startDate is valid if startDate is later than emanifest start date and earlier than
       Current date and startDate is earlier than endDate.
     - 5.2.2. The startDate is invalid if startDate is later than Current date or startDate is earlier
       than emanifest start date.
     - 5.2.3. The endDate is valid if endDate is later than emanifest start date and earlier than
       Current date and endDate later than startDate.
     - 5.2.4. The endDate is invalid if endDate is later than Current date or endDate is earlier
       than emanifest start date.
     - 5.2.5. If the startDate is valid and endDate is invalid the service will return bills in the time
       range between startDate and Current date.
     - 5.2.6. If the endDate is valid and startDate is invalid the service will return bills in the time
       range between emanifest start date and endDate.
     - 5.2.7. If the endDate is invalid and startDate is invalid the service will return bills in the
       time range between emanifest start date and current Date.

   - 5.3. If startDate is not provided, the system will stop the processing and generates the following
     error:

     - E_SearchParameterRequiredStartDate: Missing required search parameter startDate

   - 5.4. If endDate is not provided, the system will stop the processing and generates the following
     error:

     - E_SearchParameterRequiredEndDate: Missing required search parameter endDate

   - 5.5. If startDate and endDate are not provided, the system will stop the processing and
     generates the following error:

     - E_SearchParameterRequiredStartDateEndDate: Missing required search parameters
       startDate and endDate

   - 5.6. If provided startDate is later than provided endDate, the system will stop the processing and
     generates the following error:

     ```
     - E_StartDateLaterThanEndDate: Provided StartDate is later than EndDate
     ```

   - 5.7. If StartDate is earlier than emanifest start date, the system will return the following warning
     in the return JSON:

     ```
     - E_ StartDateEarlierThanEmanifestStart: Provided StartDate is earlier than emanifest
       start
     ```

   - 5.8. If EndDate is earlier than emanifest start date, the system will return the following warning
     in the return JSON:

     ```
     - message "Provided EndDate is earlier than emanifest start date”
     - field: endDate
     - value: [value of endDate]
     ```

   - 5.9. If EndDate is later than Current date, the system will return the following warning in the
     return JSON:

     ```
     - message "Provided EndDate is later than Current date”
     - field: endDate
     - value: [value of endDate]
     ```

   - 9.10. If StartDate is later than Current date system will return the following warning in the
     return JSON:

     ```
     - message "Provided StartDate later than Current date
     - field: StartDate
     - value: [value of StartDate]
     ```

   - 9.11. If the provided pageNumber is larger than totalNumberOfPages or less than one , the
     system will return the following warning in the return JSON
     ```
     - "message": "Provided pageNumber must be equal or greater than one. pagenumber is set to
       1"
     - field: pageNumber
     - value: [value of page number]
     ```

6. The service will generate JSON containing one or multiple Bills. If the provided value of amountChanged is true,
   Bill.totalAmountChanged is true and bill.updatedDate is in the time range specified by startDate and endDate, the
   service will include the bill in the returned JSON. The response will contain the following information:

   - `totalNumberOfBills`: Total Number Of Bills for provided search criteria
   - `totalNumberOfPages`: Total Number Of Pages for provided search criteria
   - `currentPageNumber`: Current Page Number for provided search criteria
   - `searchedParameters`: valid parameters used in search
     - `field`: parameter field name
     - `value`: parameter value
   - `warnings`: validation errors for optional parameters
     - `message`: validation message
     - `field`: parameter field name
     - `value`: parameter value

   Each bill will contain the following information:

   - `billingAccount`: EPA Site Id
   - `billId`: bill id
   - `billStatus`: Following values can be returned: "Unpaid", "InProgress", "ReadyForPayment",
     "Paid", "SentToCollections", "Credit", "ZeroBalance"
   - `totalAmount`: if the billStatus is Credit then a negative value will be returned. If the billStatus
     is ZeroBalance then 0 value will be returned
   - `currentAmount`: The amount for manifests invoiced for the current billing period
   - `previousAmount`: The total for all manifests not paid or sent to collections for billing
     periods before the current period
   - `previousInterestAmount`: The total of interest fees occurred on the previous amounts for all
     manifests not paid or sent to collections for billing periods before the current period
   - `previousPenaltyAmount`: for invoices that are Unpaid after four months, the penalty amount
     for that invoice
   - `previousLateFeeAmount`: Total of the flat fee, penalty, and interest charges for all manifests
     and invoices not paid from billing periods before the current period
   - `dueDate` The date the invoice is due
   - `paidBy`: Contains the bill payee user id, for invoices that were mark as paid by the EPA, this
     element is not returned
   - `paymentType`: Contains payment type , Following values can be returned: "Credit", "Ach",
     for invoices that were mark as paid by the EPA, this element is not returned
   - `createdDate`: The date the invoice was created
   - `totalAmountChanged`: Indicates if the totalAmount has been changed from the original
     calculated amount at the beginning of the month.
   - `updatedDate`: The date the invoice was last updated
   - `lateFees` (when applicable) containing the following information:
     - `lateFeeBillId`: Bill Id which Late Fee is calculated for
     - `interestAmount`: the total interest amount for this lateFeeBillId
     - `penaltyAmount`: the total penalty amount for this lateFeeBillId
     - `lateFeeAmount`: the total interest, penalty, and flat fee amounts for this lateFeeBillId
     - `flatFeeAmount`: the total flat fee amount for this lateFeeBillId
     - `status`: the status of the invoice, please note that invoices sent to collection will be
       marked as inactive
   - `revisions`: (when applicable) containing the following information:
     - `amount`: Amount of adjustment on the invoice
     - `amountType`: "Current", “LateFee”
     - `adjustmentType`: "Increase", “Decrease”, “FullPayment”
     - `publicComments`:
     - `createdDate`
   - `RecalculationInfo`: (when applicable) containing the following information:
     - `recalculationReason`: “OriginalSiteBill”, “NewSiteBill”, “SoftDelete”

7. On success, the system returns JSON generated in section 4
8. If any system errors were encountered during processing, the system will return:

- error: containing error code, error message, error id, and error date
