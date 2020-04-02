# Hubspot Backup

This repo makes a backup of OpenOwnership's Hubspot CRM and saves it into our
team GDrive.

The code runs via a Github Action, which is scheduled to run at 4:05am every
day, as well as whenever code is pushed to the repository.

## Running the code locally

The code to run the backup lives in [/hubspot/export_hubspot.py](https://github.com/openownership/notion-backup/tree/master/hubspot/export_hubspot.py). To run it:

1. Install requirements

   ```shell
   git clone git@github.com:openownership/hubspot-backup.git
   cd hubspot-backup
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   touch .env
   ```

2. Set your `HUBSPOT_API_KEY` in the `.env` file:

   ```shell
   HUBSPOT_API_KEY=<get-the-key-from-hubspot>
   GDRIVE_ROOT_FOLDER_ID=<get-the-folder-id-from-gdrive>
   GDRIVE_SERVICE_ACCOUNT=<get-the-service-account-info-from-1password>
   ```

3. Run the python module: `python hubspot`

## Github Action config

The Github Action is configured via secrets set up in
[the repo settings](https://github.com/openownership/notion-backup/settings/secrets).
These are then set as env vars for the python script to use.
