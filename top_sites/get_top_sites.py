import time
import urllib2

def store_site(name, contents):
    with open('top_sites/%s' % name, 'w') as f:
        f.write(contents)

def log_error(message):
    with open('errors.log', 'a') as f:
        f.write(message + '\n')

def fetch_site(url, rank):
    contents = '### URL: %s\n\n' % url
    contents += '### RANK: %s\n\n' % rank

    request = urllib2.Request(url)
    try:
        start_time = time.time()

        # Simulate browser
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        response = opener.open(request, timeout = 10)
        headers = '\n'.join(['%s: %s' % (h, response.headers.get(h)) for h in response.headers])
        page_contents = response.read()

        download_time = time.time() - start_time
    except Exception as e:
        page_contents = 'An error occured: %s' % e
        headers = page_contents
        download_time = 0
        log_error('Error in: #%s, %s' % (rank, url))
    
    contents += '### TIME: %.4f\n\n' % download_time
    contents += '### HEADERS: \n%s\n\n' % headers
    contents += '### HTML: \n%s\n\n' % page_contents
    return contents

def fetch_sites(top_sites, start, stop):
    for i in range(start, stop):
        url = top_sites[i]
        rank = str(i + 1)
        name = rank + '.dat'
        contents = fetch_site(url, rank)

        print 'Fetched (%s of %i): %s' % (rank, len(top_sites), url)

        store_site(name, contents)

num_top_sites = 10000
top_sites = []

# Select limited number of top sites
with open('top-1m.csv') as in_file:
    i = 0
    for line in in_file:
        if i == num_top_sites:
            break
        i += 1
        top_sites.append('http://www.' + line.split(',')[1].strip())

fetch_sites(top_sites, 0, num_top_sites)