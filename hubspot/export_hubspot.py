import os
import json

from dotenv import load_dotenv
from hubspot3 import Hubspot3


load_dotenv()


def downloadContacts(client):
    contacts = client.contacts.get_all()
    with open('backup/contacts.json', 'w') as f:
        f.write(json.dumps(contacts, indent=2, sort_keys=True))


def downloadCompanies(client):
    companies = client.companies.get_all()
    with open('backup/companies.json', 'w') as f:
        f.write(json.dumps(companies, indent=2, sort_keys=True))


def downloadEngagements(client):
    engagements = client.engagements.get_all()
    with open('backup/engagements.json', 'w') as f:
        f.write(json.dumps(engagements, indent=2, sort_keys=True))


def main():
    client = Hubspot3(api_key=os.getenv('HUBSPOT_API_KEY'))
    downloadContacts(client)
    downloadCompanies(client)
    downloadEngagements(client)


if __name__ == "__main__":
    main()
