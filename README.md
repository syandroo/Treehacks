Instructions:

If you haven't installed these yet, run:
pip install tornado
pip install easyjson
pip install flask

The summarizer is linked to the Treehacks Slack by default. 
To change this, go to slack_listener.py and add your API Access Token
to the connect_to_slack function

To initialize the server for summarization, run
$ python run_server.py

To initialize the server for splitting related messages, run
$ python server/server.py

Server will be listening at port 8889, showing the JSON data of all the groups

