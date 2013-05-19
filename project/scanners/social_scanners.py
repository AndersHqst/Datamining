from scanner_attribute import ScannerAttribute


def twitter_share_scanner(website):
    """Scan website for displaying a Twitter share

    :param website: website to scan
    :return ScannerAttribute:
    """
    key = 'twitter_share'
    tw_classes = [
        'twitter-share-button',
        'twitter-follow-button',
        'twitter-hashtag-button',
        'twitter-mention-button'
    ]
    for tw_class in tw_classes:
        if len(website.soup.find_all('a', {'class': tw_class})) > 0:
            return ScannerAttribute(key, 1, 1, [0, 1])
    return ScannerAttribute(key, 0, 0, [0, 1])


def facebook_share_scanner(website):
    """Scan website for displaying a Facebook share

    :param website: website to scan
    :return ScannerAttribute:
    """
    key = 'facebook_share'
    fb_classes = [
        'fb-like', 'fb-send',
        'fb-follow',
        'fb-comments',
        'fb-activity',
        'fb-recommendations',
        'fb-recommendations-bar',
        'fb-facepile',
        'fb-like-box',
        'fb-login-button'
    ]
    for fb_class in fb_classes:
        if len(website.soup.find_all('div', {'class': fb_class})) > 0:
            return ScannerAttribute(key, 1, 1, [0, 1])
    return ScannerAttribute(key, 0, 0, [0, 1])
