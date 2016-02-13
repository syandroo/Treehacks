import random
import json
#input a list of sentences
#take out the top key word of each sentence in order

#classify by main topic?

json data of the conversation
who is in the conversation and emotion and what is mentioned

# consumes json file containing one topic 
# example of format of json:{user:_name_, emotion:-1, content: __str__}
# uses the user,emotion,content information provided to 
# output a generated sentence
def response_generator(json_input):
	json = json.loads(json_input)
	user = json[user]
	emotion_score = json[emotion]
	content = json[content]
	if (emotion_score < -.5):
		angry_responses = ["%s mentioned %s angrily" % (user, content), "%s is feeling extremely passionated for %s" % (user,content)]
	else if (emotion_score > 0.5):
		happy_responses = ["%s talked about %s in a very cheerful mood" % (user, content), "%s is feeling happy and said %s" % (user,content),"%s is having a great conversation on %s" % (user,content)]
	else:
		mutural_responses = ["%s elaborated on %s" % (user, contient), "%s mentioned %s" % (user,contient)]
	responses = angry_responses + happy_responses + mutural_responses
	return random.choice(responses)


