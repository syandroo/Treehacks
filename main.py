#!/usr/bin/python
# coding: utf-8

import groupme_listener
import text_analysis
import slack_listener as slack


def main():
    # get GroupMe message stream
    # group_data, access_token = groupme_listener.intiate_groupme_interaction()
    # messages_info, messages_text_only = groupme_listener.process_group_data(group_data, access_token)

    # get Slack channel message stream
    slack_team_data, sc = slack.connect_to_slack()
    user_id_to_name_map = slack.map_user_id_to_names(sc)
    messages_data = slack.get_messages(slack_team_data, user_id_to_name_map, sc)


    # bot to send summary to the channel
    summary = 'does my slack-bot work?'
    slack.send_message(summary, messages_data['channel_id'], sc)
    

if __name__ == '__main__':
    main()
