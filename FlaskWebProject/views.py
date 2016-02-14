"""
Routes and views for the Flask application.
"""

from flask import render_template, request
from FlaskWebProject import app

from oauth_constants import TEST_TEAM_SLACK_ACCESS_TOKEN 
from generate_summary_json import generate_summary_json

global TEST_TEAM_SLACK_ACCESS_TOKEN


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page'
    )


# text is number of messages
@app.route('/summarize', methods=['GET'])
def summarize():
    member_id = requests.args.get('user_id')
    channel_id = requests.args.get('channel_id')
    channel_name = requests.args.get('channel_name')
    num_messages = requests.args.get('text')
    summary_json = generate_summary_json(member_id, channel_id, channel_name, num_messages, TEST_TEAM_SLACK_ACCESS_TOKEN)
    return {'text': channel_name, 'private': True}


if __name__ == '__main__':
    app.run(debug=True)