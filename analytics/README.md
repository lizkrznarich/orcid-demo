This Python script uses the Google Analytics, Drive and Sheets (via GSpread) APIs, as well as the ORCID Public API, to generate a custom analytics report, upload it to Drive and add external data from ORCID.

## Demo
A demo site that has Google Analytics tracking configured and displays data using this script is located at http://orcid.github.io/or2016-ga

## Pre-requisites
Slides that explain these pre-requesites are located at 

1. Create a [Google Analytics](https://analytics.google.com) account and set up tracking for your website
2. Develop Google Analytics queries using the [Analytics API](https://developers.google.com/analytics/devguides/reporting/core/v3/reference)
3. Create a new [Google Developer Console project](https://console.developers.google.com/project)
4. [Enable the Analytics and Drive APIs](https://console.developers.google.com/apis/library) for your project
5. Create a [Google Service Account](https://console.developers.google.com/apis/credentials) and download a P12 key 
6. [Enable domain-wide access](https://console.developers.google.com/iam-admin/serviceaccounts) for your service account 
7. [Grant your service account access to Google Analytics](https://analytics.google.com/analytics/web/#management/Settings) 
8. [Create a new Google Drive folder](https://drive.google.com/drive/my-drive) and grant your service account access to it


## Set up virtual environment 

5. `cd analytics`

6. `virtualenv venv`

7. `source ./venv/bin/activate` nix systesm `\venv\bin\activate` windows

8. `pip2 install -r requirements.txt` 

## Create config file 

1. Create a copy of the provided config_example.py file and name it config.py
    
        mv config_example.py config.py

2. Edit config.py to include default values for your Google Drive folder ID, p12 file location, Google Analytics view ID, and Google service account email 

    vim config.py

Your final config.py file should look something like:
    
    import argparse
    import time
    import calendar

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_id', default='0Bs0lFl2y-hZudnEvTDJZV63V2RpD', type=str)
    parser.add_argument('--secret_file_location', default='my_google_cred_secret_file.p12', type=str)
    parser.add_argument('--report_date_Y_m_d', default=time.strftime("%Y-%m-%d"), type=str)
    #enter dates as Y-m-d like 2016-05-31
    parser.add_argument('--start_date', type=str)
    parser.add_argument('--end_date', type=str)
    args = parser.parse_args()
    folder_id = args.folder_id
    start_date = args.start_date
    end_date = args.end_date
    report_date_Y_m_d = args.report_date_Y_m_d 
    secret_file_location = args.secret_file_location
    #global settings
    endpoint='https://pub.orcid.org'
    profile_id='ga:123456789'
    service_account_email='my-service-account-username@my-project-name.iam.gserviceaccount.com'

## Create reports
Run the build_report.py script, passing in the appropriate arguments:

`python build_report.py --start_date='2016-05-01' --end_date='2016-05-31'`

### Available args

**--folder_id** Google Drive folder ID for the parent folder that report csv files should be uploaded to

**--secret_file_location** Location of the Google API credentials file

**--report_date_Y_m_d** Date used in raw data file names (default time.strftime("%Y-%m-%d"))

**--start_date** Start date for Google Analytics queries YYYY-mm-dd

**--end_date**  End date for Google Analytics queries YYYY-mm-dd
