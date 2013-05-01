def analyze_website(website, scanners):
	attributes = {}
	for scanner in scanners:
		attribute_name, attribute_value = scanner(self.website)
		attributes[attribute_name] = attribute_value
	return attributes

# Sample scanner
def utf8_scanner(website):
	return "utf8", True

# Sample

scanners = [utf8_scanner]
websites = []
for website in websites:
	analyzer = WebsiteAnalyzer(websites, scanners)
	attributes = analyzer.analyze()

	# Put keys/values in DB

