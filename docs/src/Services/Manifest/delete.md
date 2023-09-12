# Manifest Delete Service

The Delete service deletes the manifest by provided Manifest Tracking Number. Depending on the manifest submission type,
the manifest can be deleted in the following statuses:

- "FullElectronic ": can be deleted only if in the `"Pending"` or `"Scheduled"` status
- `"Hybrid"`: can be deleted only if in the `"Pending"` or `"Scheduled"` status
- `"DataImage5Copy"`: can be deleted only if in the `"ReadyForSignature"` or "MtnValidationFailed" status
- `"Image"`: can be deleted only if originType = "Web" or "Service" and status is in the `"ReadyForSignature"` or "
  MtnValidationFailed" status

Service will check if the manifest is locked. The manifest is locked for delete when Manifest is in a queue for signing.

## Sequence of Steps

1. [Security Token Validation](../authentication.md#security-token-validation).
2. [User Authorization](../authentication.md#user-authorization).
3. The system will check if the provided manifest tracking number is valid and exists in the system.

   3.1 {{#include ../../components/mtn-validation-steps.md}}
