import urllib, urllib2
import json

def html_url(doc_id):
    return 'http://localhost:8983/solr/update/extract?literal.id=' + doc_id + '&commit=true'

def json_url():
    return 'http://localhost:8983/solr/update/?commit=true'

def run():
    html_headers = {'content-type': 'text/xml; charset=utf-8'}
    json_headers = { 'content-type': 'application/json' }

    #get sites
    fd = open('../page_rank/top_sites.csv')
    sites = fd.read().split(',')
    sites = filter(lambda x: len(x) > 0, sites)
    fd.close()

    for site in sites:

        try:
            #Index raw html
            html_resp = urllib2.urlopen('http://www.' + site)
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

            print 'indexed header for site: ' + site
        except Exception, e:
            print 'Exception: ', e

run()






