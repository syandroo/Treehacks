# distance measure for a pair of messages.
import numpy as np

def keywords_l0(feat1, feat2):
    '''
    see how many keywords match between feature1 and feature2.
    the matches are weighted by relavance.
    '''
    score = 0.
    keywords_to_dict = lambda keywords: {item['text']: item
            for item in keywords}

    keywords1 = keywords_to_dict(feat1['keywords'])
    keywords2 = keywords_to_dict(feat2['keywords'])

    for keyword in keywords1:
        if keyword in keywords2:
            val1 = keywords1[keyword]
            val2 = keywords1[keyword]
            relevance1 = float(val1['relevance'])
            relevance2 = float(val2['relevance'])
            if val1['text'] == val2['text']:
                score += min(relevance1, relevance2)

    dist = -score
    return dist

