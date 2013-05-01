from HTMLParser import HTMLParser
import urllib2

class TitleHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_title_tag = False
        self.title = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.is_title_tag = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.is_title_tag = False
        # print "Encountered an end tag :", tag

    def handle_data(self, data):
        if self.is_title_tag:
            self.title = data
            self.is_title_tag = False
        # print "Encountered some data  :", data

#Should we decalare this as a default for all scanners?
#We might need to know the number of possible values an attribute can take for algorithms
def bins():
    return [0, 1]

def title_scanner(website):
    parser = TitleHTMLParser()
    parser.feed(website.html)
    key = 'title_tag'
    if not parser.title.isspace():
        return (key, 1)
    return (key, 0)



