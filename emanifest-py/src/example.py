# This script provides a basic example of how the emanifest library is used
# The script expects 2 environment variables to exists,
# 1. RCRAINFO_API_ID --> API ID (need Site Manager access to at least one site)
# 2. RCRAINFO_API_KEY --> corresponding API key, generated through RCRAInfo
# 3. You'll also need to substitute the manifest tracking number for a manifest
# for a manifest you have access to.

# emanifest python package is a wrapper around the python requests package
# every RcrainfoClient method returns a RcrainfoResponse object (except Auth)
# which contains 4 fields:
# RcrainfoResponse {
#   response:       requests.Response
#   ok:             requests.Response.ok
#   multipart_json: string                  part of multipart/mixed response if applicable
#   multipart_zip:  zipfile.ZipFile         part of multipart/mixed response if applicable
# }

import os
from emanifest import client as em


def main():
    eman = em.new_client('preprod')
    eman.Auth(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))

    # dot_numbers = eman.GetManMethodCodes()
    # print(dot_numbers.response.json())

    manifest_response = eman.GetAttachments("000012345GBF")
    if manifest_response.ok:
        # manifest_response.multipart_zip.extractall()
        print(manifest_response.multipart_json)


if __name__ == '__main__':
    main()
