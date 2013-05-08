import sys
from utils.bin_helper import bin_numeric, bin_numeric_desc, bin_fuzzy_text

def alexa_rank_scanner(website):
    # Mapping:
    # 0 - 99: 0
    # 100 - 499: 1
    # ...
    bins = [1000, 5000, 10000, 25000, 50000, 100000, 250000, sys.maxsize]
    rank = website.alexa_rank
    return 'alexa_rank', bin_numeric(bins, rank)

def alexa_rank_dk_scanner(website):
    bins = [10, 50, 250, 1000, 5000, sys.maxsize]
    rank = website.alexa_rank_dk
    return 'alexa_rank_dk', bin_numeric(bins, rank)

def alexa_load_time_scanner(website):
    bins = [500, 1000, 1500, 2000, 2500, sys.maxsize]
    load_time = website.alexa_load_time
    return 'alexa_load_time', bin_numeric(bins, load_time)

def alexa_links_ins_scanner(website):
    # Mapping:
    # 10001 - inf: 0
    # 7501 - 10000: 1
    # ...
    bins = [10000, 7500, 5000, 2500, 1000, 500, 0]
    load_time = website.alexa_load_time
    return 'alexa_links_ins', bin_numeric_desc(bins, load_time)

def alexa_lang_scanner(website):
    bins = ['dk', 'en', 'sv', 'no', 'de', 'fr']
    lang = website.alexa_lang
    return 'alexa_lang', bin_fuzzy_text(bins, lang)