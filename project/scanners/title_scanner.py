
def title_scanner(website):
    key = 'title_tag'
    title = website.soup.title

    if title is None or title.string.isspace():
        return key, 0
    return key, 1




