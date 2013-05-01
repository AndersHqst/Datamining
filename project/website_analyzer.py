
def analyze(website, scanners):
	attributes = {}
	for scanner in scanners:
		attribute_name, attribute_value = scanner(self.website)
		attributes[attribute_name] = attribute_value
	return attributes
