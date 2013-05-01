from HTMLParser import HTMLParser

"""A website is considered to have a description, if the tag is present, and it contains text."""

class DescriptionStopException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)

class DescriptionHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.description = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            name = next((b for a, b in attrs if a == 'name'), '')
            content = next((b for a, b in attrs if a == 'content'), '')
            if name == 'description':
                 self.keywords = content
                 raise DescriptionStopException()


    def handle_endtag(self, tag):
        pass


    def handle_data(self, data):
        pass



def bins():
    return [0, 1]

def description_scanner(website):
    parser = DescriptionHTMLParser()
    try:
        parser.feed(website.html)
    except Exception as e:
        if not isinstance(e, DescriptionStopException):
            print 'DescriptionScanner Exception: ', e
            print 'site: ', website.url
            if hasattr(e, 'read'):
                print e.read()

    result = 0 < len(parser.description)
    return ('has_description', int(result))