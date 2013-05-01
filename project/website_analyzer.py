
def analyze(website, scanners):
	attributes = {}
	for scanner in scanners:
		attribute_name, attribute_value = scanner(website)
		attributes[attribute_name] = attribute_value
	return attributes
