from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
TARGET_SPREADSHEET_ID = '1SCphwNdUCzVt0FVR7lnzDQXWQ2kA66kT3xDF6sXruNA'
SAMPLE_RANGE_NAME = 'Sheet1'


def auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # create service to be used for following google sheets ops
    service = build('sheets', 'v4', credentials=creds)
    return service


def upload_to_sheets(values, service):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    body = {
        'values': values
    }

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().update(spreadsheetId=TARGET_SPREADSHEET_ID,
                                   range=SAMPLE_RANGE_NAME,
                                   body=body,
                                   valueInputOption='RAW'
                                   ).execute()


def read_current_sheet(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=TARGET_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    if 'values' in result:
        return result['values']
    else:
        return []
