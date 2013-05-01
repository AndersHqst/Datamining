from data_fetcher import DataFetcher


# Select limited number of top sites
sites = []
with open('top-dk.csv') as in_file:
    for line in in_file:
        sites.append('http://www.' + line.split(',')[1].strip())

fetcher = DataFetcher(sites)
fetcher.fetch(stop=10)