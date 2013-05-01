import sys

def index_of_interval_bin(bins, val):
    """
    Returns index of the bin that the values should be binned to.
    Values are binned in range: [a,b)
    TODO optimize this to do binary search, could not make it work with binsect.
    """
    for index, bin in enumerate(bins):
        if bin[0] <= val and val < bin[1]:
            return index
    raise ValueError