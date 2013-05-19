import re
import time
import urllib2
import gzip
from StringIO import StringIO
from pagerank import GooglePageRank
from alexa import get_alexa_data
from data_builder import DataBuilder


class DataFetcher:

    """Handles the extraction of data from a list of websites (URLs)

    Data is scraped from the raw HTML, the HTTP headers and from the robots.txt file.
    Further, this data is supplemented by a request to Alexa and a request for the PageRank.
    """

    def __init__(self, sites, output_dir='output', output_log='output.log', error_log='errors.log'):
        self.sites = sites
        self.output_dir = output_dir
        self.output_log = output_log
        self.error_log = error_log

    def fetch(self, start=None, stop=None):
        """Fetch data from the websites in the interval [start, stop]."""

        start = start if start is not None else 0
        stop = min(stop, len(
            self.sites)) if stop is not None else len(self.sites)

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
            self.log_output('Fetched (%s in range %i to %i): %s' % (
                str(i + 1), start, stop, url))

    def fetch_site(self, builder, url):
        """Scrape data directly from the website itself."""

        try:
            request = urllib2.Request(url)
            start_time = time.time()

            # Simulate browser (some websites do not allow crawlers)
            opener = urllib2.build_opener()
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0'),
                ('Accept-Charset', 'utf-8'),
                ('Accept-encoding', 'gzip')
            ]

            # Get response
            response = opener.open(request, timeout=20)

            # Headers
            headers = '\n'.join(['%s: %s' % (h, response.headers.get(h))
                                for h in response.headers])

            # A rough estimate, but better than nothing
            encoding = 'latin-1' if response.info().get(
                'Content-Type').find('8859-1') >= 0 else 'utf-8'

            # Contents
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                page_contents = f.read().decode(encoding)
            else:
                page_contents = response.read().decode(encoding)

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
        """Fetch data from Alexa."""

        try:
            data = get_alexa_data(url)
            builder.append('ALEXA_RANK', data['total_rank'])
            builder.append('ALEXA_RANK_DK', data['dk_rank'])
            builder.append('ALEXA_DESCRIPTION', data['description'])
            builder.append('ALEXA_TITLE', data['title'])
            builder.append('ALEXA_LANG', data['langauge'])
            builder.append('ALEXA_LINKS_IN', data['links_in'])
            builder.append('ALEXA_HAS_ADULT_CONTENT', data[
                           'has_adult_content'])
            builder.append('ALEXA_LOAD_TIME', data['load_time'])
        except Exception as e:
            self.log_error(url, e)

    def fetch_robots(self, builder, url):
        """Read the robots.txt file."""

        try:
            request = urllib2.Request(url + '/robots.txt')
            response = urllib2.urlopen(request, timeout=20)
            robots = response.read().decode('utf-8') # We simply assume that it is ASCII or UTF-8
        except Exception as e:
            robots = ''
            self.log_error(url, 'Error when fetching robots.txt: %s' % e)

        builder.append('ROBOTS', robots, multiline=True)

    def fetch_pagerank(self, builder, url):
        """Fetch the Google PageRank."""
        gpr = GooglePageRank()
        rank = gpr.get_rank(url)
        rank = (rank if rank is not None else -1)
        builder.append('GOOGLE_PAGE_RANK', rank)

    def get_filename(self, url):
        """Convert a URL to a filesystem compatible filename."""
        url = url.replace('http://', '').replace('www', '')
        pattern = re.compile('[\W_]+')
        return '%s.dat' % pattern.sub('', url)

    def log_output(self, message):
        """Write output to a log file."""
        with open(self.output_log, 'a') as f:
            f.write(message + '\n')
        print message

    def log_error(self, url, message):
        """Write errors to an error log."""
        with open(self.error_log, 'a') as f:
            error = "Error in '%s': %s" % (url, message)
            f.write(error + '\n')

    def write_output_file(self, name, contents):
        """Utility method which writes to UTF-8 encoded file."""
        with open('%s/%s' % (self.output_dir, name), 'w') as f:
            f.write(contents.encode('utf-8'))
