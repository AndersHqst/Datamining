
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
                if line.startswith('### RANK:'):
                    self.alexa_rank = int(line.strip('### RANK:').strip())
                if line.startswith('### TIME:'):
                    self.response_time = float(line.strip('### TIME:').strip())

                if line.startswith('### HEADERS:'):
                    line = self.dat_file.readline()
                    while not line.startswith('###'):
                        if not line.isspace():
                            chunks = line.split(':')
                            self.headers[chunks[0]] = ''.join(chunks[1:])
                        # print 'Header line: ', line
                        line = self.dat_file.readline()

                if line.startswith('### HTML:'):
                    # print 'Html first line: ', line
                    line = self.dat_file.readline()
                    while not line.startswith('###'):
                        if not line.isspace():
                            self.html += line
                        line = self.dat_file.readline()
                        # print 'Html line: ', line
                line = self.dat_file.readline()

            except Exception, e:
                print 'Exception parsing .dat file: ', self.dat_file.name
                print 'Exception: ', e
                return