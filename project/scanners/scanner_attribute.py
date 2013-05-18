
class ScannerAttribute:

    def __init__(self, key, raw_value, binned_value=None, bins=None):
        self.key = key
        self.raw_value = raw_value
        self.binned_value = binned_value
        self.bins = bins


def create_binary_attribute(key, value):
    return ScannerAttribute(key, int(value), int(value), [0, 1])
