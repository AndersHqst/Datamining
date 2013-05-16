import math

# Scripts as layout for testing the coefficients that come from RapidMiner

# - 0.016 * has_description = 0
# + 0.016 * has_description = 1
# + 0.025 * has_keywords = 0
# - 0.025 * has_keywords = 1
# + 0.056 * title_tag = 1
# - 0.056 * title_tag = 0
# + 0.221 * alexa_links_in
# - 0.217 * alexa_rank
# + 0.019 * alexa_rank_dk
# + 0.149 * external_links_count
# - 0.011 * img_count
# - 0.040 * internal_links_count
# - 0.041

def pred(serie):
    page_rank = 0
    if serie['has_description'] == 1:
        page_rank += 0.016 * 1
    if serie['has_keywords'] == 1:
        page_rank += -0.025 * 1
    if serie['title_tag'] == 1:
        page_rank += 0.056 * 1
    page_rank += 0.221 * serie['alexa_links_in']
    page_rank += -0.217 * serie['alexa_rank']
    page_rank += 0.019 * serie['alexa_rank_dk']
    page_rank += 0.149 * serie['external_links_count']
    page_rank += -0.011 * serie['img_count']
    page_rank += -0.040 * serie['internal_links_count']
    return page_rank - 0.041

def eval(frame):
    frame.fillna(frame.mean(), inplace=True)
    squared_error = 0
    error = 0
    for index in frame.index:
        p = pred(frame.ix[index])
        # print 'fram page rank: ', frame.ix[index]['page_rank']
        err = (p - frame.ix[index]['page_rank']) ** 2
        squared_error  += err
        error += math.sqrt(err)
    entries = float(len(frame))
    return squared_error / entries, error / entries



