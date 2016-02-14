"""
Routes and views for the Flask application.
"""
import os

from flask import render_template, request
from FlaskWebProject import app

from generate_summary_json import generate_summary_json


ACCESS_TOKEN = os.getenv('TEST_TEAM_SLACK_ACCESS_TOKEN')


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page'
    )


@app.route('/summarize', methods=['GET'])
def summarize(ACCESS_TOKEN):
    member_id = requests.args.get('user_id')
    channel_id = requests.args.get('channel_id')
    channel_name = requests.args.get('channel_name')
    num_messages = requests.args.get('text')
    summary_json = generate_summary_json(member_id, channel_id, channel_name, num_messages, ACCESS_TOKEN)
    return {'text': channel_name, 'private': True}


if __name__ == '__main__':
    app.run(debug=True)