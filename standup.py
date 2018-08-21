from flask import Flask
from flask import request
import json
from datetime import datetime
from ConfigParser import SafeConfigParser


"""
Read in and parse config options
"""

config = SafeConfigParser()
config.read('config')

listen_port = config.get('main', 'listen_port')
include_channel = config.get('main', 'include_channel')
date_format = config.get('main', 'tag_date_format')
compact_date= config.get('main', 'compact_date')


app = Flask(__name__)


@app.route("/standup", methods=['POST'])
def slash_command():
    """
    Retrieve text field from the form request which contains
    the message entered by the user who invoked the slash command
    """
    form_text = request.form["text"]
    channel = "_"+request.form["channel_name"] if include_channel == 'True' else " "
    short_tag_date = "%m%d%Y" if date_format == 'mdy' else "%Y%m%d"
    long_tag_date =  "%m_%d_%Y" if date_format == 'mdy' else "%Y_%m_%d"
    tag_date = short_tag_date if compact_date == 'True' else long_tag_date


    if len(form_text) > 0:
        """
        Format the return message with markdown with standup hash tags
        """
	output = "##### Status Update for {}\n\n{}\n\n#standup-{} #standup".format(
                datetime.strftime(datetime.now(), "%A %-d %B %Y"),
                form_text,
                datetime.strftime(datetime.now(), tag_date+channel),
            )

        """
        Create data json object to return to Mattermost with
        response_type = in_channel (everyone sees) or ephemeral (only sender sees)
        text = the message to send
        """
        data = {
            "response_type": "in_channel",
            "text": output,
        }
    else:
        """
        If the user didn't type a message send a note that only
        they see about typing a message
        """
        data = {
            "response_type": "ephemeral",
            "text": "Error: No status message entered. Please try again.",
        }

    """
    Create the response object to send to Mattermost with the
    data object written as json, 200 status, and proper mimetype
    """
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=listen_port, debug=False)
