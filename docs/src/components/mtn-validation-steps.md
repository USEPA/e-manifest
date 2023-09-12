The system will check if the provided MTN is valid and exists in the system. Manifest Tracking Number shall be
compliant with following rules:

    - Nine numeric characters + valid three character Manifest Tracking Suffix
    - If the provided Manifest Tracking Number does not have valid format the processing will be stopped and system
      generates the following error:
      - `E_InvalidManifestTrackingNumber: Provided Manifest Tracking Number has invalid format`
    - If the provided Manifest Tracking Number does not have a valid suffix the processing will be stopped and system
      generates the following error:
      - `E_InvalidManifestTrackingNumberSuffix: Provided Manifest Tracking Number has invalid`
    - If the Manifest Tracking Number is not in the system the processing will stop and the system generates the
      following error:
      - `E_ ManifestTrackingNumberNotFound: Provided Manifest Tracking Number was not found`
