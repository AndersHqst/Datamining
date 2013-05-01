from HTMLParser import HTMLParser
import urllib2
import sys

class ImgHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.img_tags = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.img_tags += 1

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

def bins():
    return [(0, 5), (5, 10), (10, 15), (15, 20), (20, sys.maxint)]

def image_count_scanner(website):
    parser = ImgHTMLParser()
    parser.feed(website.html)
    return ('img_count', parser.img_tags)