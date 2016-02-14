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


def timestamps_l1(feat1, feat2):
    ''' difference in seconds between the two messages '''
    dist = np.abs(
            float(feat1['timestamp']) -
            float(feat2['timestamp'])
        )
    return dist


def mention(feat1, feat2):
    '''
    does message2 mentions the sender of message1?
    '''
    score = 0.
    for name in feat2['mentions']:
        if (name == feat1['sender']['nickname'] or
                name in feat1['mentions']):
            score += 1.
    dist = -score
    return dist


def combined(feat1, feat2):
    ''' hand-crafted combined feature '''
    weights = {
        mention: 3600.0, # one mention is a worth of 20 miniutes.
        timestamps_l1: 1.,
        keywords_l0: 3600.0
    }

    dist = 0.
    for (func, w) in weights.items():
        dist += w * func(feat1, feat2)

    return dist


def worth(feat):
    score = 0.
    score += sum([float(keyword['relevance']) for keyword in feat['keywords']])
    return score







