import argparse
import time
import calendar

parser = argparse.ArgumentParser()
parser.add_argument('--folder_id', default='YOUR FOLDER ID HERE', type=str)
parser.add_argument('--secret_file_location', default='YOUR P12 FILE LOCATION HERE', type=str)
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
profile_id='YOUR GOOGLE ANALYTICS VIEW ID HERE'
service_account_email='YOUR GOOGLE SERVICE ACCOUNT EMAIL ADDRESS HERE'
