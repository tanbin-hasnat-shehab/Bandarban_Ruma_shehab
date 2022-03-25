#from __future__ import print_function

#import os.path

#from google.auth.transport.requests import Request
#from google.oauth2.credentials import Credentials
#from google_auth_oauthlib.flow import InstalledAppFlow
import streamlit as st
from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
from google.oauth2 import service_account
SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# If modifying these scopes, delete the file token.json.
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '104Ixo6jiLk2PFqJqBKjt7K9IwX1kDkI89mZaWeSJHaM'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def input_data():
    ###############################################################################
    m_value=[[n,myverbs]]
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='ss!B2', valueInputOption='USER_ENTERED', body={'values':m_value})
    response = request.execute()
    ################################################################################################

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range='ss!A1:G13').execute()
    values = result.get('values', [])
    ################################################################################################
n=st.slider("কি খবর", 0, 30, value=5)
myverbs = st.radio('show values on graph:', ['yes','no'])

if n:
    input_data()


