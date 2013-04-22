import urllib, urllib2
import json

#We have a running instance on AWS with solr installed
#All queries below will work, BESIDES adding html pages - I get a 500 :(
#Everything should work against the lates solr version running on localhost
#http://ec2-54-228-157-235.eu-west-1.compute.amazonaws.com/solr/

base_url = 'http://localhost:8983/'

#Add document
url = base_url + 'solr/update/?commit=true'
headers = { 'content-type': 'application/json' }
data =[{'id': 'TestDoc1', 'title': 'test1'},{'id': 'TestDoc2', 'title': 'another test'}]
data = json.dumps(data)
req= urllib2.Request(url, data, headers=headers)
resp = urllib2.urlopen(req)

#Add HTML document
#note that we have to provide som document id in the url
url = base_url + 'solr/update/extract?literal.id=documentId&commit=true'
headers = {'content-type': 'text/xml; charset=utf-8'}
data = urllib2.urlopen('http://www.google.com').read()
req = urllib2.Request(url, data=data, headers=headers)
resp = urllib2.urlopen(req)

#query on id tag
url = base_url + 'solr/select/?q=id:GB18030TEST'
resp = urllib2.urlopen(url)

#query some string, fl to filter returned fields:
#manual: http://wiki.apache.org/solr/CommonQueryParameters
url = base_url + 'solr/select/?q=keywords:biler&fl=id'
resp = urllib2.urlopen(url)

#delete
url = base_url + 'solr/update/?commit=true'
headers = { 'content-type': 'application/json' }
data = {'delete': { 'query': 'id:some_id' }} #set id:* to clean entire index..
data = json.dumps(data)
req= urllib2.Request(url, data, headers=headers)
resp = urllib2.urlopen(req)
