from scanner_attribute import ScannerAttribute


def title_scanner(website):
    """Scan website for using the title meta-tag

    :param website: website to scan
    :return ScannerAttribute: """
    key = 'title_tag'
    title = website.soup.title

    if title is None or title.string is None or title.string.strip() == '':
        return ScannerAttribute(key, 0, 0, [0, 1])
    return ScannerAttribute(key, 1, 1, [0, 1])
