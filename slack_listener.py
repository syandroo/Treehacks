import time
import json
from slackclient import SlackClient  # https://github.com/slackhq/python-slackclient


# token found at https://api.slack.com/web#authentication


def connect_to_slack():
    access_token = str(raw_input("Enter your developer access token: "))
    sc = SlackClient(access_token)
    if sc.rtm_connect():
        response = sc.api_call('rtm.start')
        team_data = json.loads(response)
    else:
        print "connection failed! invalid token?"
    return team_data, sc


def get_channels(team_data):
    channels = team_data['channels']
    is_member_channels = [channel for channel in channels if channel['is_member']]
    for i, channel in enumerate(is_member_channels):
        name = channel['name']
        print i, name
    try:
        channel_number = int(raw_input("Enter channel number to summarize: "))
        channel = channels[channel_number]
    except ValueError:
        print("NaN! Try again!")
    return channel


def get_channel_id(channel):
    channel_id = channel['id']
    return channel_id


def get_channel_name(channel):
    channel_name = channel['name']
    return channel_name


def get_num_unread_messages(channel):
    num_unread_messages = channel['unread_count']
    return num_unread_messages


def get_unread_messages(team_data, slack_client):
    channel = get_channels(team_data)
    channel_id = get_channel_id(channel)
    channel_name = get_channel_name(channel)
    num_unread_messages = get_num_unread_messages(channel)
    message_data = {'channel_name': channel_name, 'num_unread_messages': num_unread_messages,
                    'messages': []}
    response = slack_client.api_call('channels.history', channel=channel_id)
    channel_data = json.loads(response)
    for message in channel_data['messages']:
        if message['type'] == 'message' and 'subtype' not in message:
            message_data['messages'].append(message['text'])
    return message_data







