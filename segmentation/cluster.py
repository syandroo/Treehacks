# cluster the messages in a channel.
import numpy as np
import sklearn.cluster

from segmentation.preprocessing.slack import parse_body
from segmentation.distance import keywords_l0
from segmentation.feature import extract_all

def spectral_clustering(messages, dist_func=keywords_l0, num_clusters=3):
    '''
    takes a list of converstation messages and return `num_cluster` threads.
    '''
    m = len(messages)
    affinity = np.zeros((m, m))

    # extract message features.
    for (mi, message) in enumerate(messages):
        if type(message) != dict:
            message = {
                'text': message
            }
        if 'feat' not in message: # extract on the fly.
            message['feat'] = extract_all(parse_body(message['text']))
        messages[mi] = message # write back.

    # build affinity matrix.
    for mi in range(m):
        for mj in range(m):
            affinity[mi, mj] = np.exp(-1.0 * keywords_l0(
                        messages[mi]['feat'],
                        messages[mj]['feat']
                    ))

    # run clustering.
    print affinity
    labels = sklearn.cluster.spectral_clustering(affinity, n_clusters=num_clusters, eigen_solver='arpack')

    return labels


def split_messages(messages, labels):
    # segment messages by labels.
    messages_split = [[] for label in set(labels)]

    for (mi, message) in enumerate(messages):
        messages_split[labels[mi]].append(message)

    return messages_split





