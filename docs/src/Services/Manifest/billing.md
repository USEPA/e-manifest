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
   - 3.8. If the billStatus is “Active” the processing will be stopped and system will generate the following error:
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
       - `submissionType`: "FullElectronic", “Hybrid”, “DataImage5Copy”, “Image”
       - `originType`: "Web", “Services”, “Mail”
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

## Bill Search Service
