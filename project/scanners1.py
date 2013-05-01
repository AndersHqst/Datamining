def url_scanner(website):
    return 'url', "'%s'" % website.url

def alexa_rank_scanner(website):
    return 'alexa_rank', website.alexa_rank