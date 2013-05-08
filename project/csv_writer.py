
class CsvWriter:

    def __init__(self, attribute_rows, filename=None, separator=',', include_header=True, surround_symbol=''):
        self.separator = separator
        self.attribute_rows = attribute_rows
        self.include_header = include_header
        self.surround_symbol = surround_symbol

        if filename is None:
            self.filename = 'data.csv'
        else:
            self.filename = filename

        with open(self.filename, 'w'):
            pass

    def write(self):
        with open(self.filename, 'a') as f:
            if self.include_header:
                f.write(self.create_header_row(self.attribute_rows[0]))
            for attributes in self.attribute_rows:
                f.write(self.create_row(attributes))

    def create_header_row(self, attributes):
        keys = [self.surround(key) for key in sorted(attributes.keys())]
        return self.separator.join(keys) + '\n'

    def create_row(self, attributes):
        values_to_remove = ['-1', 'UNKNOWN']

        keys = sorted(attributes.keys())
        values = [self.surround(str(attributes[key])) for key in keys]
        values = [val if not val in values_to_remove else '' for val in values]

        return self.separator.join(values) + '\n'

    def surround(self, text):
        return self.surround_symbol + text + self.surround_symbol
