import sys
from utils.bin_helper import bin_numeric
from scanner_attribute import ScannerAttribute


def page_rank_scanner(website):
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, sys.maxsize]
    rank = website.google_page_rank
    return ScannerAttribute('page_rank', rank, bin_numeric(bins, rank), bins)
