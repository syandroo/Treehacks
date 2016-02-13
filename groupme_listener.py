#!/usr/bin/python
# coding: utf-8

import requests
import re

from text_processor import sanitize_text

def intiate_groupme_interaction(access_token):
    # returns a list of all the groups accessible with given access token
    response = requests.get('https://api.groupme.com/v3/groups?token='+access_token)
    data = response.json()
    if data['response'] == []:
        print("No accessible groups")
        return
    for i in xrange(len(data['response'])):
        group = data['response'][i]['name']
        print i, group
    try:
        group_number = int(raw_input('Enter group number to analyze:'))
    except ValueError:
        print("NaN! Try again!")
    group_data = data['response'][group_number]
    return group_data


def get_group_id(group_data):
    group_id = group_data['id']
    return group_id


def get_group_name(group_data):
    group_name = group_data['name']
    return group_name


def process_group_data(group_data, access_token):
    group_id = get_group_id(group_data)
    response = requests.get('https://api.groupme.com/v3/groups/'+group_id+'/messages?token='+access_token)
    data = response.json()
    messages = {}
    messages_only = []
    while True:
        for i in xrange(20):  # API sends messages in batches of 20
            try:
                message_id = data['response']['messages'][i]['id'] 
                sender = data['response']['messages'][i]['name'] 
                sender_id = data['response']['messages'][i]['sender_id']
                raw_message = data['response']['messages'][i]['text']
                epoch_time_sent = data['response']['messages'][i]['created_at']
                if raw_message:
                    message = sanitize_text(raw_message.encode('utf-8'))
                    messages[message_id] = {'sender': sender, 'sender_id': sender_id, 'message': message,
                                            'time_sent': epoch_time_sent}
                    messages_only.append(message+'.')
            except IndexError :  # retrieved all the messages
                messages_text = " ".join(messages_only)
                return messages, messages_text
        payload = {'before_id': message_id}
        response = requests.get('https://api.groupme.com/v3/groups/'+group_id+'/messages?token='+access_token, params=payload)
        data = response.json()

