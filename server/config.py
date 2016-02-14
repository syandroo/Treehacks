import simplejson as json

print '[server] loading config'
# with open('config.json', 'r') as f:
#     configuration = json.load(f)
#     SLACK_TOKEN = configuration['SLACK_TOKEN']

# import groupme_listener
import os

SLACK_TOKEN = os.environ.get('TEST_TEAM_SLACK_ACCESS_TOKEN')

CACHE_ROOT = 'cache/'

SERVER_PORT = 80
SERVER_ROOT = 'server'
print '[server] loading config [done]'
