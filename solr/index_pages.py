import urllib, urllib2
import json

def html_url(doc_id):
    return 'http://localhost:8983/solr/update/extract?literal.id=' + doc_id + '&commit=true'
    # return 'http://ec2-54-228-157-235.eu-west-1.compute.amazonaws.com/solr/update/extract?literal.id=' + doc_id + '&commit=true'

def json_url():
    return 'http://localhost:8983/solr/update/?commit=true'
    # return 'http://ec2-54-228-157-235.eu-west-1.compute.amazonaws.com/solr/update/?commit=true'


def run(sites):
    """index a list of sites to solr
    @param sites: list of site names starting with http://www
    """
    html_headers = {
        'content-type': 'text/xml; charset=utf-8',
        'User-Agent'  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31',
        'Accept'      : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset' :' ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding' : 'gzip,deflate,sdch',
        'Accept-Language' : 'da-DK,da;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection' : 'keep-alive'
    }
    json_headers = { 'content-type': 'application/json' }

    indexed_sites = 0
    for site in sites:

        try:
            #Index raw html
            html_resp = urllib2.urlopen(site)
            html = html_resp.read()
            url = html_url(site)
            print 'url: ' + url
            req = urllib2.Request(url, data=html, headers=html_headers)
            html_resp = urllib2.urlopen(req)
            print 'indexed: ' + site
            #print result

            #Index headers
            headers = html_resp.headers.dict
            raw = [key + ':' + headers[key] for key in headers.keys()]
            raw = ''.join(raw)
            data =[{'id': 'header_' + site, 'text': raw}]
            data = json.dumps(data)
            req = urllib2.Request(json_url(), data, headers=json_headers)
            resp = urllib2.urlopen(req)

            indexed_sites += 1
            print 'indexed header for site: ' + site
        except Exception, e:
            print 'Exception: ', e
            print 'Contents: ', e.read()
            fd = open('not_indexed.txt', 'rw')
            fd.write(site + ',\n')
            fd.close()

    print 'Total sites: ', len(sites)
    print 'Sites index: ', indexed_sites

#get sites from csv file
fd = open('../page_rank/top_sites.csv')
sites = fd.read().split(',')
sites = filter(lambda x: len(x) > 0, sites)
sites = ['http://www.' + site for site in sites]
fd.close()

run(sites[:3])






