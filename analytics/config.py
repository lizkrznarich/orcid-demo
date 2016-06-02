import argparse
import time
import calendar

parser = argparse.ArgumentParser()
parser.add_argument('--folder_id', default='0Bz0lLl2y-vZodnBvTXJZV3V2TzQ', type=str)
parser.add_argument('--owner', default='ejkrznarich@gmail.com', type=str)
parser.add_argument('--secret_file_location', default='ORCID OR2016 GA-2a4cbd1e4d78.p12', type=str)
parser.add_argument('--report_date_Y_m_d', default=time.strftime("%Y-%m-%d"), type=str)
parser.add_argument('--report_date_Y_mb', default=time.strftime("%Y-%m%b"), type=str)

temp_year = int(time.strftime("%Y"))
temp_month = int(time.strftime("%m")) - 1
if temp_month == 0:
  temp_month = 12
  temp_year = temp_year - 1
days_in_month = str(calendar.monthrange(temp_year, temp_month)[1])
if temp_month < 10:
  temp_month = '0' + str(temp_month)
parser.add_argument('--start_date', default=str(temp_year)+'-'+str(temp_month)+'-01', type=str)
parser.add_argument('--end_date', default=str(temp_year)+'-'+str(temp_month)+'-'+days_in_month, type=str)

parser.add_argument('--date', type=str)
args = parser.parse_args()

folder_id = args.folder_id
owner = args.owner
start_date = args.start_date
end_date = args.end_date
report_date_Y_m_d = args.report_date_Y_m_d 
report_date_Y_mb = args.report_date_Y_mb
secret_file_location = args.secret_file_location

#global settings
endpoint='https://pub.orcid.org'
profile_id='ga:123116334'
service_account_email='or-2016-ga-service-account@orcid-or2016-ga.iam.gserviceaccount.com'
