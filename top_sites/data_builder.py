
class DataBuilder:

    def __init__(self):
        self.singleline_attributes = {}
        self.multiline_attributes = {}

    def append(self, key, value, multiline=False):
        if multiline:
            self.multiline_attributes[key] = value
        else:
            self.singleline_attributes[key] = value

    def generate(self):
        contents = u'### START ###\n\n'
        for key, value in self.singleline_attributes.iteritems():
            if isinstance(value, str):
                value = value.decode('utf-8')
            contents += u'### %s: %s\n\n' % (key, value)
        for key, value in self.multiline_attributes.iteritems():
            if isinstance(value, str):
                value = value.decode('utf-8')
            contents += u'### %s:\n%s\n\n' % (key, value)
        return contents + '### STOP ###'
