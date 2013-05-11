from os import listdir
from os.path import isfile, join
from arff_writer import ArffWriter
from website import Website
from website_analyzer import analyze
from scanners import *

# Settings
website_dir = 'top_sites'

scanners = [
    url_scanner,
    image_count_scanner,
    external_links_scanner,
    internal_links_scanner,
    title_scanner,
    cms_scanner,
    description_scanner,
    keyword_scanner,
    alexa_rank_scanner,
    alexa_rank_dk_scanner,
    alexa_load_time_scanner,
    alexa_links_ins_scanner,
    alexa_lang_scanner,
    server_scanner,
    analytics_scanner,
    image_count_scanner,
    external_links_scanner,
    internal_links_scanner,
    title_scanner,
    cms_scanner,
    description_scanner,
    keyword_scanner,
    alexa_rank_scanner,
    alexa_rank_dk_scanner,
    alexa_load_time_scanner,
    alexa_links_ins_scanner,
    alexa_lang_scanner,
    html5_scanner,
    html5_tag_scanner,
    xhtml_scanner,
    twitter_share_scanner,
    facebook_share_scanner
]

# Get all websites
files_names = [join(website_dir,fn) for fn in listdir(website_dir) if isfile(join(website_dir,fn))]
websites = []

print 'Files loaded: ', len(files_names)

for fn in files_names[:25]:
    with open(fn) as f:
        website = Website(f)
        websites.append(website)
        print 'Parsed: %s' % website.url

print 'Websites parsed'

# Scan attributes
attribute_rows = []
for website in websites:
    attributes = analyze(website, scanners)
    attribute_rows.append(attributes)
    print 'Analyzed: %s' % website.url

# Write to ARFF
writer = ArffWriter(attribute_rows, filename='data_binned.arff')
writer.write()

writer = ArffWriter(attribute_rows, filename='data_raw.arff', output_raw=True)
writer.write()
