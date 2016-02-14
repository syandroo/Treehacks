import simplejson as json

print '[server] loading config'
with open('config.json', 'r') as f:
    configuration = json.load(f)
    SLACK_TOKEN = configuration['SLACK_TOKEN']


CACHE_ROOT = 'cache/'

SERVER_PORT = 8889
SERVER_ROOT = 'server'
print '[server] loading config [done]'
