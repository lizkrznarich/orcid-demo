import config
import sys
import oauth2client
import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
from oauth2client import client
from apiclient.http import MediaFileUpload
from apiclient.http import MediaInMemoryUpload
import time
import string
import gspread
import io
from io import BytesIO

#Verify credentials and get google sheets service
def create_sheets_client(scope):
  f = open(config.secret_file_location, 'rb')
  key = f.read()
  f.close()
  credentials = SignedJwtAssertionCredentials(config.service_account_email, key, scope)
  sheets_client = gspread.authorize(credentials)
  return sheets_client

def edit_spreadsheet(sheets_client, drive_file, orcid_data):
    drive_file_FileId = drive_file.get('id')
    drive_file_worksheet = sheets_client.open_by_key(drive_file_FileId).sheet1
    orcid_record_col = drive_file_worksheet.find('ORCID Records with this DOI').col
    doi_orcid_count = 0
    for doi in orcid_data:
      try:
        doi_match_row = drive_file_worksheet.find(doi[0]).row
        drive_file_worksheet.update_cell(doi_match_row, orcid_record_col, doi[1])
        doi_orcid_count += 1 
      except:
        pass

    total_linked_orcid_row = drive_file_worksheet.find('Items linked to at least 1 ORCID iD').row
    drive_file_worksheet.update_cell(total_linked_orcid_row, 2, doi_orcid_count)   





