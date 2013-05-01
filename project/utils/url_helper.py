

def strip_web_prefix(url):
    "Strip website url for web prefixes"
    if url.startswith('http://'):
        url = url[7:]
    if url.startswith('www.'):
        url = url[4:]
    return url