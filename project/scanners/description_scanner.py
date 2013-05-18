from scanner_attribute import ScannerAttribute

"""A website is considered to have a description, if the tag is present, and it contains text."""


def bins():
    return [0, 1]


def description_scanner(website):
    has_description = False
    meta_tags = website.soup.find_all('meta')
    for meta_tag in meta_tags:
        if meta_tag.has_key('name') and meta_tag.has_key('content'):
            # Keys exist, get the values
            name = meta_tag['name']
            content = meta_tag['content']
            if 'description' in name.lower():
                has_description = 0 < len(content)
        if has_description:
            break

    return ScannerAttribute('has_description', int(has_description), int(has_description), [0, 1])
