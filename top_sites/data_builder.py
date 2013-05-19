
class DataBuilder:

    """Utility class for generating data documents in an easy to parse format."""

    def __init__(self):
        self.singleline_attributes = {}
        self.multiline_attributes = {}

    def append(self, key, value, multiline=False):
        """Add data to the document."""
        if multiline:
            self.multiline_attributes[key] = value
        else:
            self.singleline_attributes[key] = value

    def generate(self):
        """Generate the formatted document.

        The document will have the format:
        ### START ###

        ### <key>: <singleline-value>

        ### <key>: <singleline-value>

        ### <key>:
        <multiline-value>

        ### <key>:
        <multiline-value>

        ### STOP ###
        """

        contents = u'### START ###\n\n'

        # Add singleline values
        for key, value in self.singleline_attributes.iteritems():
            if isinstance(value, str):
                value = value.decode('utf-8')
            contents += u'### %s: %s\n\n' % (key, value)

        # Add multiline values
        for key, value in self.multiline_attributes.iteritems():
            if isinstance(value, str):
                value = value.decode('utf-8')
            contents += u'### %s:\n%s\n\n' % (key, value)

        return contents + '### STOP ###'
