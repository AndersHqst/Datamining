import re
import time
import urllib2
from alexa import get_alexa_data
from data_builder import DataBuilder

class DataFetcher:

    def __init__(self, sites, output_dir='output', output_log='output.log', error_log='errors.log'):
        self.sites = sites
        self.output_dir = output_dir
        self.output_log = output_log
        self.error_log = error_log

    def fetch(self, start=None, stop=None):
        start = start if start is not None else 0
        stop = min(stop, len(self.sites)) if stop is not None else len(self.sites)

        for i in range(start, stop):
            url = self.sites[i]
            name = self.get_filename(url)

            # Build data output
            builder = DataBuilder()
            builder.append('URL', url)
            self.fetch_site(builder, url)
            self.fetch_alexa(builder, url)
            self.fetch_robots(builder, url)
            self.fetch_pagerank(builder, url)

            self.write_output_file(name, builder.generate())
            self.log_output('Fetched (%s in range %i to %i): %s' % (str(i + 1), start, stop, url))

    def fetch_site(self, builder, url):
        try:
            request = urllib2.Request(url)
            start_time = time.time()

            # Simulate browser
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]

            # Get response
            response = opener.open(request, timeout = 20)
            headers = '\n'.join(['%s: %s' % (h, response.headers.get(h)) for h in response.headers])
            page_contents = response.read().decode('utf-8')

            download_time = time.time() - start_time
        except Exception as e:
            page_contents = 'An error occured: %s' % e
            headers = page_contents
            download_time = 0
            self.log_error(url, e)
        
        builder.append('MEASURED_TIME', '%.4f' % download_time)
        builder.append('HEADERS', headers, multiline=True)
        builder.append('HTML', page_contents, multiline=True)

    def fetch_alexa(self, builder, url):
        try:
            data = get_alexa_data(url)
            builder.append('ALEXA_RANK', data['total_rank'])
            builder.append('ALEXA_RANK_DK', data['dk_rank'])
            builder.append('ALEXA_DESCRIPTION', data['description'])
            builder.append('ALEXA_TITLE', data['title'])
            builder.append('ALEXA_LANG', data['langauge'])
            builder.append('ALEXA_LINKS_IN', data['links_in'])
            builder.append('ALEXA_HAS_ADULT_CONTENT', data['has_adult_content'])
            builder.append('ALEXA_LOAD_TIME', data['load_time'])
        except Exception as e:
            self.log_error(url, e)

    def fetch_robots(self, builder, url):
        pass

    def fetch_pagerank(self, builder, url):
        pass

    def get_filename(self, url):
        url = url.replace('http://', '').replace('www', '')
        pattern = re.compile('[\W_]+')
        return '%s.dat' % pattern.sub('', url)

    def log_output(self, message):
        with open(self.output_log, 'a') as f:
            f.write(message + '\n')
        print message

    def log_error(self, url, message):
        with open(self.error_log, 'a') as f:
            error = "Error in '%s': %s" % (url, message)
            f.write(error + '\n')

    def write_output_file(self, name, contents):
        with open('%s/%s' % (self.output_dir, name), 'w') as f:
            f.write(contents.encode('utf-8'))