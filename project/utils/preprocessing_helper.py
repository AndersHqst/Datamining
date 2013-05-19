import sys


def index_of_interval_bin(bins, val):
    """Return bin index, using style-1 bins.

    Returns index of the bin that the values should be binned to.
    Values are binned in range: [a,b)
    """
    for index, bin in enumerate(bins):
        if bin[0] <= val and val < bin[1]:
            return index
    raise ValueError


def index_of_discrete_bin(bins, val):
    """Return bin index, using style-1 bins.

    Returns index of the bin string exists in value provided, 
    or -1 if not found.
    """
    for index, bin in enumerate(bins):
        if bin in val:
            return index
    return -1
