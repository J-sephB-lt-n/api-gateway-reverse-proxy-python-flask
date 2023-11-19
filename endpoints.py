"""Defines backend service endpoints (called by the API gateway)"""

# standard lib imports #
import datetime
import json

# 3rd party imports #
import flask

app = flask.Flask(__name__)


@app.route("/return_to_sender", methods=["GET", "POST"])
def return_to_sender():
    """Returns text string explaining what was sent in the request"""
    debug_text: str = f'received {flask.request.method} request at {datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")} UTC'
    req_params = flask.request.args
    debug_text += "\nquery parameters:"
    if req_params:
        for key, val in req_params.items():
            debug_text += f"\n    {key}: {val}"
    else:
        debug_text += "\n    <none>"

    if "application/json" in flask.request.headers.get("Content-Type", ""):
        debug_text += "\nJSON:\n"
        debug_text += json.dumps(flask.request.get_json(), indent=4)

    return flask.Response(debug_text, status=200)
