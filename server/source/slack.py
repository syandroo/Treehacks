from os import path
import sys
import time
import simplejson as json
from datetime import datetime
from multiprocessing import Process

import slack_listener as slack
from server.config import SLACK_TOKEN, CACHE_ROOT

CACHE_REFRESH = 60.0  # refresh every X seconds.

def sync(channel_number):
    slack_team_data, sc = slack.connect_to_slack(SLACK_TOKEN)
    user_id_to_name_map = slack.map_user_id_to_names(sc)
    messages_data = slack.get_messages(slack_team_data, user_id_to_name_map, sc, channel_number=channel_number)
    return messages_data


def sync_process(channel_number):
    old_stdout = sys.stdout
    #sys.stdout = open(path.join(CACHE_ROOT, "slack_listener.out"), "w")
    while True:
        message_data = sync(channel_number)
        with open(path.join(CACHE_ROOT, 'slack_%d' % channel_number), 'w') as f:
            json.dump(message_data, f)
        time.sleep(CACHE_REFRESH)
        print>>old_stdout, '[slack listener] sync finished %s' % datetime.now().isoformat()


def start_sync(channel_number):
    process = Process(target=sync_process, args=(channel_number,))
    process.start()


def get_messages(channel_number):
    with open(path.join(CACHE_ROOT, 'slack_%d' % channel_number), 'r') as f:
        messages_data = json.load(f)
    return messages_data

