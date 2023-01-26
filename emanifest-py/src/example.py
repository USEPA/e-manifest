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

from emanifest import new_client


def main():
    # change this manifest tracking number to one associated with your site
    mtn = '100032524ELC'

    rcrainfo = new_client('preprod')
    rcrainfo.authenticate(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))

    dot_numbers = rcrainfo.get_man_method_codes()
    # The Response can be accessed by calling the request.Response.json() method, or the json attribute for ease
    # These should print the same json
    print(dot_numbers.response.json())
    print(dot_numbers.json)

    # Get Manifest json
    manifest = rcrainfo.get_manifest(mtn)
    print(manifest.json)
    # uncommenting the below will save manifest to './manifest.json'
    # if manifest.ok:
    #     with open('manifest.json', 'wb') as file:
    #         file.write(manifest.response.content)

    manifest_attachments = rcrainfo.get_manifest_attachments(mtn)
    print(manifest_attachments.ok)
    # uncommenting the below line will save a number of files to your working directory
    # if manifest_attachments.ok:
    #     manifest_attachments.zip.extractall()

    # update the paper manifest with the path to .json and .zip file
    update_resp = rcrainfo.update_manifest('example_update.json', 'example_update.zip')
    print(update_resp.ok)

    # or pass json as a string
    with open('example_update.json') as f:
        data = f.read()  # data is a string containing the manifest json
        update_resp = rcrainfo.update_manifest(data)
        print(update_resp.ok)


if __name__ == '__main__':
    main()
