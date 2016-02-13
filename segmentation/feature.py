# some features for independent sentences and sentence segmentation.
from alchemyapi import AlchemyAPI

alchemyapi = AlchemyAPI()


def get_sanitized(data):
    if 'sanitized' in data: # use sanitized data.
        text = data['sanitized']
    else:   # use text
        text = data['text']
    return text


def entities(data, call=None):
    ''' wrapper of alchemyapi's entities() '''
    resp = dict(data)
    text = get_sanitized(data)
    if not call:
        resp['entities'] = alchemyapi.entities('text', text)['entities']
    else:
        resp['entities'] = call['entities']
    return resp


def keywords(data, call=None):
    ''' wrapper of alchemyapi's keywords() '''
    resp = dict(data)
    text = get_sanitized(data)
    if not call:
        resp['keywords'] = alchemyapi.keywords('text', text)['keywords']
    else:
        resp['keywords'] = call['keywords']
    return resp


def taxonomy(data, call=None):
    ''' wrapper of alchemyapi's taxonomy() '''
    resp = dict(data)
    text = get_sanitized(data)
    if not call:
        resp['taxonomy'] = alchemyapi.taxonomy('text', text)['taxonomy']
    else:
        resp['taxonomy'] = call['taxonomy']
    return resp


def extract_all(data):
    resp = dict(data)
    text = get_sanitized(data)
    whitelist = ['concepts', 'entities', 'keywords', 'taxonomy']
    call = alchemyapi.combined('text', text)
    for key in whitelist:
        if key not in call:
            continue
        resp[key] = call[key]
    return resp





