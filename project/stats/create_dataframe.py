import pandas
from pandas import DataFrame
import numpy as np
import re
import csv
from urlparse import urlparse


def valid(url):
    """Returns true if this is a valid url"""
    return 0 < len(urlparse(url)[1])


def url_index(row):
    """Return index of the url if any, and -2 otherwise to indicate 
    that we use labels and that we have tried to fin a url index
    """
    for index, data in enumerate(row):
        if 0 < len(urlparse(data)[1]) and 'www' in data or 'http' in data:
            return index

    # No url was found, so we use id
    return -2


def row_from_chunks(chunks):
    """Returns a list of row values. It expects a list of chunks crated 
    from splitting a file line with csv's, where commas in between 
    quotes have been chunked up. This method merges them back together.

    :param row: list of row chunks
    """
    # Some values migh have commas in then. In that case we re-concatenate
    # chunks between quotes
    merging = False
    merged_value = ''
    quote = None  # Record quote as '\'' and look for this as the end quote also.
    row = []
    for chunk in chunks:
        # Important that we are not already merging, i do not restart - this is
        # an edge case actually gives an error in our data..
        if chunk.startswith('\'') and not merging:
            merging = True
            quote = chunk[0]
            merged_value += chunk
        elif merging:
            merged_value += chunk
        else:
            row.append(chunk)

        # If the chunk ends with a quote, append the merged value to the row, and stop mergin
        # At this point, if merging is True, quote should not be None, if so, we would just like
        # things to blow up here
        if merging and chunk.endswith(quote):
                merging = False
                quote = None
                row.append(merged_value)
    return row


def create_dataframe(file_descriptior, binned=False):
    """Creates and returns a pandas data frame from a Weka arff file."""
    attributes = []
    is_data = False
    data = {}
    URL_INDEX = -1
    id_index = - \
        1  # If no urls in the data, we label the index with a ascending id
    for index, line in enumerate(file_descriptior.readlines()):

        if is_data:
            chunks = line.rstrip().rstrip(',').split(',')
            row = row_from_chunks(chunks)

            # url is not set
            if URL_INDEX == -1:
                URL_INDEX = url_index(row)

            if URL_INDEX == -2:
                url = index
            else:
                # Use url for indexing
                url = row.pop(URL_INDEX)

                # Clean url string and check that the url is valid
                if url.startswith('www'):
                    url = 'http://' + url
                    if not valid(url):
                        continue  # Effectively deletes the sample from the frame

            pairs = zip(attributes, row)
            data[url] = {}
            for attr, val in pairs:
                try:
                    converted = int(val)
                except Exception:
                    converted = val
                data[url][attr] = converted

        # Parse attribute, ignore url which is used for index
        if line.startswith("@ATTRIBUTE"):
            chunks = line.split(' ')
            attr = chunks[1]
            if not 'url' in attr.lower():
                attributes.append(attr)

        elif line.startswith("@DATA"):
            is_data = True

    # replace missing values with np.nan
    frame = DataFrame(data)
    if not binned:
        frame[frame == '?'] = np.nan
    return frame.T


def default_frame(arff_file='../dataset_03/data_raw.arff', binned=False):
    fd = open(arff_file, 'rb')
    frame = create_dataframe(fd, binned=binned)
    fd.close()
    return frame


def mixed_dataset():
    return default_frame('../dataset_03/data_mixed.arff', binned=True)


def binned_dataset():
    return default_frame('../dataset_03/data_binned.arff', binned=True)


def plot_value_counts(plt, serie, title):
    """Create vertical plot of discrete values and their corresponding count

    :param plt: plot
    :param serie: pandas Series
    :param title: title of the plot
    """
    plt.close()
    plt.figure(1)
    plt.grid(True)
    plt.title = title
    plt.yticks(np.arange(len(serie)), serie.index)
    plt.barh(np.arange(len(serie)), serie, align='center')
    plt.show()


def _bin(bins, x):
    if not isinstance(x, basestring):
        return "UNKNOWN"
    for bin in bins:
        if bin.lower() in x.lower():
            return bin.upper()
    return 'UNKNOWN'


def bin(serie, bins):
    """Bin a serie of string values to bin. A value in the serie is 
    set to a corresponding bin, if the value contains the bin 
    string - ignoring case. 

    Example: frame['binned_servers'] = bin(frame['server'], ['Apache', 'IIS'])

    :return a binned serie
    """
    return serie.apply(lambda x: _bin(bins, x))
