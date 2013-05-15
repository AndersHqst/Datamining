from math import sqrt
from collections import Counter
import numpy as np
from scipy.stats import mode

def split_csvline(line):
    return [attribute.replace('"', '').replace('\n', '') for attribute in line.split(';')]


def analyze(filename):
    in_filename = filename + '.csv'
    summary_filename = filename + '_summary.csv'
    plottable_filename = filename + '_plottable.csv'

    with open(in_filename, 'r') as f:
        csvlines = f.readlines()

    clusters = {}

    headerline = csvlines[0]
    headers = split_csvline(headerline)

    for line in csvlines[1:]:
        attributes = split_csvline(line)
        cluster_key = attributes[-1]

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

    # Output cluster data summary
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

            su = np.sum(attribute_list)
            mn = np.average(attribute_list)
            mo = mode(attribute_list)[0][0]
            sd = np.std(attribute_list)

            sums.append(str(su))
            means.append(str(mn))
            modes.append(str(mo))
            stddevs.append(str(sd))

        output += ';'.join(sums) + '\n'
        output += ';'.join(means) + '\n'
        output += ';'.join(modes) + '\n'
        output += ';'.join(stddevs) + '\n'

    with open(summary_filename, 'w') as f:
        f.write(output)
    print 'Summary written to: %s' % summary_filename

    # Output cluster data as plottable
    output = ''
    
    for attribute_key in attribute_keys:
        output += attribute_key + ';;;;'
    output += '\n'

    for attribute_key in attribute_keys:
        output += 'sum;mean;mode;stddev;'
    output += '\n'

    for cluster_key in sorted(clusters.keys()):
        cluster = clusters[cluster_key]

        for attribute_key in attribute_keys:
            attribute_list = np.array(cluster[attribute_key])

            su = np.sum(attribute_list)
            mn = np.average(attribute_list)
            mo = mode(attribute_list)[0][0]
            sd = np.std(attribute_list)

            output += '%s;%s;%s;%s;'% (su, mn, mo, sd)
        output += '\n'

    with open(plottable_filename, 'w') as f:
        f.write(output)
    print 'Plottable data written to: %s' % plottable_filename


analyze('output/kmeans_cluster_data')
analyze('output/kmedoids_cluster_data')
analyze('output/dbscan_cluster_data')