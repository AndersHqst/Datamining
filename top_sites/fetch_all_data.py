from data_fetcher import DataFetcher

# Read list of URLs
sites = []
with open('top-dk.csv') as in_file:
    for line in in_file:
        sites.append('http://www.' + line.split(',')[1].strip())

# Fetch sites
fetcher = DataFetcher(sites)
fetcher.fetch(stop=10)
