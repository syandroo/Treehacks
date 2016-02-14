# some features for independent sentences and sentence segmentation.
from alchemyapi import AlchemyAPI
from os import path
import shelve
import hashlib
import codecs

alchemyapi = AlchemyAPI()

CACHE_DIR = 'cache'

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
    print 'text', text
    # request feature extraction.
    text_hash = hashlib.sha256(text.encode('ascii', 'ignore')).hexdigest()
    print 'text_hash', text_hash
    cache_db = shelve.open(path.join(CACHE_DIR, 'feature'))
    if not cache_db.has_key(text_hash):
        print 'new call'
        call = alchemyapi.combined('text', text)
        cache_db[text_hash] = call
    else:
        print 'cached call'
        call = cache_db[text_hash]
    cache_db.close()
    # filter results.
    whitelist = ['concepts', 'entities', 'keywords', 'taxonomy']
    for key in whitelist:
        if key not in call:
            continue
        resp[key] = call[key]
    return resp





