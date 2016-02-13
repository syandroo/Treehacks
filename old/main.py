from alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

demo_text = "Hi i am andrew. Trying the thing out."
abbreviations = {'dr.': 'doctor', 'mr.': 'mister', 'bro.': 'brother', 'bro': 'brother', 'mrs.': 'mistress', 'ms.': 'miss', 'jr.': 'junior', 'sr.': 'senior',
                 'i.e.': 'for example', 'e.g.': 'for example', 'vs.': 'versus'}
terminators = ['.', '!', '?']
wrappers = ['"', "'", ')', ']', '}']

# TODO - extract text from article

# splits sentences from paragraphs ====================================
def find_sentences(paragraph):
   end = True
   sentences = []
   while end > -1:
       end = find_sentence_end(paragraph)
       if end > -1:
           sentences.append(paragraph[end:].strip())
           paragraph = paragraph[:end]
   sentences.append(paragraph)
   sentences.reverse()
   return sentences


def find_sentence_end(paragraph):
    [possible_endings, contraction_locations] = [[], []]
    contractions = abbreviations.keys()
    sentence_terminators = terminators + [terminator + wrapper for wrapper in wrappers for terminator in terminators]
    for sentence_terminator in sentence_terminators:
        t_indices = list(find_all(paragraph, sentence_terminator))
        possible_endings.extend(([] if not len(t_indices) else [[i, len(sentence_terminator)] for i in t_indices]))
    for contraction in contractions:
        c_indices = list(find_all(paragraph, contraction))
        contraction_locations.extend(([] if not len(c_indices) else [i + len(contraction) for i in c_indices]))
    possible_endings = [pe for pe in possible_endings if pe[0] + pe[1] not in contraction_locations]
    if len(paragraph) in [pe[0] + pe[1] for pe in possible_endings]:
        max_end_start = max([pe[0] for pe in possible_endings])
        possible_endings = [pe for pe in possible_endings if pe[0] != max_end_start]
    possible_endings = [pe[0] + pe[1] for pe in possible_endings if sum(pe) > len(paragraph) or (sum(pe) < len(paragraph) and paragraph[sum(pe)] == ' ')]
    end = (-1 if not len(possible_endings) else max(possible_endings))
    return end


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)
# end sentences ===============================================

# TODO extract group messages, should be clean using groupme api call

# TODO return sentiments of each sentence in array
def sent(str):
  init = alchemyapi.sentiment('text', str)
  return init['docSentiment']['score']

# returns the sentiment of each string in an array
def sentArr(list):
  return map(sent, list)

# TODO show when changes in sentiment happens - probably important in convo
# consumes a list of strings and produces a list of strings that show a sentiment change > sensitivity
def sentChanged(list, sensitivity):
  sentiments = sentArr(list).append(0)
  result = []
  for x in range(len(list)):
    if abs(sentiments[x] - sentiments[x+1]) > sensitivity:
      result.append(list[x])
  return result

print sentArr(find_sentences(demo_text))
#print sentChanged(find_sentences(demo_text), 0.03)

#<<<<<<< HEAD
# TODO: extract topic of conversation at the moment
# "flow" of conversation, can also check if topic changed
#def topic(str):
#  init = alchemyapi.idk yet('text', str)
#  return init[][] idk yet
#=======
# TODO 

def current_topic(str):
  # INPUT: a string(sentence)
  # OUTPUT: the most popular concepts
 init = alchemyapi.entities('text', str, {'sentiment': 1}).pop[0]
 return init['text']#.encode('utf-8')

def topicChanged(list, currenttopic):
  #INPUT: a listof sentecnes, current_topic
  #Output: a list of sentences that changed topic
  solution = []
  for index in range(len(list)):
    if (current_topic(list[index])!=currenttopic):
      solution.append(list[index])
  return solutions


#>>>>>>> origin/master
