import json
from . import papersCache as pc
import re
import hashlib
import urllib


# retrieve the metadata available at doi.org
# store retrieved json data in cache
# return json data
def getDoi(doi):
    check_doi = re.match(r'^https?://(dx\.)?doi\.org/', doi)
    if check_doi is not None:
        doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi)

    # url = 'http://doi.org/' + urllib.quote_plus(doi)
    # request = urllib2.Request(url, headers={"Accept": "application/vnd.citationstyles.csl+json"})
    url = 'http://doi.org/' + urllib.parse.quote_plus(doi)
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.citationstyles.csl+json"})
    try:
        response = urllib.request.urlopen(request)
        html_raw = response.read()
        json_data = json.loads(html_raw)
        # as doi's use '/' chars, we do an md5 of the doi as the filename
        filename = hashlib.md5(doi.encode()).hexdigest()
        pc.dumpJson(filename, json_data, filetype='raw/doi')
        return json_data
    except urllib.error.HTTPError as e:
        print("DOI: "+doi+" error: "+str(e.code))
        return None
    except ValueError as e:
        print("DOI: "+doi+" error: "+str(e))
        return None
