import re
import os

def generate_table(serie, col_text, title, caption):
    """Build a two column latex table

    :param serie: mx1 pandas serie with column values to be inserted
    :param col_text: header text for column
    :param title: table title
    :param caption: table caption
    """

    max_site_name_length = 27

    table = "\\hhtab{p{130pt}p{50pt}}\n"
    table += "{\n"
    table += "\\toprule\n"
    table += "Site & " + col_text + "\\\\\n"
    table += "\\midrule\n"

    for index, val in enumerate(serie):
        site = serie.index[index].strip('http://www.')
        if max_site_name_length < len(site):
            chunks = list(site)
            site = ''.join(chunks[:max_site_name_length]) + '...'
        table += '%s & %s' % (site, val) + "\\\\\n"
    table += "\\bottomrule\n"
    table += "}{" + caption + "}{tab:" + title + "}"
    print "table string: ", table

    #file name
    file_name = title.lower().replace(' ', '_')
    # Remove bad characters
    file_name = "".join([c for c in file_name if re.match(r'\w', c)])
    fd = open("./tables/" + file_name + ".tex", 'w+')
    fd.write(table)
    fd.close()

    return table

def generate_tables(frame):
    # Alexa Rank - low value mean top ranks
    f = frame.alexa_rank[frame.alexa_rank.notnull()]
    f.sort()
    top10 = f[:10]
    bot10 = f[-10:]
    # generate_table(bot10[-5:], "Rank", "Alexa Rank bottom 5", "Bottom 5 Danish sites on the Alexa Rank")
    generate_table(bot10, "Rank", "Alexa Rank bottom 10", "Bottom 10 Danish sites on the Alexa Rank")
    # generate_table(top10[:5], "Rank", "Alexa Rank Top 5", "Top 5 Danish sites on the Alexa Rank")
    generate_table(top10, "Rank", "Alexa Rank Top 10", "Top 10 Danish sites on the Alexa Rank")

    # Alexa Rank Dk
    f = frame.alexa_rank_dk[frame.alexa_rank_dk.notnull()]
    f.sort()
    top10 = f[:10]
    bot10 = f[-10:]
    # generate_table(bot10[-5:], "Rank", "Alexa Rank DK bottom 5", "Bottom 5 Danish sites on the Alexa Rank")
    generate_table(bot10, "Rank", "Alexa Rank DK bottom 10", "Bottom 10 Danish sites on the Alexa Rank DK")
    # generate_table(top10[:5], "Rank", "Alexa Rank DK Top 10", "Top 10 Danish sites on the Alexa Rank")
    generate_table(top10, "Rank", "Alexa Rank DK Top 10", "Top 10 Danish sites on the Alexa Rank DK")

    # Alexa links in - back-links
    f = frame.alexa_links_in[frame.alexa_links_in.notnull()]
    f.sort()
    f = f[::-1] #reverse
    top10 = f[:10]
    generate_table(top10, "Links", "Alexa Links In - back-links", "Danish sites with most back-links according to Alexa. Back-links are often considered important for good page rank")
    # generate_table(top10[-5:], "HTML 5 Tags", "HTML 5 Tags Top 5", "Sites with most HTML 5 Tags.")

    # Alexa site load time
    f = frame.alexa_load_time[frame.alexa_load_time.notnull()]
    f.sort()
    top10 = f[:10]
    bot10 = f[-10:]
    # generate_table(bot10[-5:], "Time (ms)", "Alexa Load Time bottom 5", "Sites with the slowest load time on Alexa")
    generate_table(bot10, "Time (ms)", "Alexa Load Time bottom 10", "Sites with the slowest load time on Alexa")
    # generate_table(top10[:5], "Time (ms)", "Alexa Load Time Top 5", "Sites with the fastest load time on Alexa")
    generate_table(top10, "Time (ms)", "Alexa Load Time Top 10", "Sites with the fastest load time on Alexa")

    # Google Page Rank
    f = frame.page_rank[frame.page_rank.notnull()]
    f.sort()
    f = f[::-1] #reverse
    top10 = f[:10]
    bot10 = f[-10:]
    # generate_table(bot10[:5], "Rank", "Google Page Rank top 5", "Bottom 5 Danish sites on the Google Page Rank")
    generate_table(bot10, "Rank", "Google Page Rank bottom 10", "Bottom 10 Danish sites on the Google Page Rank")
    # generate_table(top10[-5:], "Rank", "Google Page Rank Top 10", "Top 10 Danish sites on the Google Page Rank")
    generate_table(top10, "Rank", "Google Page Rank Top 10", "Top 10 Danish sites on the Google Page Rank")

    # Internal links count - page linking to itself, low ranks are many zeros and ones, so not included
    f = frame.internal_links_count[frame.internal_links_count.notnull()]
    f.sort()
    f = f[::-1] #reverse
    top10 = f[:10]
    generate_table(top10, "Links", "Internal Links Count Top 10", "Sites with most internal links, ie links on the site pointing to itself")
    # generate_table(top10[-5:], "Links", "Internal Links Count Top 5", "Sites with most internal links, ie links on the site pointing to itself")

    # External links count - page linking to other pages, low ranks are many zeros and ones, so not included
    f = frame.external_links_count[frame.external_links_count.notnull()]
    f.sort()
    f = f[::-1] #reverse
    top10 = f[:10]
    generate_table(top10, "Links", "External Links Count Top 10", "Sites with most external links, ie links on the site pointing to another site")
    # generate_table(top10[-5:], "Links", "External Links Count Top 5", "Sites with most external links, ie links on the site pointing to another site")

    # External links count
    f = frame.img_count[frame.img_count.notnull()]
    f.sort()
    f = f[::-1] #reverse
    top10 = f[:10]
    generate_table(top10, "Images", "Image Count Top 10", "Sites with most images.")
    # generate_table(top10[-5:], "Images", "Image Count Top 5", "Sites with most images.")

    # HTML5 tags
    f = frame.html5_tags[frame.html5_tags.notnull()]
    f.sort()
    f = f[::-1] #reverse
    top10 = f[:10]
    generate_table(top10, "Tags", "HTML 5 Tags Top 10", "Sites with most HTML 5 Tags.")
    # generate_table(top10[-5:], "HTML 5 Tags", "HTML 5 Tags Top 5", "Sites with most HTML 5 Tags.")

    #Writes all tables to a .tex appendix file
    files = os.listdir('./tables/')
    tex_file = open('tables_appendix.tex', 'w')
    tex_file.truncate()
    for fn in files:
        path = './tables/' + fn
        fd = open(path)
        tex_file.write(fd.read() + '\n\n')
        fd.close()
        os.remove(path)
    tex_file.close()






