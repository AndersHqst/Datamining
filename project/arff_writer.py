
class ArffWriter:

    def __init__(self, attribute_rows, attribute_info=None, filename=None, separator=',', 
	        include_header=True, surround_symbol="'", dataset_name='data', output_raw=False):
        self.separator = separator
        self.attribute_rows = attribute_rows
        self.include_header = include_header
        self.surround_symbol = surround_symbol
        self.dataset_name = dataset_name
        self.output_raw = output_raw
        self.attribute_info = attribute_info

        if filename is None:
            self.filename = 'data.arff'
        else:
            self.filename = filename

        with open(self.filename, 'w'):
            pass

    def write(self):
        with open(self.filename, 'a') as f:
            if self.include_header:
                f.write(self.create_header(self.attribute_rows[0]))
            for attributes in self.attribute_rows:
                f.write(self.create_row(attributes))

    def create_header(self, attributes):
        keys = sorted(attributes.keys())

        header = '@RELATION %s\n\n' % self.dataset_name

        for key in keys:
            attribute = attributes[key]

            if self.attribute_info is not None and self.attribute_info.has_key(key):
                info = self.attribute_info[key]
                
                if info.exclude:
                    continue

                header += '@ATTRIBUTE %s ' % key
                if info.use_binned:
                    header += '{' + ','.join([str(i) for i in range(len(attribute.bins))]) + '}\n'
                else:
                    header += '%s\n' % info.type

            elif not self.output_raw and attribute.bins is not None:
                header += '@ATTRIBUTE %s ' % key
                header += '{' + ','.join([str(i) for i in range(len(attribute.bins))]) + '}\n'
            else:
                header += '@ATTRIBUTE %s ' % key
                header += 'string\n'

        header += '\n@DATA\n'

        return header

    def create_row(self, attributes):
        values_to_remove = ['-1']

        keys = sorted(attributes.keys())
        values = []

        for key in keys:
            attribute = attributes[key]

            # Get raw or binned value
            if self.attribute_info is not None and self.attribute_info.has_key(key):
                info = self.attribute_info[key]
                if info.exclude:
                    continue
                if info.use_binned:
                    value = str(attribute.binned_value)
                else:
                    value = str(attribute.raw_value) 
            elif not self.output_raw and attribute.binned_value is not None:
                value = str(attribute.binned_value)
            else:
                value = str(attribute.raw_value)

            # If value contains space, it must be quoted
            if ' ' in value:
                value = self.surround(value)

            # Insert ? instead of missing values
            if not value in values_to_remove and value.strip() != '':
                values.append(value)
            else:
                values.append('?')

        return self.separator.join(values) + '\n'

    def surround(self, text):
        return self.surround_symbol + text + self.surround_symbol
