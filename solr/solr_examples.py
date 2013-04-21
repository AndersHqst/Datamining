import urllib, urllib2
import json

#Add document
url = 'http://localhost:8983/solr/update/?commit=true'
data =
[
    {'id': 'TestDoc1', 'title': 'test1'},
    {'id': 'TestDoc2', 'title': 'another test'}
]
data = json.dumps(data)
req= urllib2.Request(url, data, headers={ 'Content-type': 'application/json' })
resp = urllib2.urlopen(req)

#query on id tag
url = 'http://localhost:8983/solr/select/?q=id:GB18030TEST'
resp = urllib2.urlopen(url)

#query some string
url = 'http://localhost:8983/solr/select/?q=Samsung'
resp = urllib2.urlopen(url)

#delete
url = 'http://localhost:8983/solr/update/?commit=true'
data = {'delete': { 'query': 'id:some_id' }}
data = json.dumps(data)
req= urllib2.Request(url, data, headers={ 'Content-type': 'application/json' })
resp = urllib2.urlopen(req)