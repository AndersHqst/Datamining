import sys
from lxml import etree
from utils.bin_helper import bin_numeric
from scanner_attribute import ScannerAttribute

html5_tags = [
    'audio', 'video', 'source', 'embed', 'track', 'datalist', 
    'keygen', 'output', 'article', 'aside', 'bdi', 'command', 
    'details', 'dialog', 'summary', 'figure', 'figcaption', 
    'footer', 'header', 'hgroup', 'mark', 'meter', 'nav', 
    'progress', 'ruby', 'rt', 'rp', 'section', 'time', 'wbr'
]

def html5_scanner(website):
    is_found = False
    for tag in html5_tags:
        if len(website.soup.find_all(tag)) > 0:
            is_found = True
            break
    if '<!DOCTYPE html>' in website.html:
        is_found = True

    return ScannerAttribute('html5', int(is_found), int(is_found), [0, 1])

def html5_tag_scanner(website):
    count = 0
    for tag in html5_tags:
        count += len(website.soup.find_all(tag))

    bins = [1, 10, 50, sys.maxsize]
    return ScannerAttribute('html5_tags', count, bin_numeric(bins, count), bins)

def xhtml_scanner(website):
    try:
        etree.XML(website.html)
        return ScannerAttribute('xhtml', 1, 1, [0, 1])
    except:
        return ScannerAttribute('xhtml', 0, 0, [0, 1])
