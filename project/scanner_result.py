
class ScannerAttribute:
    def __init__(key, raw_value, binned_value=None, bins=None):
        self.key = key
        self.raw_value = raw_value
        self.binned_value = binned_value
        self.bins = bins
