import argparse
import time
import calendar

parser = argparse.ArgumentParser()
parser.add_argument('--folder_id', default='0Bz0lLl2y-vZodnBvTXJZV3V2TzQ', type=str)
parser.add_argument('--secret_file_location', default='ORCID OR2016 GA-2a4cbd1e4d78.p12', type=str)
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
profile_id='ga:123116334'
service_account_email='or-2016-ga-service-account@orcid-or2016-ga.iam.gserviceaccount.com'
