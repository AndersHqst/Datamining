
def bin_numeric(bins, value):
    """Return bin index, using style-2 bins."""
    if value < 0:
        return -1
    for i in range(len(bins)):
        if value < bins[i]:
            return i


def bin_numeric_desc(bins, value):
    """Return bin index, using style-2 bins (descending)."""
    if value < 0:
        return -1
    for i in range(len(bins)):
        if value > bins[i]:
            return i


def bin_fuzzy_text(bins, value):
    """Return bin index for text bins.

    Return bin index by finding the first bin which 
    contains the value.
    """
    for i in range(len(bins)):
        if value in bins[i]:
            return i
    return -1
