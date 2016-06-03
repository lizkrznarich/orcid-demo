import config
import google_drive as gd
import google_analytics as ga
import google_sheets as gs
import orcid_api as orcid
import time
import calendar
import os

repo_dois = ['10.10.1038/nphys1170', '10.1087/20120404', '10.1002/0470841559.ch1', '10.6084/m9.figshare.1582705.v1', '10.1594/PANGAEA.726855', '10.6084/m9.figshare.3172084', '10.3207/2959859860']

def main():
  ga_service = ga.get_service('analytics', 'v3', ['https://www.googleapis.com/auth/analytics.readonly'])
  sheets_client = gs.create_sheets_client('https://spreadsheets.google.com/feeds')
  gd_service = gd.get_service('drive', 'v3', ['https://www.googleapis.com/auth/drive'])
  orcid_data = orcid.get_orcid_data(repo_dois)
  filedata = ga.create_csv(ga_service, config.report_date_Y_m_d, config.start_date, config.end_date, repo_dois)
  filename = "or2016_ga_demo_" + config.report_date_Y_m_d
  drive_file = gd.upload_csv_from_memory(filename, gd_service, filedata, config.folder_id)
  edit_drive_file = gs.edit_spreadsheet(sheets_client, drive_file, orcid_data)

if __name__ == '__main__':
  main()
