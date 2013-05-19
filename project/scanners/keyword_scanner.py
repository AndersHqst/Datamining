from scanner_attribute import ScannerAttribute

"""A website is considered to have a keyword, if the tag is present, and it contains text."""


def bins():
    return [0, 1]


def keyword_scanner(website):
    """Scan website for using the keywords HTML meta tag

    :param website: website to scan
    :return ScannerAttribute:
    """
    has_keywords = False
    meta_tags = website.soup.find_all('meta')
    for meta_tag in meta_tags:
        if meta_tag.has_key('name') and meta_tag.has_key('content'):
            # Keys exist, get the values
            name = meta_tag['name']
            content = meta_tag['content']
            if 'keywords' in name.lower():
                has_keywords = 0 < len(content)
        if has_keywords:
            break
    return ScannerAttribute('has_keywords', int(has_keywords), int(has_keywords), [0, 1])
