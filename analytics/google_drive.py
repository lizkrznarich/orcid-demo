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
import io
from io import BytesIO

#Verify credentials and get google drive service
def get_service(api_name, api_version, scope):
  f = open(config.secret_file_location, 'rb')
  key = f.read()
  f.close()
  credentials = SignedJwtAssertionCredentials(config.service_account_email, key, scope=scope)
  http = credentials.authorize(httplib2.Http())
  service = build(api_name, api_version, http=http)
  return service

def upload_csv_from_memory(filename, service, output, folder_id):
    response = checkIfExists(filename, service, folder_id)
    if response is None:
        file = create_file(filename, service, output, folder_id)
    else:
        fileId = response['files'][0]
        file = update_file(filename, service, output, fileId)
    return file

def create_file(filename, service, output, folder_id):
    file_metadata = {
        'name' : filename,
        'mimeType' : 'application/vnd.google-apps.spreadsheet',
        'parents' : [ folder_id ]
    }
    media = MediaInMemoryUpload(output, mimetype='text/csv', resumable=False)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file

def update_file(filename, service, output, fileId ):
    file_metadata = {
        'name' : filename,
        'mimeType' : 'application/vnd.google-apps.spreadsheet'
    }
    media = MediaInMemoryUpload(output, mimetype='text/csv', resumable=False)
    file = service.files().update(fileId=fileId['id'], body=file_metadata, fields='id', media_body=media).execute()
    return file

def checkIfExists(filename, service, folder_id):
    params={}
    params['q'] = "'%s' in parents and name = '%s' and trashed = False" % (folder_id, filename)
    params['pageSize'] = 1000
    response = service.files().list(**params).execute()
    if len(response['files']) > 0:
      return response
    return None

#MAIN FUNCTION
def main():
  if __name__ == '__main__':
    main()
