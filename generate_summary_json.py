#!/usr/bin/python
# coding: utf-8

import json

import groupme_listener
import slack_listener as slack


# 1000 is the max number of messages Slack will return
def generate_summary_json(member_id, channel_id, channel_name, num_messages=1000, access_token=None):
    # get GroupMe message stream
    # group_data, access_token = groupme_listener.intiate_groupme_interaction()
    # messages_info, messages_text_only = groupme_listener.process_group_data(group_data, access_token)

    # get Slack channel message stream
    sc = slack.connect_to_slack(access_token)
    user_id_to_name_map = slack.map_user_id_to_names(sc)
    messages = slack.get_messages(user_id_to_name_map, channel_id, channel_name, sc, num_messages)
    messages_data = json.dumps(messages)
    return messages_data


    # bot to send summary to the channel
    summary = 'hi there!'
    slack.send_message(summary, messages_data['channel_id'], sc)