import time
from collections import namedtuple
from os import listdir
from os.path import isfile, join
from arff_writer import ArffWriter
from website import Website
from website_analyzer import analyze
from scanners import *

"""A script which creates the actual dataset.


"""

# Settings
website_dir = 'top_sites_all'

# A list of the used scanners
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
    facebook_share_scanner,
    page_rank_scanner,
    alexa_has_adult_content,
    jquery_scanner,
    prototype_scanner,
    dojo_scanner,
    mootools_scanner,
    modernizr_scanner,
    underscore_scanner,
    handlebars_scanner,
    knockout_scanner,
    ember_scanner,
    angular_scanner,
    backbone_scanner,
    content_news_scanner,
    content_sport_scanner,
    content_games_scanner,
    content_technology_scanner,
    content_xxx_scanner,
    content_music_scanner,
    content_shop_scanner,
    content_transport_scanner,
    content_food_scanner,
    content_film_scanner,
    content_health_scanner,
    content_business_scanner
]

# Get all websites

start_time = time.time() # We time how long it takes to generate the dataset.

# Get a list of all the input data files
filenames = [join(website_dir, fn)
             for fn in listdir(website_dir) if isfile(join(website_dir, fn))]
websites = []

print 'Files loaded: ', len(filenames)

load_time = time.time()

# Parse the data files into Website objects
for i in range(len(filenames)):
    fn = filenames[i]
    with open(fn) as f:
        website = Website(f)
        websites.append(website)
    print 'Parsed (%i of %i): %s' % (i + 1, len(filenames), website.url)

print 'Websites parsed'

parse_time = time.time()

# Use scanners to find all attributes for each website
attribute_rows = []
for i in range(len(websites)):
    website = websites[i]
    attributes = analyze(website, scanners)
    attribute_rows.append(attributes)
    print 'Analyzed (%i of %i): %s' % (i + 1, len(websites), website.url)

print 'Websites analyzed'

analyze_time = time.time()

# Write to ARFF

# Create a binned version of the dataset
writer = ArffWriter(attribute_rows, filename='dataset/data_binned.arff')
writer.write()

# Create a raw version of the dataset
writer = ArffWriter(
    attribute_rows, filename='dataset/data_raw.arff', output_raw=True)
writer.write()

# Create a mixed version of the dataset
Info = namedtuple('Info', ['type', 'use_binned', 'exclude'])
attribute_info = {
    'alexa_has_adult_content': Info('nominal', True, False),
    'alexa_lang': Info('nominal', True, False),
    'alexa_links_in': Info('numeric', False, False),
    'alexa_load_time': Info('numeric', False, False),
    'alexa_rank': Info('numeric', False, False),
    'alexa_rank_dk': Info('numeric', False, False),
    'cms': Info('nominal', True, False),
    'external_links_count': Info('numeric', False, False),
    'facebook_share': Info('nominal', True, False),
    'has_analytics': Info('nominal', True, False),
    'has_content_business': Info('nominal', True, False),
    'has_content_film': Info('nominal', True, False),
    'has_content_food': Info('nominal', True, False),
    'has_content_games': Info('nominal', True, False),
    'has_content_health': Info('nominal', True, False),
    'has_content_music': Info('nominal', True, False),
    'has_content_news': Info('nominal', True, False),
    'has_content_shop': Info('nominal', True, False),
    'has_content_sport': Info('nominal', True, False),
    'has_content_technology': Info('nominal', True, False),
    'has_content_transport': Info('nominal', True, False),
    'has_content_xxx': Info('nominal', True, False),
    'has_description': Info('nominal', True, False),
    'has_js_angular': Info('nominal', True, False),
    'has_js_backbone': Info('nominal', True, False),
    'has_js_dojo': Info('nominal', True, False),
    'has_js_ember': Info('nominal', True, False),
    'has_js_handlebars': Info('nominal', True, False),
    'has_js_jquery': Info('nominal', True, False),
    'has_js_knockout': Info('nominal', True, False),
    'has_js_modernizr': Info('nominal', True, False),
    'has_js_mootools': Info('nominal', True, False),
    'has_js_prototype': Info('nominal', True, False),
    'has_js_underscore': Info('nominal', True, False),
    'has_keywords': Info('nominal', True, False),
    'html5': Info('nominal', True, False),
    'html5_tags': Info('numeric', False, False),
    'img_count': Info('numeric', False, False),
    'internal_links_count': Info('numeric', False, False),
    'page_rank': Info('numeric', False, False),
    'server': Info('nominal', True, False),
    'title_tag': Info('nominal', True, False),
    'twitter_share': Info('nominal', True, False),
    'url': Info('string', True, True),
    'xhtml': Info('nominal', True, False)
}

writer = ArffWriter(
    attribute_rows, attribute_info=attribute_info, filename='dataset/data_mixed.arff')
writer.write()

# Write stats
with open('dataset/stats.log', 'w') as f:
    time_to_load = 'Time, loading: %s' % str(load_time - start_time)
    time_to_parse = 'Time, parsing: %s' % str(parse_time - load_time)
    time_to_analyze = 'Time, analyzing: %s' % str(analyze_time - parse_time)
    time_total = 'Time, total: %s' % str(analyze_time - start_time)
    output = '%s\n%s\n%s\n%s' % (
        time_to_load, time_to_parse, time_to_analyze, time_total)
    print output
    f.write(output)
