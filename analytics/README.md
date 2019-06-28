# API Extravaganza! Combining Google Analytics & ORCID APIs
This script uses the Google Analytics, Drive and Sheets (via GSpread) APIs, as well as the ORCID Public API, to generate a custom analytics report, upload it to Drive and add external data from ORCID.

See the [slides](22sep2016-ands-api-extravaganza.pdf) for a complete tutorial!

## Demo site
A demo site that has Google Analytics tracking configured and displays data using this script is located at http://orcid.github.io/analytics-demo

## Pre-requisites 
This list is daunting. See the [slides](22sep2016-ands-api-extravaganza.pdf) for a step-by-step guide (with pictures!)

1. Create a [Google Analytics](https://analytics.google.com) account and set up tracking for your website
2. Develop Google Analytics queries using the [Analytics API](https://developers.google.com/analytics/devguides/reporting/core/v3/reference)
3. Create a new [Google Developer Console project](https://console.developers.google.com/project)
4. [Enable the Analytics and Drive APIs](https://console.developers.google.com/apis/library) for your project
5. Create a [Google Service Account](https://console.developers.google.com/apis/credentials) and download a P12 key 
6. [Enable domain-wide access](https://console.developers.google.com/iam-admin/serviceaccounts) for your service account 
7. [Grant your service account access to Google Analytics](https://analytics.google.com/analytics/web/#management/Settings) 
8. [Create a new Google Drive folder](https://drive.google.com/drive/my-drive) and grant your service account access to it


## Set up virtual environment 
The project contains a requirements.txt file that allows you to run the scripts using a [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs). 

If you choose not to use a virtual environment, you'll need to install the dependencies listed in the requirements.txt file.

1. Clone the demo files
        
        git clone git@github.com:lizkrznarich/orcid-demo.git

2. Change to the analytics directory
        
        cd orcid-demo/analytics

3. Install virtualenv

        pip install virtualenv

2. Create a new virtual environment

        virtualenv venv

3. Activate the new virtual environment
        
        source ./venv/bin/activate

4. Install the project dependencies in the virtual environment

        pip2 install -r requirements.txt 

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
    parser.add_argument('--orcid_client_id', default='APP-XXXXXXXXXXXX', type=str)
    parser.add_argument('--orcid_client_secret', default='3a87028d-c84c-4d5f-8ad5-38a93181c9e1', type=str)
    args = parser.parse_args()
    folder_id = args.folder_id
    secret_file_location = args.secret_file_location
    report_date_Y_m_d = args.report_date_Y_m_d 
    start_date = args.start_date
    end_date = args.end_date
    orcid_client_id = args.orcid_client_id
    orcid_client_secret = args.orcid_client_secret
    #global settings
    search_endpoint='https://pub.orcid.org'
    token_endoint='https://orcid.org/oauth/token'
    profile_id='ga:123456789'
    service_account_email='my-service-account-username@my-project-name.iam.gserviceaccount.com'

## Edit Analytics queries
Edit the start_date, end_date, metrics, dimensions, and filters arguments for the run_query function in google_analytics.py to match your query parameters. 

        data = run_query(service, start_date, end_date, 'ga:totalEvents', 'ga:eventLabel', 'ga:eventAction==download')

## Create reports
Run the build_report.py script, passing in the appropriate arguments:

        python build_report.py --start_date='2016-05-01' --end_date='2016-05-31'

### Available args

**--folder_id** Google Drive folder ID for the parent folder that report csv files should be uploaded to

**--secret_file_location** Location of the Google API credentials file

**--report_date_Y_m_d** Date used in raw data file names (default time.strftime("%Y-%m-%d"))

**--start_date** Start date for Google Analytics queries YYYY-mm-dd

**--end_date**  End date for Google Analytics queries YYYY-mm-dd

**--orcid_client_id**  ORCID APID client ID 

**--orcid_client_secret**  ORCID APID client secret

_For info on setting up ORCID API credentials, see [Accessing the ORCID Public API](https://members.orcid.org/api/accessing-public-api)_

##Resources
- [Google Analytics Query Explorer](https://ga-dev-tools.appspot.com/quer y-explorer/)
- [Google Analytics Dimensions & Metrics Explorer](https://developers.google.com/analytics/devguides/reporting/core/dimsmets)
- [Google Developer Console](https://console.developers.google.com)
- [Google Analytics Core Reporting API documentation](https://developers.google.com/analytics/devguides/reporting/core/v4)
- [Google Drive API documentation](https://developers.google.com/drive/v3)
- [ORCID Search API documentation](https://members.orcid.org/api/tutorial-searching-api-12-and-earlier)
- [Gspread documentation](http://gspread.readthedocs.io)
- [Google Sheets API documentation](https://developers.google.com/sheets)
- [Google Charts API documentation](https://developers.google.com/chart)
- [ORCID API documentation](http://members.orcid.org/api)
- [ORCID Search API tutorial](http://members.orcid.org/api/tutorial-searching-data-using-api)
- [ORCID API app examples and code libraries](http://members.orcid.org/api/code-examples)
