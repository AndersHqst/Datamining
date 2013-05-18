from bs4 import BeautifulSoup


class Website():

    def __init__(self, dat_file):
        self.url = ''
        self.headers = {}

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
        self.soup = None
        self.dat_file = dat_file
        self.parse()

    def parse(self):
        line = self.dat_file.readline().decode('utf-8')
        while line:
            try:
                if line.startswith('### URL:'):
                    self.url = line.strip('### URL:').strip()

                elif line.startswith('### ALEXA_RANK:'):
                    self.alexa_rank = int(line.replace(
                        '### ALEXA_RANK:', '').strip())
                elif line.startswith('### ALEXA_RANK_DK:'):
                    self.alexa_rank_dk = int(line.replace(
                        '### ALEXA_RANK_DK:', '').strip())
                elif line.startswith('### MEASURED_TIME:'):
                    self.measured_response_time = float(
                        line.replace('### MEASURED_TIME:', '').strip())

                if line.startswith('### HEADERS:'):
                    line = self.dat_file.readline().decode('utf-8')
                    while not line.startswith('###'):
                        if not line.isspace():
                            chunks = line.split(':')
                            self.headers[chunks[0]] = ''.join(chunks[1:])
                        # print 'Header line: ', line
                        line = self.dat_file.readline().decode('utf-8')

                if line.startswith('### HTML:'):
                    # print 'Html first line: ', line
                    line = self.dat_file.readline().decode('utf-8')
                    while not line.startswith('###'):
                        if not line.isspace():
                            self.html += line
                        line = self.dat_file.readline().decode('utf-8')
                    self.soup = BeautifulSoup(self.html)

                elif line.startswith('### ROBOTS:'):
                    line = self.dat_file.readline().decode('utf-8')
                    while not line.startswith('###'):
                        self.robots += line
                        line = self.dat_file.readline().decode('utf-8')
                elif line.startswith('### ALEXA_LOAD_TIME'):
                    self.alexa_load_time = int(line.replace(
                        '### ALEXA_LOAD_TIME:', '').strip())
                elif line.startswith('### GOOGLE_PAGE_RANK'):
                    self.google_page_rank = int(line.replace(
                        '### GOOGLE_PAGE_RANK:', '').strip())
                elif line.startswith('### ALEXA_HAS_ADULT_CONTENT'):
                    self.alexa_adult_content = line.replace(
                        '### ALEXA_HAS_ADULT_CONTENT:', '').strip().lower() == 'true'
                elif line.startswith('### ALEXA_TITLE:'):
                    self.alexa_title = line.replace(
                        '### ALEXA_TITLE:', '').strip()
                elif line.startswith('### ALEXA_DESCRIPTION:'):
                    self.alexa_description = line.replace(
                        '### ALEXA_DESCRIPTION:', '').strip()
                elif line.startswith('### ALEXA_LANG:'):
                    self.alexa_lang = line.replace(
                        '### ALEXA_LANG:', '').strip()
                elif line.startswith('### ALEXA_LINKS_IN'):
                    self.alexa_links_in = int(line.replace(
                        '### ALEXA_LINKS_IN:', '').strip())
                line = self.dat_file.readline().decode('utf-8')

            except Exception, e:
                print 'Exception parsing .dat file: ', self.dat_file.name
                print 'Exception: ', e
                return
