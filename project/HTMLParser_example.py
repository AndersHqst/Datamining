from HTMLParser import HTMLParser
import urllib2

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data

resp = urllib2.urlopen('http://www.google.com')
data = resp.read()
parser = MyHTMLParser()
parser.feed(data)
