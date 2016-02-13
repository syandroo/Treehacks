Instructions:

To initialize summarization for text without title, use:

groupSummary(text) from main.py

To initialize summarization for text with title, use:

articleSummary(title, text) from main.py

Issues and possible improvements:
1. I'm trying to output a sentiment with the summaries, but the sentiment
function won't work with the output of articleSummaries or groupSummaries

They work for manually inputted lists of strings though

2. Maybe it'd be cooler too if we could use emotions instead of plain sentiment
like when they show the bullet points of what you missed, the color of the box
changes based on what the emotion is

3 To use even more Watson tools, we could check the personality of each person 
in the group chat while you were away

4. To implement the news article suggester, we need at least a simple recommender
system, or use an API to make up for the lack of it

5. Echo integration?? All that's finished so far is the text summary, and I'd say it's pretty effective

