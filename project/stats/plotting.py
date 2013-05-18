import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from matplotlib.pyplot import savefig
import matplotlib.gridspec as gridspec
import scipy.stats
import create_dataframe
import re


def cms_barh(plt, frame):
    cms_frame = frame['cms'].value_counts()
    cms_frame.plt(kind='barh', title='CMS distribution')


def numeric_attribute_histogram(plt, frame, title, num=10, interquartile=False, 
        mmm=True, binary=False):
    """Plot a histogram of an attribute in a DataFrame
        Expects matplotlib.rc('text', usetex=True) in interactive environment

    :param plt: plot
    :param frame: pandas DataFrame
    :param title: title on plot and file name
    :param num: num for linspace, will be number of bins in histogram
    :param interquartile: plot interquartile
    :param mmm: plot text with min, max, mean
    :param binary: mmm and interquartile cannot be True, and num is 2, 
        histogram bars have a legend is added
    """
    # Assert values for binary - an exception might be better
    if binary:
        num = 2
        interquartile = False
        mmm = False
    print "Create plot: %s num=%d interquartile=%s mmm=%s binary=%s" 
        % (title, num, interquartile, mmm, binary)

    plt.close()
              # Not sure if this is clever, but easier unless we plot more
              # things on top of eachother
    fig = plt.figure(1, figsize=(8, 6))

    # image file name, and plot title are similar
    file_name = title.lower().replace(' ', '_')
    # Remove bad characters
    file_name = "".join([c for c in file_name if re.match(r'\w', c)])

    # Remove missing values
    clean_frame = frame[frame.notnull()]
    clean_frame = np.sort(clean_frame)
    missing_values = len(frame) - len(
        clean_frame)  # Added as new line under title
    vals = clean_frame.values

    if not binary:
        # interquartile values
        if interquartile:
            q1 = len(vals) / 4
            q3 = len(vals) - len(vals) / 4
            vals = vals[q1:q3]
            clean_frame = clean_frame[q1:q3]
            title += " - interquartile"
            file_name += "_interquartile"

        min_ = vals[0]
        max_ = vals[-1]
        print "mix=%d max=%d" % (min_, max_)

        # Create a gridspec with 2 rows and one column. GridSpec allows plot
        # resizing
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        ax1 = plt.subplot(gs[0])

        # axis
        ax1.set_ylabel('sites')
        # ax1.set_xlabel('data')

        bins = np.linspace(min_, max_, num=num)
        print "bins=%s" % bins
        ax1.set_xticks(bins)

        # General statistical figures
        mean = np.mean(vals)
        mode = scipy.stats.mode(vals)  # mode, and occurances
        median = vals[len(vals) / 2]

        # Build string
        text = "Stat: \n$min=" + str(
            min_) + "$\n" + "$max=" + str(max_) + "$\n"
        text += "$\mu=%.2f$\n" % mean
        text += "$mode=%d (%d)$\n" % (mode[0], mode[1])  # mode, and occurances
        text += "$median=%d$" % median

        # Plot
        fig.text(0.75, 0.75, text, bbox={
                 'facecolor': 'white', 'alpha': 1., 'pad': 8})
        ax1.hist(vals, bins=bins)

        # Build tables displaying top and bottom values
        bottom_ten_table = build_column_table(clean_frame[:5], "Bottom 5")
        # Top 10 is the end of the list - revesed to have the higheset at the
        # top
        top_ten_table = build_column_table(clean_frame[-5:][::-1], "Top 5")

        # Plot tables
        ax2 = plt.subplot(gs[1])
        ax2.text(0.5, 0., bottom_ten_table, size=10)
        ax2.text(0., 0., top_ten_table, size=10)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)

    else:  # Binary plot
        bins = [0, 1]
        # ax1.get_xaxis().set_visible(False)
        plt.ylabel('sites')
        plt.hist([[0] * sum(vals == 0), [1] * sum(
            vals == 1)], bins=bins, histtype='bar', color=['r', 'b'], label=['No', 'Yes'])
        plt.legend()

    # Add some final info
    title += "\nsites: " + str(len(vals))
    # If any data was removed, we report this on the plot
    if missing_values != 0:
        title += ", removed sites: " + str(missing_values)
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # Save to file
    savefig("./figures/" + file_name + ".png")


def build_column_table(frame, col_text):
    """Build a one colum latex table.

    :param frame: mx1 pandas dataframe with column values
    :param col_text: header text for column
    """
    max_site_name_length = 27
    table = '\\begin{tabular}{ p{140pt} | p{60pt} |} Site & %s\\\\' % col_text
    for index, val in enumerate(frame):
        site = frame.index[index].strip('http://www.')
        if max_site_name_length < len(site):
            chunks = list(site)
            site = ''.join(chunks[:max_site_name_length]) + '...'
        table += '\\hline %s & %s\\\\' % (site, val)
    table += '\\end{tabular}'
    print "table string: ", table
    return table


def discrete_attribute_plot(plt, serie, title, total_sites=0, left_space=0.3):
    """Plot bar histogram of discretized values

    :param plt: plot
    :param serie: pandas Series
    :param title: title for the plot
    :param total_sites: if sites have been removed, total sites can be displayed
    :param left_space: add space to the left of the plot for long names
    """
    plt.close()
    fig = plt.gcf()
    # image file name, and plot title are similar
    file_name = title.lower().replace(' ', '_')
    # Remove bad characters
    file_name = "".join([c for c in file_name if re.match(r'\w', c)])

    # Approximate adjustment
    plt.subplots_adjust(left=left_space)

    # Plot
    title += "\nSites %d" % serie.sum()
    if total_sites != 0:
        title += " out of: %d" % total_sites
    # fig.text(0.75, 0.75, text, bbox={'facecolor': 'white', 'alpha': 1.,
    # 'pad': 8})
    plt.title(title)
    serie.plot(kind='barh')
    savefig("./figures/" + file_name + "_discrete.png")


# For fast plotting test
def generate_page_rank(plt, frame):
    f = frame['page_rank']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)


def generate_plots(plt, frame):
    """Generic creation of all numeric and binary plots"""

    f = frame['external_links_count']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['alexa_links_in']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['alexa_load_time']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['alexa_rank']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['alexa_rank_dk']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Dk', 'DK'))
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Dk', 'DK'), interquartile=True)
    f = frame['external_links_count']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['img_count']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['internal_links_count']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['page_rank']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)
    f = frame['html5_tags']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    # Removed interquartile for html_5 tags - it is all 0
    # numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title(),
    # interquartile=True)
    f = frame['page_rank']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title())
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), interquartile=True)

    f = frame['alexa_has_adult_content']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['facebook_share']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_analytics']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_description']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_keywords']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['html5']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['title_tag']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['twitter_share']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)

    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['xhtml']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)

    f = frame['has_content_business']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_film']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_food']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_games']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_health']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_music']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_news']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_shop']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_sport']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_technology']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_transport']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_content_xxx']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title(), binary=True)
    f = frame['has_js_angular']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_backbone']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_dojo']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_ember']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_handlebars']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_jquery']
    numeric_attribute_histogram(plt, f, f.name.replace('_', ' ').title().replace(
        'Js', 'JS').replace('Jquery', 'JQuery'), binary=True)
    f = frame['has_js_knockout']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_modernizr']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_mootools']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_prototype']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
    f = frame['has_js_underscore']
    numeric_attribute_histogram(plt, f, f.name.replace(
        '_', ' ').title().replace('Js', 'JS'), binary=True)
