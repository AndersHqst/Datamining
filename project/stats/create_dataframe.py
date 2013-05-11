import pandas
from pandas import DataFrame
import numpy as np

def create_dataframe(file_descriptior):
    """Creates and returns a pandas data frame from a Weka arff file"""
    attributes = []
    is_data = False
    data = {}
    URL_INDEX = 18
    for line in file_descriptior.readlines():

        if is_data:
            row = line.rstrip().rstrip(',').split(',')
            url = row.pop(len(row)-2)
            pairs = zip(attributes, row)
            data[url] = {}
            for attr, val in pairs:
                try:
                    converted = int(val)
                except Exception:
                    converted = val
                data[url][attr] = converted

        #Parse attribute, ignore url which is used for index
        if line.startswith("@ATTRIBUTE"):
            chunks = line.split(' ')
            attr = chunks[1]
            if not 'url' in attr.lower():
                attributes.append(attr)

        elif line.startswith("@DATA"):
            is_data = True

    #replace missing values with np.nan
    frame = DataFrame(data)
    frame[frame == '?'] = np.nan
    return frame.T

def default_frame():
    fd = open('../data_raw.arff', 'r')
    frame = create_dataframe(fd)
    fd.close()
    return frame