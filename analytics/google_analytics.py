import argparse
import io
from io import BytesIO
import sys
import oauth2client
from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
from apiclient.discovery import build
from oauth2client import client
import config
import string
import unicodecsv as csv

#VERIFY CREDENTIALS AND GET GOOGLE ANALYTICS SERVICE
def get_service(api_name, api_version, scope):
  f = open(config.secret_file_location, 'rb')
  key = f.read()
  f.close()
  credentials = SignedJwtAssertionCredentials(config.service_account_email, key, scope=scope)
  http = credentials.authorize(httplib2.Http())
  service = build(api_name, api_version, http=http)
  return service

#RUN ANALYTICS QUERY
def run_query(service, start_date, end_date, metrics, dimensions, filters):
    if filters != '':
        api_query = service.data().ga().get(
            ids=config.profile_id,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            dimensions=dimensions,
            filters=filters)
    else: 
        api_query = service.data().ga().get(
            ids=config.profile_id,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            dimensions=dimensions)

    return api_query.execute()

def create_csv(service, report_date, start_date, end_date, dois):
    # Open temp csv file to write data
    filedata = io.BytesIO()
    writer = csv.writer(filedata)
    #Run Google Analytics query
    data = run_query(service, start_date, end_date, 'ga:totalEvents', 'ga:eventLabel', 'ga:eventAction==download')
    rows = data.get('rows')
    #1. Write client-report data to csv
    writer.writerow(["My Fancy Analytics Report!"])
    writer.writerow(["Generated on " + report_date])
    writer.writerow(["Data for " + start_date + " to " + end_date])
    writer.writerow([])
    writer.writerow(["Aggregate Data"])
    writer.writerow(["Items in repository", len(dois)])
    writer.writerow(["Items downloaded at least once", len(rows)])
    writer.writerow(["Items linked to at least 1 ORCID iD"])
    writer.writerow([])
    writer.writerow(["Item Data"])
    writer.writerow(["DOI", "Downloads", "ORCID Records with this DOI"])
    if rows is not None:
        for r in rows:
            writer.writerow([r[0], r[1]])
    writer.writerow([])
    return filedata.getvalue()


#MAIN FUNCTION
def main():
    if __name__ == '__main__':
        main()
