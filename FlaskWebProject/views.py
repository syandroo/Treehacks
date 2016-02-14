"""
Routes and views for the flask application.
"""
import os
from datetime import datetime
from flask import render_template, request
from FlaskWebProject import app

from generate_summary_json import generate_summary_json


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/summarize', methods=['GET'])
def summarize():
    access_token = os.getenv('TREEHACKS_SLACK_ACCESS_TOKEN')
    member_id = request.args.get('user_id')
    channel_id = request.args.get('channel_id')
    channel_name = request.args.get('channel_name')
    num_messages = request.args.get('text')
    summary_json = generate_summary_json(member_id, channel_id, channel_name, num_messages, TEST_TEAM_SLACK_ACCESS_TOKEN)
    return {'text': channel_name, 'private': True}


if __name__ == '__main__':
    app.run(debug=True)