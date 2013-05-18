
def bin_numeric(bins, value):
    if value < 0:
        return -1

    for i in range(len(bins)):
        if value < bins[i]:
            return i


def bin_numeric_desc(bins, value):
    if value < 0:
        return -1

    for i in range(len(bins)):
        if value > bins[i]:
            return i


def bin_fuzzy_text(bins, value):
    for i in range(len(bins)):
        if value in bins[i]:
            return i

    return -1
