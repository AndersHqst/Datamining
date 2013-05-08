from HTMLParser import HTMLParser

"""True is a website uses google analytics"""

class AnalyticsStopException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)

class AnalyticsHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.has_analytics = False
        self.is_script = False

    def handle_starttag(self, tag, attrs):
        self.is_script = False
        if tag == 'script':
            self.is_script = True


    def handle_endtag(self, tag):
        self.is_script = False


    def handle_data(self, data):
        if self.is_script == True:
            if 'google-analytics.com/ga.js' in data:
                self.has_analytics = True
                raise AnalyticsStopException()



def bins():
    return [0, 1]

def analytics_scanner(website):
    parser = AnalyticsHTMLParser()
    try:
        parser.feed(website.html)
    except Exception as e:
        if not isinstance(e, AnalyticsStopException):
            print 'AnalyticsScanner Exception: ', e
            print 'site: ', website.url
            if hasattr(e, 'read'):
                print e.read()
    return ('has_analytics', int(parser.has_analytics))