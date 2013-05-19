
class ScannerAttribute:

    """A simple class the represent an attribute.

    This interface must be obeyed when returning attributes
    from a scanner.

    The raw value must always be provided. A binned value is optional.
    """

    def __init__(key, raw_value, binned_value=None, bins=None):
        self.key = key
        self.raw_value = raw_value
        self.binned_value = binned_value
        self.bins = bins
