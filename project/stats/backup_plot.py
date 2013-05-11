def numeric_attribute_histogram(plt, frame, title, num=10, interquantile=False, mmm=True, binary=False):
    """Plot a histogram of an attribute in a DataFrame

    :param plt: plot
    :param frame: pandas DataFrame
    :param title: title on plot and file name
    :param num: num for linspace, will be number of bins in histogram
    :param interquantile: plot interquantile
    :param mmm: plot text with min, max, mean
    :param binary: mmm cannot be True, and num is 2, histogram bars are a legend is added
    """

    plt.close() #Not sure if this is clever, but easier unless we plot more things on top of eachother
    fig = plt.figure(1)

    if interquantile:
        title += "\ninterquantile"
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.ylabel('sites')
    plt.xlabel('links')

    # Remove missing values
    clean_frame = frame[frame.notnull()]
    clean_frame = np.sort(clean_frame)
    missing_values = len(frame) - len(clean_frame)

    # If any data was removed, we report this on the plot
    if missing_values != 0:
        title += "\n" + str(missing_values) + " missing values"
    vals = clean_frame.values

    # Interquantile values
    if interquantile:
        vals = vals[len(vals) / 4: len(vals) - len(vals) / 4]
    min_ = vals[0]
    max_ = vals[-1]

    # There can be no other way..
    if binary:
        num = 2

    bins = np.linspace(min_, max_, num=num)
    plt.xticks(bins)

    if not binary:
        # Build tables displaying top and bottom values
        bottom_ten_table = build_column_table(clean_frame[:10], "Bottom 10")
        # Top 10 is the end of the list - revesed to have the higheset at the top
        top_ten_table = build_column_table(clean_frame[-10:][::-1], "Top 10")

        # Plot tables
        table_plot = fig.add_subplot(211)
        table_plot.text(0, 0, bottom_ten_table, size=12)
        table_plot.text(0.5, 0, top_ten_table, size=12)

        # General statistical figures
        mean = np.mean(vals)
        mode = scipy.stats.mode(vals) #mode, and occurances
        median = vals[len(vals) / 2]

        # Build string
        text = "Stat: \n$min=" + str(min_) + "$\n" + "$max=" + str(max_) + "$\n"
        text += "$\mu=%.2f$\n" % mean
        text += "$mode=%d (%d)$\n" % (mode[0], mode[1]) #mode, and occurances
        text += "$median=%d$" % median

        # Plot
        fig.text(0.75, 0.75, text, bbox={'facecolor':'white', 'alpha':1., 'pad':8})
        plt.hist(vals, bins=bins)

    else: # Binary plot
        plt.hist(vals, bins=bins, histtype='bar', color=['red', 'blue'], label=['No', 'Yes'])

    title = title.lower().replace(' ', '_').replace('\n', '_')
    savefig("./figures/" + title.lower().replace(' ', '_') + ".png")