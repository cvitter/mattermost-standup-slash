from flask import Flask
from flask import request
import json
from datetime import datetime

__doc__ = """\
standup.py

------------------------------------------------------------------------------------------
Flask application below
"""

app = Flask(__name__)
 
@app.route( "/standup", methods = [ 'POST' ] )
def slashCommand():
    
    """
    Retrieve text field from the form request which contains the message entered by the
    user who invoked the slash command
    """
    form_text = request.form["text"]
    if len(form_text) > 0:
        """
        Format the return message with markdown with standup hash tags
        """
        output = "##### Status Update for {}\n\n{}\n\n#standup-{} #standup".format(
                datetime.strftime(datetime.now(), "%A %-d %B %Y"),
                form_text,
                datetime.strftime(datetime.now(), "%Y%m%d"),
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
        
        """
        Create the response object to send to Mattermost with the
        data object written as json, 200 status, and proper mimetype
        """
        response = app.response_class(
            response = json.dumps(data),
            status = 200,
            mimetype = 'application/json'
        )
    else:
        """
        If the user didn't type a message send a note that only they see about typing a message
        """
        data = {
            "response_type": "ephemeral",
            "text": "Error: No status message entered. Please try again.",
        }
        
        response = app.response_class(
            response = json.dumps(data),
            status = 200,
            mimetype = 'application/json'
        )

    return response

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5004, debug = False)