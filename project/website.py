
class Website():

    def __init__(self, dat_file):
        self.url = ""
        self.headers= {}
        self.alexa_rank = 0
        self.response_time = 0
        self.html = ""
        self.dat_file = dat_file
        self.parse()

    def parse(self):
        line = self.dat_file.readline()
        while line:
            try:
                if line.startswith('### URL:'):
                    self.url = line.strip('### URL:').strip()
                elif line.startswith('### RANK:'):
                    self.alexa_rank = int(line.strip('### RANK:').strip())
                elif line.startswith('### TIME:'):
                    self.response_time = float(line.strip('### TIME:').strip())
                elif line.startswith('### HEADERS:'):
                    header_line = self.dat_file.readline()
                    while not header_line.isspace():
                        # print 'header line: ', header_line
                        chunks = header_line.split(':')
                        self.headers[chunks[0]] = ''.join(chunks[1:])
                        header_line = self.dat_file.readline()
                elif line.startswith('### HTML:'):
                    html_line = self.dat_file.readline()
                    while not html_line.isspace():
                        self.html += html_line
                        html_line = self.dat_file.readline()
                line = self.dat_file.readline()

            except Exception, e:
                print 'Exception parsing .dat file: ', self.dat_file.name
                print 'Exception: ', e
                return

fd = open('1.dat', 'r')
ws = Website(fd)

print 'url: ', ws.url
print 'headers: ', ws.headers
print 'alexs: ', ws.alexa_rank
print 'response_time', ws.response_time
print 'html len', len(ws.html)