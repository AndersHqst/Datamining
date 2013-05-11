
def analyze(website, scanners):
    attributes = {}
    for scanner in scanners:
        attribute = scanner(website)
        attributes[attribute.key] = attribute
    return attributes
