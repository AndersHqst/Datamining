
class ArffWriter:

    """Write attribute data to an ARFF file

    This is a small utility class, which outputs attributes to
    a correctly formattet ARFF file (to be read by WEKA/RapidMiner)
    """

    def __init__(
        self, attribute_rows, attribute_info=None, filename=None, separator=',',
            include_header=True, surround_symbol="'", dataset_name='data', output_raw=False):

        self.separator = separator # Separator between attributes
        self.attribute_rows = attribute_rows # Attributes belonging to each website
        self.include_header = include_header # Whether or not header should be included
        self.surround_symbol = surround_symbol # Symbol to surround text with spaces
        self.dataset_name = dataset_name # Name of the dataset
        self.output_raw = output_raw # Whether or not to output the raw values

        # A dictionary with attribute names as keys, containing an object with
        # the following attributes: type, use_binned, exclude
        self.attribute_info = attribute_info # A dictionary 

        # Set filename or choose default filename
        if filename is None:
            self.filename = 'data.arff'
        else:
            self.filename = filename

        # Truncate output file
        with open(self.filename, 'w'):
            pass

    def write(self):
        """Generate and write the ARFF file."""
        with open(self.filename, 'a') as f:
            if self.include_header:
                f.write(self.create_header(self.attribute_rows[0]))
            for attributes in self.attribute_rows:
                f.write(self.create_row(attributes))

    def create_header(self, attributes):
        """Format the ARFF header."""

        # We sort the keys, so we always get the attributes in alphabetical order
        keys = sorted(attributes.keys())

        # Add name of dataset
        header = '@RELATION %s\n\n' % self.dataset_name

        # Create all the attributes information lines
        for key in keys:
            attribute = attributes[key]

            # If attribute_info is defined, we use this to determine the type
            if self.attribute_info is not None and self.attribute_info.has_key(key):
                info = self.attribute_info[key]

                # Skip excluded attributes
                if info.exclude:
                    continue

                header += '@ATTRIBUTE %s ' % key

                # Use either binned or raw values
                if info.use_binned:
                    header += '{' + ','.join([str(i)
                                             for i in range(len(attribute.bins))]) + '}\n'
                else:
                    header += '%s\n' % info.type

            # If attribute_info is not defined, output either raw or binned
            elif not self.output_raw and attribute.bins is not None:
                header += '@ATTRIBUTE %s ' % key
                header += '{' + ','.join([str(i)
                                         for i in range(len(attribute.bins))]) + '}\n'
            else:
                header += '@ATTRIBUTE %s ' % key
                header += 'string\n'

        header += '\n@DATA\n'

        return header

    def create_row(self, attributes):
        """Format a row of attributes."""

        # Remove all '-1' values, as we used these to represent missing values
        values_to_remove = ['-1']

        # Sort he attribute names
        keys = sorted(attributes.keys())
        values = []

        # Format each attribute on the line
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
        """Surround text with the surround_symbol."""
        return self.surround_symbol + text + self.surround_symbol
