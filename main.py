#!/usr/bin/python
# coding: utf-8

import os
import sys

import groupme_listener
import text_analysis
import slack_listener as slack


# article source: https://blogs.dropbox.com/developers/2015/03/limitations-of-the-get-method-in-http/
# text for testing
inputTitle = "Limitations of the GET method in HTTP"
inputText = "We spend a lot of time thinking about web API design, and we learn a lot from other APIs and discussion with their authors. In the hopes that it helps others, we want to share some thoughts of our own. In this post, we’ll discuss the limitations of the HTTP GET method and what we decided to do about it in our own API.  As a rule, HTTP GET requests should not modify server state. This rule is useful because it lets intermediaries infer something about the request just by looking at the HTTP method.  For example, a browser doesn’t know exactly what a particular HTML form does, but if the form is submitted via HTTP GET, the browser knows it’s safe to automatically retry the submission if there’s a network error. For forms that use HTTP POST, it may not be safe to retry so the browser asks the user for confirmation first.  HTTP-based APIs take advantage of this by using GET for API calls that don’t modify server state. So if an app makes an API call using GET and the network request fails, the app’s HTTP client library might decide to retry the request. The library doesn’t need to understand the specifics of the API call.  The Dropbox API tries to use GET for calls that don’t modify server state, but unfortunately this isn’t always possible. GET requests don’t have a request body, so all parameters must appear in the URL or in a header. While the HTTP standard doesn’t define a limit for how long URLs or headers can be, most HTTP clients and servers have a practical limit somewhere between 2 kB and 8 kB.  This is rarely a problem, but we ran up against this constraint when creating the /delta API call. Though it doesn’t modify server state, its parameters are sometimes too long to fit in the URL or an HTTP header. The problem is that, in HTTP, the property of modifying server state is coupled with the property of having a request body.  We could have somehow contorted /delta to mesh better with the HTTP worldview, but there are other things to consider when designing an API, like performance, simplicity, and developer ergonomics. In the end, we decided the benefits of making /delta more HTTP-like weren’t worth the costs and just switched it to HTTP POST.  HTTP was developed for a specific hierarchical document storage and retrieval use case, so it’s no surprise that it doesn’t fit every API perfectly. Maybe we shouldn’t let HTTP’s restrictions influence our API design too much.  For example, independent of HTTP, we can have each API function define whether it modifies server state. Then, our server can accept GET requests for API functions that don’t modify server state and don’t have large parameters, but still accept POST requests to handle the general case. This way, we’re opportunistically taking advantage of HTTP without tying ourselves to it."

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def main(event, context):
    # get GroupMe message stream
    # group_data, access_token = groupme_listener.intiate_groupme_interaction()
    # messages_info, messages_text_only = groupme_listener.process_group_data(group_data, access_token)

    # get Slack channel message stream
    slack_team_data, sc = slack.connect_to_slack()
    user_id_to_name_map = slack.map_user_id_to_names(sc)
    messages_data = slack.get_messages(slack_team_data, user_id_to_name_map, sc)
    print messages_data
    

if __name__ == '__main__':
    main(event, context)