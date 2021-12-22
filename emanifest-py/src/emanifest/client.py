"""
e-Manifest library for using the e-Manifest API
see https://github.com/USEPA/e-manifest
"""
import os  # dev dependency
import sys
import requests
import datetime


# class RcrainfoResp:
#     def __init__(self, response: requests.Response):
#         self.status = response.status_code
#         self.data = response.json()


class RcrainfoClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.token_expiration = None

    def Auth(self, api_id, api_key):
        auth_url = "{base_url}/api/v1/auth/{api_id}/{api_key}".format(
            base_url=self.base_url,
            api_id=api_id,
            api_key=api_key)
        resp = requests.get(auth_url)
        if resp.ok:
            self.token = resp.json()['token']
            expire = resp.json()['expiration']
            # see datetime docs https://docs.python.org/3.7/library/datetime.html#strftime-strptime-behavior
            expire_format = '%Y-%m-%dT%H:%M:%S.%f%z'
            self.token_expiration = datetime.datetime.strptime(expire, expire_format)


def new_client(base_url):
    """
    Create instance of RCRAInfoClient
    Parameters:
        base_url (str): either 'prod', 'preprod' or url up to '/api/
    """
    if "https" not in base_url:
        urls = {
            "PROD": "https://rcrainfo.epa.gov/rcrainfoprod/rest/",
            "PREPROD": "https://rcrainfopreprod.epa.gov/rcrainfo/rest/"
        }
        if base_url.upper() in urls:
            base_url = urls[base_url.upper()]
        else:
            print("base_url not recognized")
            sys.exit(1)
    client = RcrainfoClient(base_url)
    return client


# temporary testing area
eman = new_client("preprod")
# set environment variable with os.environ[] or python-dotenv package with following keys
eman.Auth(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))
print(eman.token_expiration)
