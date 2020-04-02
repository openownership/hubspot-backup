import os
import datetime
import json
import csv
import zipfile

from dotenv import load_dotenv
from hubspot3 import Hubspot3
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession


load_dotenv()


def createFolder(session):
    metadata = {
        'name': datetime.datetime.utcnow().isoformat(),
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [os.getenv('GDRIVE_ROOT_FOLDER_ID')]
    }
    response = session.post(
        'https://www.googleapis.com/drive/v3/files?supportsAllDrives=true',
        json=metadata
    )
    response.raise_for_status()
    return response.json()['id']


def download(data, name):
    with open('backup/{}'.format(name), 'w') as f:
        f.write(json.dumps(data, indent=2, sort_keys=True))


def convertToCSV(name):
    csvName = 'backup/{}.csv'.format(name.split('.')[0])
    with open(csvName, 'w') as csvFile:
        with open('backup/{}'.format(name), 'r') as jsonFile:
            data = json.loads(jsonFile.read())
            # HubSpot's API responses are sparse objects, so we have to find
            # all the keys ourselves
            fieldnames = set()
            for record in data:
                fieldnames.update(list(record.keys()))
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


def compress(name):
    zipName = 'backup/{}.zip'.format(name.split('.')[0])
    with zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED) as zipObj:
        zipObj.write('backup/{}'.format(name))


def upload(name, session, folderId, mimeType):
    file_metadata = {
        'name': name,
        'mimeType': mimeType,
        'parents': [folderId]
    }
    start_response = session.post(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true',
        json=file_metadata
    )
    start_response.raise_for_status()
    resumable_uri = start_response.headers.get('Location')
    file = open('backup/{}'.format(name), 'rb')
    upload_response = session.put(resumable_uri, data=file)
    upload_response.raise_for_status()


def main():
    hubspot_client = Hubspot3(api_key=os.getenv('HUBSPOT_API_KEY'))
    service_account_info = json.loads(os.getenv('GDRIVE_SERVICE_ACCOUNT'))
    google_credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    authed_session = AuthorizedSession(google_credentials)

    contacts = hubspot_client.contacts.get_all(
        extra_properties=['hs_persona', 'country']
    )
    download(contacts, 'contacts.json')
    download(hubspot_client.companies.get_all(), 'companies.json')
    download(hubspot_client.engagements.get_all(), 'engagements.json')
    download(hubspot_client.tickets.get_all(), 'tickets.json')

    convertToCSV('contacts.json')
    convertToCSV('companies.json')

    compress('engagements.json')

    folderId = createFolder(authed_session)
    upload('contacts.csv', authed_session, folderId, 'text/csv')
    upload('companies.csv', authed_session, folderId, 'text/csv')
    upload('engagements.zip', authed_session, folderId, 'application/zip')
    upload('tickets.json', authed_session, folderId, 'application/json')


if __name__ == "__main__":
    main()
