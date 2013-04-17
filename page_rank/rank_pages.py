import pagerank
import numpy as np
import time

gpr = pagerank.GooglePageRank()
ranks = []

l = open('top_sites.csv')
l = l.readlines()
pages = l[0].split(',')

start = time.time()
for page in pages:
    url = 'http://' + page
    rank = gpr.get_rank(url)
    ranks.append(rank)
rank_time = (time.time() - start) / float(len(pages))
print 'Approx seconds to rank a page: %f' % rank_time

result = zip(pages, ranks)
s = ''.join("(%s, %s)\n" % tup for tup in result)

f = open('result.txt', 'w')
f.write(s)
f.close()
