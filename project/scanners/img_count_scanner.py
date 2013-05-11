import sys
from utils.preprocessing_helper import index_of_interval_bin
from scanner_attribute import ScannerAttribute

def image_count_scanner(website):
    count = len(website.soup.find_all('img'))
    bins = [(0, 5), (5, 10), (10, 15), (15, 20), (20, sys.maxsize)]
    return ScannerAttribute('img_count', count, index_of_interval_bin(bins, count), bins)