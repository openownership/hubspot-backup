import os
import json

from dotenv import load_dotenv
from hubspot3 import Hubspot3


load_dotenv()


def download(data, name):
    with open('backup/{}.json'.format(name), 'w') as f:
        f.write(json.dumps(data, indent=2, sort_keys=True))


def main():
    client = Hubspot3(api_key=os.getenv('HUBSPOT_API_KEY'))
    download(
        client.contacts.get_all(extra_properties=['hs_persona', 'country']),
        'contacts'
    )
    download(client.companies.get_all(), 'companies')
    download(client.engagements.get_all(), 'engagements')
    download(client.tickets.get_all(), 'tickets')


if __name__ == "__main__":
    main()
