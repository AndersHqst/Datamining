import sys
from urlparse import urlparse
from utils.url_helper import strip_web_prefix
from utils.preprocessing_helper import index_of_interval_bin
from scanner_attribute import ScannerAttribute

def links_count(website):
    internal_count = 0
    external_count = 0
    links = website.soup.find_all('a')
    for link in links:
        url = link.get('href')
        if url is not None:
            # Check if the site pointed to is the site being parsed itself
            # Tuple index 1 is net_loc
            info = urlparse(url)
            if strip_web_prefix(website.url) in info[1]:
                internal_count += 1
            else:
                external_count += 1
    return internal_count, external_count

def bins():
    return [(0, 10), (10, 30), (30, 60), (60, sys.maxsize)]

def external_links_scanner(website):
    internal_count, external_count = links_count(website)
    return ScannerAttribute('external_links_count', external_count, index_of_interval_bin(bins(), external_count), bins())

def internal_links_scanner(website):
    internal_count, external_count = links_count(website)
    return ScannerAttribute('internal_links_count', internal_count, index_of_interval_bin(bins(), internal_count), bins())
