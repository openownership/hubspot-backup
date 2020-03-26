# Hubspot Backup

This repo stores a backup of [OpenOwnership's Hubspot](https://app.hubspot.com/contacts/6472048/contacts/list/view/all/)
and the code which makes that backup and regularly updates it.

The backup itself is in [/backup](https://github.com/openownership/notion-backup/tree/master/backup)
this is a copy of Hubspots' contacts, companies and all of the 'engagements'
(emails, notes, meetings, calls, etc) we've recorded with them.

The code runs via a Github Action, which is scheduled to run at 4:05am every
day, as well as whenever code is pushed to the repository.

## Running the code locally

The code to run the backup lives in [/hubspot/export_hubspot.py]. To run it:

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
   ```

3. Run the python module: `python notion`

## Github Action config

The Github Action is configured via a `HUBSPOT_API_KEY` secret set up in
[the repo settings](https://github.com/openownership/notion-backup/settings/secrets).
This is then set as an env var for the python script to use.
