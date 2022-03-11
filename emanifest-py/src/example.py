import os
from emanifest import client


def main():
    eman = client.new_client('preprod')
    eman.Auth(os.getenv('RCRAINFO_API_ID'), os.getenv('RCRAINFO_API_KEY'))

    dot_numbers = eman.GetManMethodCodes()
    print(dot_numbers.response.json())


if __name__ == '__main__':
    main()
