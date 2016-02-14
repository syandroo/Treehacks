# visualization tools for conversation summerisation.
from tornado import (ioloop, web)
import simplejson as json

from .config import SERVER_ROOT
from segmentation.cluster import spectral_clustering, split_messages, adhoc_clustering
from segmentation.preprocessing.slack import merge_messages_by_sender

import text_analysis
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


def segmentation():
    messages_data = get_slack_messages(16)
    channel_name = messages_data['channel_name']
    messages = messages_data['messages']
    messages = merge_messages_by_sender(messages)
    labels = spectral_clustering(messages, num_clusters=5)
    # labels = adhoc_clustering(messages)
    print labels
    return (channel_name, messages, labels)


def summarization(messages, labels):
    messages_split = split_messages(messages, labels)
    summaries = []
    for messages in messages_split:
        message = ' '.join(
                [message['sender']['full_name'] + ': \n' +
                    message['text'] + '\n' for message in messages]
            )
        print 'message', message
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



handlers = [
    (r"/(.*\.jpg)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/"}),
    (r"/(.*\.png)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/"}),
    (r"/(.*\.css)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/css/"}),
    (r"/(.*\.js)", web.StaticFileHandler, {"path": SERVER_ROOT + "/frontend/js/"}),
    # main routes.
    (r"/segmentation", SegmentationHandler),
    (r"/summarization", SummarizationHandler),
]

settings = {
    "autoreload": True,
    "debug": True,
    "template_path": SERVER_ROOT + "/frontend/template"
}



