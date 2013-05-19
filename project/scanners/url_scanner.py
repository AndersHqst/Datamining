from scanner_attribute import ScannerAttribute


def url_scanner(website):
    """Scan website for its url

    Trivial, but we want to use the website url as id,
    so it is scanned from the website as any other attribute.

    :param website: website to scan
    :return ScannerAttribute:
    """
    return ScannerAttribute('url', website.url)
