"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

import os
import sys
import urllib2

import groupme_listener
import text_analysis
import slack_listener as slack


def main(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    slack_team_data, sc = slack.connect_to_slack()
    user_id_to_name_map = slack.map_user_id_to_names(sc)
    messages_data = slack.get_messages(slack_team_data, user_id_to_name_map, sc)
    #print messages_data

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "amzn1.echo-sdk-ams.app.[unique-value-here]"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyChannelIsIntent":
        return set_channel_in_session(intent, session)
    elif intent_name == "WhatIsMyChannel":
        return get_channel_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome!"
    speech_output = "Hello! I'm pleased to meet you! " \
                    "Tired of scrolling through all the messages from your friends? I am here to help you! " \
                    "Please tell me what channel you would like to listen to. "\
                    "The default is 55"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what channel you would like to listen to, by saying. " \
                    "I would like to listen to channel 55"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

    #return build_response({}, build_speechlet_response("card_title", "This is welcome", "", False))


def set_channel_in_session(intent, session):
    #return build_response({}, build_speechlet_response("card_title", "This is setup", "", False))
    
    # """ Sets the color in the session and prepares the speech to reply to the
    # user.
    # """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    if 'Channel' in intent['slots']:
        channel_number = intent['slots']['Channel']['value']
        #url = 'http://wwww.whatever.deployer'
        #req = urllib2.Request(url, channel_number)
        #response = urllib2.urlopen(req).read()
        response = "hello there"
        session_attributes = create_channel_attributes(chanzznel_number)
        speech_output = "This is the most recent topic that is going on in channel" + \
                        channel_number + \
                        response
        reprompt_text = "What else would you like to know?"
    else:
        speech_output = "I'm not sure which channel you would like to listen to. " \
                        "Wanna set it one more time?"
        reprompt_text = "I'm still not sure which channel you are trying to listen to" \
                        "You can tell me the number of the channel by saying, " \
                        "I would like to listen to channel 55."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    # session_attributes = {}
    # card_title = "Welcome!"
    # speech_output = "Hello! I'm pleased to meet you! " \
    #                 "Tired of scrolling through all the messages from your friends? I am here to help you!" \
    #                 "Please tell me what channel you would like to listen to"\
    #                 "The default is 55"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    # reprompt_text = "Please tell me what channel you would like to listen to, by saying" \
    #                 "I would like to listen to channel 55"
    # should_end_session = False
    # return build_response(session_attributes, build_speechlet_response(
    #     card_title, speech_output, reprompt_text, should_end_session))


def create_channel_attributes(channel_number):
    return {"Channel_Number": channel_number}

def get_channel_from_session(intent, session):
    #return build_response({}, build_speechlet_response("card_title", "This is welcome", "", False))
    #     card_title, speech_output, reprompt_text, should_end_session))
    session_attributes = {}
    reprompt_text = None

    if "Channel_Number" in session.get('attributes', {}):
        Channel_Number = session['attributes']['Channel_Number']
        speech_output = "Your current channel is " + Channel_Number
        should_end_session = False
    else:
        speech_output = "I'm not sure what your channel number is " \
                        "You can always reset the channel number"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }