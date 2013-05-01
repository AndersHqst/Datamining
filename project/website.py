
class Website():

    def __init__(self, dat_file):
        self.url = ''
        self.headers= {}

        self.alexa_rank = 0
        self.alexa_rank_dk = 0
        self.google_page_rank = 0

        self.alexa_load_time = 0
        self.measured_response_time = 0

        self.alexa_adult_content = False
        self.alexa_title = ''
        self.alexa_description = ''
        alexa_lang = ''
        alexa_links_in = 0

        self.robots = ''

        self.html = ''
        self.dat_file = dat_file
        self.parse()

    def parse(self):
        line = self.dat_file.readline()
        while line:
            try:
                if line.startswith('### URL:'):
                    self.url = line.strip('### URL:').strip()
                elif line.startswith('### ALEXA_RANK:'):
                    self.alexa_rank = int(line.strip('### ALEXA_RANK:').strip())
                elif line.startswith('### ALEXA_RANK_DK:'):
                    self.alexa_rank_dk = int(line.strip('### ALEXA_RANK_DK:').strip())
                elif line.startswith('### MEASURED_TIME:'):
                    self.measured_response_time = float(line.strip('### MEASURED_TIME:').strip())
                elif line.startswith('### HEADERS:'):
                    header_line = self.dat_file.readline()
                    while not header_line.isspace():
                        # print 'header line: ', header_line
                        chunks = header_line.split(':')
                        self.headers[chunks[0]] = ''.join(chunks[1:])
                        header_line = self.dat_file.readline()
                elif line.startswith('### HTML:'):
                    html_line = self.dat_file.readline()
                    while not html_line.startswith('###'):
                        self.html += html_line
                        html_line = self.dat_file.readline()
                elif line.startswith('### ROBOTS:'):
                    robots_line = self.dat_file.readline()
                    while not html_line.startswith('###'):
                        self.robots += robots_line
                        robots_line = self.dat_file.readline()
                elif line.startswith('### ALEXA_LOAD_TIME'):
                    self.alexa_load_time = int(line.strip('### ALEXA_LOAD_TIME:').strip())
                elif line.startswith('### GOOGLE_PAGE_RANK'):
                    self.google_page_rank = int(line.strip('### GOOGLE_PAGE_RANK:').strip())
                elif line.startswith('### ALEXA_HAS_ADULT_CONTENT'):
                    self.alexa_adult_content = bool(line.strip('### ALEXA_HAS_ADULT_CONTENT:').strip())
                elif line.startswith('### ALEXA_TITLE:'):
                    self.alexa_title = line.strip('### ALEXA_TITLE:').strip()
                elif line.startswith('### ALEXA_DESCRIPTION:'):
                    self.alexa_description = line.strip('### ALEXA_DESCRIPTION:').strip()
                elif line.startswith('### ALEXA_LANG:'):
                    self.alexa_lang = line.strip('### ALEXA_LANG:').strip()
                elif line.startswith('### ALEXA_LINKS_IN'):
                    self.alexa_links_in = int(line.strip('### ALEXA_LINKS_IN:').strip())
                line = self.dat_file.readline()

            except Exception, e:
                print 'Exception parsing .dat file: ', self.dat_file.name
                print 'Exception: ', e
                return