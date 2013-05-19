
def analyze(website, scanners):
    """Utility function to retrieve attributes for a given website."""
    attributes = {}
    for scanner in scanners:
        attribute = scanner(website)
        attributes[attribute.key] = attribute
    return attributes
