import argparse
import io
from io import BytesIO
import sys
import config
import string
import pycurl
import urllib
import json

def get_orcid_data(dois):
    token = get_orcid_token()
    dois_orcid_counts  = []
    for doi in dois:
        orcid_count = search_orcid_doi(doi, token)
        dois_orcid_counts.append([doi, orcid_count])
    return dois_orcid_counts

def get_orcid_token():
    #set request variables
    client_id = config.orcid_client_id
    client_secret = config.orcid_client_secret
    token_endpoint = config.token_endpoint
    data = BytesIO()
    #create post data
    post_data = {'client_id': client_id, 'client_secret': client_secret, 'scope': '/read-public', 'grant_type': 'client_credentials'}
    #url encode post data
    postfields = urllib.urlencode(post_data)
    #create and send http request
    c = pycurl.Curl()
    c.setopt(c.URL, token_endpoint)
    c.setopt(c.HTTPHEADER, ['Accept: application/json'])
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    c.close()
    #get request response
    json_object = json.loads(data.getvalue())
    token = json_object['access_token']
    return token

def search_orcid_doi(doi, token):
    #set request variables
    base_url = config.search_endpoint
    api_version = 'v1.2'
    search_endpoint = 'search/orcid-bio/?'
    data = BytesIO()
    query = {'defType' : 'edismax', 'q' : 'digital-object-ids:' + '"' + doi + '"'}
    #url encode query
    encoded_query = urllib.urlencode(query)
    #create request string
    request_string = base_url + '/' + api_version + '/' + search_endpoint + encoded_query
    #create and send http request
    c = pycurl.Curl()
    c.setopt(c.URL, request_string)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/orcid+xml', 'Accept: application/json', 'Authorization: Bearer %s' % token])
    c.setopt(c.POST, 0)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    c.close()
    #get request response
    json_object = json.loads(data.getvalue())
    search_results = json_object['orcid-search-results']
    num_results = search_results["num-found"]
    return num_results

    #optionally get a list of orcid ids that list the current doi
    #orcid_ids = []
    #for result in search_results['orcid-search-result']:
        #orcid_id = result['orcid-profile']['orcid-identifier']['path']
        #orcid_given_names = result['orcid-profile']['orcid-bio']['personal-details']['given-names']['value']
        #orcid_family_names = result['orcid-profile']['orcid-bio']['personal-details']['family-name']['value']
        #orcid_data.append([orcid_id, orcid_given_names, orcid_family_names])
    #return orcid_ids

if __name__ == '__main__':
    main()
