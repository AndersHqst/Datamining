import sys
from utils.bin_helper import bin_numeric

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

    return 'html5',  int(is_found)

def html5_tag_scanner(website):
    count = 0
    for tag in html5_tags:
        count += len(website.soup.find_all(tag))

    bins = [1, 10, 50, sys.maxsize]
    return 'html5_tags', bin_numeric(bins, count)