import sys
from utils.bin_helper import bin_numeric
from scanner_attribute import ScannerAttribute


def page_rank_scanner(website):
    """Scan website for its PageRank.

    This number is actually set on the website object,
    and we add it to the proprocessing by providing a
    scanner

    :param website: website to scan
    :return ScannerAttribute:
    """
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, sys.maxsize]
    rank = website.google_page_rank
    return ScannerAttribute('page_rank', rank, bin_numeric(bins, rank), bins)
