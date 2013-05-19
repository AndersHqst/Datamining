
class ScannerAttribute:
    """ScannerAttribute defines the type that is expected to be returned by scanners.
    It wraps the data needed in association with an attribute."""

    def __init__(self, key, raw_value, binned_value=None, bins=None):
        """ Init a ScannerAttribute.

        :param key: attribute key
        :param raw_value: attribute value
        :param binned_value: bin value for the attribute value
        :param bins: all possible bins for the attribute value
        """
        self.key = key
        self.raw_value = raw_value
        self.binned_value = binned_value
        self.bins = bins


def create_binary_attribute(key, value):
    """Helper function for creating a binary attribute"""
    return ScannerAttribute(key, int(value), int(value), [0, 1])
