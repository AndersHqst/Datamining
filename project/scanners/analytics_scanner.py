from scanner_attribute import ScannerAttribute
"""True is a website using google analytics"""


def bins():
    return [0, 1]


def analytics_scanner(website):
    """Checks whether or not website uses Google Analytics"""
    has_analytics = False
    scripts = website.soup.find_all('script')
    for script in scripts:
        if 'google-analytics.com/ga.js' in script.get_text(): # We simply look for the ga.js file
            has_analytics = True
            break
    return ScannerAttribute('has_analytics', int(has_analytics), int(has_analytics), [0, 1])
