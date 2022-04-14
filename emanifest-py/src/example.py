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
#   json: string                  part of multipart/mixed response if applicable
#   zip:  zipfile.ZipFile         part of multipart/mixed response if applicable
# }

import os
from emanifest import client as em


def main():

    # change this manifest tracking number to one associated with your site
    mtn = '100032524ELC'

    eman = em.new_client('preprod')
    eman.Auth(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))

    dot_numbers = eman.GetManMethodCodes()
    # The Response can be accessed by calling the request.Response.json() method, or the json attribute for ease
    print(dot_numbers.response.json())
    print(dot_numbers.json)

    # Get Manifest json
    manifest = eman.GetManByMTN(mtn)
    with open('manifest.json', 'wb') as file:
        file.write(manifest.response.content)

    manifest_response = eman.GetAttachments(mtn)
    if manifest_response.ok:
        # uncommenting the below line will save a number of files to your working directory
        # manifest_response.zip.extractall()
        print(manifest_response.json)


if __name__ == '__main__':
    main()
