import simplejson as json

print '[server] loading config'
# with open('config.json', 'r') as f:
#     configuration = json.load(f)
#     SLACK_TOKEN = configuration['SLACK_TOKEN']

# import groupme_listener
import os

SLACK_TOKEN = os.environ.get('TREEHACKS_SLACK_ACCESS_TOKEN')

CACHE_ROOT = 'cache/'

SERVER_PORT = PORT = int(os.getenv('PORT', 8000))
SERVER_ROOT = 'server'
print '[server] loading config [done]'
