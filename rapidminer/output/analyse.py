from math import sqrt
from collections import Counter
import numpy as np
from scipy.stats import mode

def split_csvline(line):
    return [attribute.replace('"', '').replace('\n', '') for attribute in line.split(';')]


def analyze(in_filename, out_filename):
    with open(in_filename, 'r') as f:
        csvlines = f.readlines()

    clusters = {}

    headerline = csvlines[0]
    headers = split_csvline(headerline)

    for line in csvlines[1:]:
        attributes = split_csvline(line)
        cluster_key = attributes[-1]
        #print cluster_key

        if not clusters.has_key(cluster_key):
            clusters[cluster_key] = {}
            cluster = clusters[cluster_key]
            for i in range(len(attributes[:-1])):
                header = headers[i]
                cluster[header] = []

        cluster = clusters[cluster_key]

        for i in range(len(attributes[:-1])):
            header = headers[i]
            attribute = attributes[i]

            try:
                cluster[header].append(int(attribute))
            except Exception:
                cluster[header].append(float(attribute))

    attribute_keys = sorted(headers[:-1])
    output = ''
    for cluster_key in sorted(clusters.keys()):
        output += cluster_key + '\n'
        output += ';'.join(attribute_keys) + '\n'

        cluster = clusters[cluster_key]

        sums = []
        means = []
        modes = []
        stddevs = []
        for attribute_key in attribute_keys:
            attribute_list = np.array(cluster[attribute_key])

            mn = np.average(attribute_list)
            mo = mode(attribute_list)[0]
            sd = np.std(attribute_list)

            sums.append(str(su))
            means.append(str(mn))
            modes.append(str(mo))
            stddevs.append(str(sd))

        output += ';'.join(sums) + '\n'
        output += ';'.join(means) + '\n'
        output += ';'.join(modes) + '\n'
        output += ';'.join(stddevs) + '\n'

    with open(out_filename, 'w') as f:
        f.write(output)
    print 'Output written to: %s' % out_filename

analyze('kmeans_cluster_data.csv', 'kmeans_cluster_data_analysis.csv')
analyze('kmedoids_cluster_data.csv', 'kmedoids_cluster_data_analysis.csv')
analyze('dbscan_cluster_data.csv', 'dbscan_cluster_data_analysis.csv')