from HTMLParser import HTMLParser
import urllib2
from urlparse import urlparse
from preprocessing_helper import index_of_interval_bin
import sys

class InternalLinksHTMLParser(HTMLParser):
    def __init__(self, website):
        HTMLParser.__init__(self)
        self.internal_links_count = 0
        self.site_url = strip_web_prefix(website.url)


    def handle_starttag(self, tag, attrs):
        href = next((b for a,b in attrs if a == 'href'), None)
        if tag == 'a' and href:
            info = urlparse(href)
            #Check if the site pointed to is the site being parsed itself
            #Tuple index 1 is net_loc
            if self.site_url in info[1]:
                self.internal_links_count += 1


    def handle_endtag(self, tag):
        pass


    def handle_data(self, data):
        pass


def bins():
    return [(0, 10), (10, 30), (30, 60), (60, sys.maxint)]


def internal_links_scanner(website):
    parser = InternalLinksHTMLParser(website)
    parser.feed(website.html)
    result = parser.internal_links_count
    return ('internal_links_count', index_of_interval_bin(bins(), result))