from HTMLParser import HTMLParser

"""A website is considered to have a keyword, if the tag is present, and it contains text."""

class KeywordsStopException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)

class KeywordsHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.keywords = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            name = next((b for a, b in attrs if a == 'name'), '')
            content = next((b for a, b in attrs if a == 'content'), '')
            if name == 'keywords':
                 self.keywords = content
                 raise KeywordsStopException()

    def handle_endtag(self, tag):
        pass


    def handle_data(self, data):
        pass


def bins():
    return [0, 1]

def keyword_scanner(website):
    parser = KeywordsHTMLParser()
    try:
        parser.feed(website.html)
    except Exception as e:
        if not isinstance(e, KeywordsStopException):
            print 'KeywordsScanner Exception: ', e
            print 'site: ', website.url
            if hasattr(e, 'read'):
                print e.read()

    result = 0 < len(parser.keywords) and not parser.keywords.isspace()
    return ('has_keywords', int(result))