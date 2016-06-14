import config
import google_drive as gd
import google_analytics as ga
import google_sheets as gs
import orcid_api as orcid
import time
import calendar
import os

#Subbing in hard-coded data for data from a local DB - in real life you might retrieve this using SQL
repo_dois = ['10.10.1038/nphys1170', '10.1087/20120404', '10.1002/0470841559.ch1', '10.6084/m9.figshare.1582705.v1', '10.1594/PANGAEA.726855', '10.6084/m9.figshare.3172084', '10.3207/2959859860']

def main():
  #Authenticate into Google Analytics API
  ga_service = ga.get_service('analytics', 'v3', ['https://www.googleapis.com/auth/analytics.readonly'])
  #Authenticate into Google Sheets API
  sheets_client = gs.create_sheets_client('https://spreadsheets.google.com/feeds')
  #Authenticate into Google Drive API
  gd_service = gd.get_service('drive', 'v3', ['https://www.googleapis.com/auth/drive'])
  #Retrieve data from ORCID Public API
  orcid_data = orcid.get_orcid_data(repo_dois)
  #Create a CSV file with Analytics data
  filedata = ga.create_csv(ga_service, config.report_date_Y_m_d, config.start_date, config.end_date, repo_dois)
  filename = "or2016_ga_demo_" + config.report_date_Y_m_d
  #Create CSV to Google Drive
  drive_file = gd.upload_csv_from_memory(filename, gd_service, filedata, config.folder_id)
  #Edit CSV with Gspread to add ORCID API data
  edit_drive_file = gs.edit_spreadsheet(sheets_client, drive_file, orcid_data)

if __name__ == '__main__':
  main()
