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
    dois_orcid_counts  = []
    for doi in dois:
        orcid_count = search_orcid_doi(doi)
        dois_orcid_counts.append([doi, orcid_count])
    return dois_orcid_counts

def search_orcid_doi(doi):
    base_url = config.endpoint
    api_version = 'v1.2'
    search_endpoint = 'search/orcid-bio/?'
    query = {'defType' : 'edismax', 'q' : 'digital-object-ids:' + '"' + doi + '"'}
    encoded_query = urllib.urlencode(query)
    request_string = base_url + '/' + api_version + '/' + search_endpoint + encoded_query
    data = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, request_string)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/orcid+xml', 'Accept: application/json'])
    c.setopt(c.POST, 0)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    c.close()
    #return json.loads(data.getvalue())
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
