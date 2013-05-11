import time
from os import listdir
from os.path import isfile, join
from arff_writer import ArffWriter
from website import Website
from website_analyzer import analyze
from scanners import *

# Settings
website_dir = 'top_sites_all'

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

# Test
# scanners = [
#     content_news_scanner,
#     content_sport_scanner,
#     content_games_scanner,
#     content_technology_scanner,
#     content_xxx_scanner,
#     content_music_scanner,
#     content_shop_scanner,
#     content_transport_scanner,
#     content_food_scanner,
#     content_film_scanner,
#     content_health_scanner,
#     content_business_scanner
# ]

# Get all websites
start_time = time.time()

filenames = [join(website_dir,fn) for fn in listdir(website_dir) if isfile(join(website_dir,fn))]
#filenames = filenames[:50]
websites = []

print 'Files loaded: ', len(filenames)

load_time = time.time()

for i in range(len(filenames)):
    fn = filenames[i]
    with open(fn) as f:
        website = Website(f)
        websites.append(website)
    print 'Parsed (%i of %i): %s' % (i+1, len(filenames), website.url)

print 'Websites parsed'

parse_time = time.time()

# Scan attributes
attribute_rows = []
for i in range(len(websites)):
    website = websites[i]
    attributes = analyze(website, scanners)
    attribute_rows.append(attributes)
    print 'Analyzed (%i of %i): %s' % (i+1, len(websites), website.url)

print 'Websites analyzed'

analyze_time = time.time()

# Write to ARFF
writer = ArffWriter(attribute_rows, filename='dataset/data_binned.arff')
writer.write()

writer = ArffWriter(attribute_rows, filename='dataset/data_raw.arff', output_raw=True)
writer.write()

# Write stats
with open('dataset/stats.log', 'w') as f:
    time_to_load = 'Time, loading: %s' % str(load_time - start_time)
    time_to_parse = 'Time, parsing: %s' % str(parse_time - load_time)
    time_to_analyze = 'Time, analyzing: %s' % str(analyze_time - parse_time)
    time_total = 'Time, total: %s' % str(analyze_time - start_time)
    output = '%s\n%s\n%s\n%s' % (time_to_load, time_to_parse, time_to_analyze, time_total)
    print output
    f.write(output)
