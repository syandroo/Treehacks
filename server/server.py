# visualization tools for conversation summerisation.
from tornado import (ioloop, web)
import simplejson as json

from .config import SERVER_ROOT, SLACK_TOKEN
from segmentation.cluster import spectral_clustering, split_messages, adhoc_clustering
from segmentation.preprocessing.slack import merge_messages_by_sender

from generate_summary_json import get_message_data

import text_analysis

import os

import random
#messages = [
#    '''
#    Don't forget it's Valentine's Day tomorrow!!
#                    Put your name down if you wanna meet your hacker valentine this weekend
#    ''',
#    '''
#    I would like to celebrate Valentine's Day with tea!
#    ''',
#    '''
#    which parrot mini drone?
#    I\u2019ve had some success using this with a Parrot Spider mini drone:
#    '''
#]
#labels = spectral_clustering(messages, num_clusters=2)

# start syncing threads.
try:
    from .source.slack import start_sync as start_slack_sync, get_messages as get_slack_messages
    # start_slack_sync(15)
except Exception as e:
    print '[server] error: ', e.message


def segmentation(message_data):
    channel_name = message_data['channel_name']
    messages = message_data['messages']
    messages = merge_messages_by_sender(messages)
    labels = spectral_clustering(messages, num_clusters=5)
    # labels = adhoc_clustering(messages)
    return (channel_name, messages, labels)


def summarization(messages, labels):
    messages_split = split_messages(messages, labels)
    summaries = []
    for messages in messages_split:
        message = ' '.join(
                [message['sender']['full_name'] + ': \n' +
                    message['text'] + '\n' for message in messages]
            )
        highlight_sentences = text_analysis.groupSummary(message)
        summary = ' '.join(highlight_sentences)
        summaries.append(summary)
    return summaries


class SegmentationHandler(web.RequestHandler):
    '''
    visualize segmentation results.
    '''
    def get(self):
        (channel_name, messages, labels) = segmentation()
        self.render('segmentation.html', data=json.dumps({
                    'messages': messages,
                    'labels': list([int(label) for label in labels]),
                }), channel_name=channel_name)

class SummarizationHandler(web.RequestHandler):
    '''
    visualize summerization results
    '''
    def get(self):
        (channel_name, messages, labels) = segmentation()
        summaries = summarization(messages, labels)
        self.render('summarization.html',
                summaries=json.dumps(summaries),
                labelset = json.dumps(list([int(label) for label in set(labels)])),
                channel_name=channel_name)


class MainHandler(web.RequestHandler):
    def get(self):
        access_token = os.getenv('TREEHACKS_SLACK_ACCESS_TOKEN')
        channel_id = self.get_argument('channel_id')
        channel_name = self.get_argument('channel_name')
        num_messages = self.get_argument('text')

        message_data = get_message_data(channel_id, channel_name, num_messages, access_token)
        message_data = json.loads(message_data)

        (channel_name, messages, labels) = segmentation(message_data)

        summaries = summarization(messages, labels)

        summary_index = random.randint(0, len(summaries))
        summary = summaries[summary_index]

        return self.write(summary)


handlers = [
    (r"/(.*\.jpg)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/"}),
    (r"/(.*\.png)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/"}),
    (r"/(.*\.css)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/css/"}),
    (r"/(.*\.js)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/js/"}),
    # main routes.
    (r"/segmentation", SegmentationHandler),
    (r"/summarization", SummarizationHandler),
    (r"/", MainHandler),
]

settings = {
    "autoreload": True,
    "debug": True,
    "template_path": SERVER_ROOT + "/frontend/template"
}



