from scanner_attribute import ScannerAttribute
"""True is a website using google analytics"""


def bins():
    return [0, 1]


def analytics_scanner(website):
    has_analytics = False
    scripts = website.soup.find_all('script')
    for script in scripts:
        if 'google-analytics.com/ga.js' in script.get_text():
            has_analytics = True
            break
    return ScannerAttribute('has_analytics', int(has_analytics), int(has_analytics), [0, 1])
