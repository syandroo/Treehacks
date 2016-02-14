import time
import json
from slackclient import SlackClient  # https://github.com/slackhq/python-slackclient


# token found at https://api.slack.com/web#authentication

channel_number = 55; #default

def connect_to_slack():
    access_token = "xoxb-21293612517-YlKw0nxVwtjXjUwvN0IrzI0Y"
    sc = SlackClient(access_token)
    if sc.rtm_connect():
        response = sc.api_call('rtm.start')
        team_data = json.loads(response)
        return team_data, sc
    else:
        raise RuntimeError("connection failed! invalid token?")


def map_user_id_to_names(slack_client):
    response = slack_client.api_call('users.list')
    member_data = json.loads(response)
    if member_data['ok']:
        all_members = {}
        members = member_data.get('members')
        for member in members:
            if not member.get('is_bot'):
                member_id = member.get('id')
                try:
                    full_name = member['profile']['real_name']
                    first_name = member['profile']['first_name']
                    nickname = member['name']
                except KeyError:  # some users have no name information
                    email_name = member['profile']['email'].split('@')[0]  # best we can do, get email address
                    full_name, first_name, nickname = email_name, email_name, email_name
                all_members[member_id] = {'full_name': full_name, 'first_name': first_name,
                                          'nickname': nickname}
    else:
        raise RuntimeError("bad connection to slack api! tried to hit users.list")
    return all_members

'''
change this so it can react to echo's command
This probably needs to be changed
'''


def get_channels(team_data):
    channels = team_data['channels']
    for i, channel in enumerate(channels):
        name = channel['name']
        print i, name
    try:
        #channel_number = int(raw_input("Enter channel number to summarize: "))
        channel_number = give_channel()
        # place holder
        channel = channels[channel_number]
    except ValueError:
        print("NaN! Try again!")
    return channel

def set_channel(user_set_channel_number):
    channel_number = user_set_channel_number

def give_channel():
    return channel_number;

def get_messages(team_data, user_id_to_name_map, slack_client, unread=False, limit=-1):
    channel = get_channels(team_data)
    channel_id = channel['id']
    channel_name = channel['name']
    messages_data = {'channel_name': channel_name, 'messages': []}
    response = slack_client.api_call('channels.history', channel=channel_id)
    channel_data = json.loads(response)
    if channel_data['ok']:
        for message in channel_data['messages']:
            if message['type'] == 'message' and 'subtype' not in message:
                text = message['text'] + '.'
                sender = user_id_to_name_map[message['user']]
                timestamp = message['ts']
                emojis = []
                try:
                    emojis = [{'name': name, 'count': count} for reaction in message['reactions']]
                except: KeyError  # no emojis in the message
                message_data = {'text': text, 'emojis': emojis, 'sender': sender, 'timestamp': timestamp}
                messages_data['messages'].append(message_data)
        return messages_data
    else:
        raise RuntimeError('bad connection to slack api! tried to hit channels.history')

