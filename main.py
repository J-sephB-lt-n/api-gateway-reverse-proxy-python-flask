"""
Defines the main endpoint (the API gateway)
"""

# 3rd party package imports #
import flask
import requests

# project module imports #
from endpoint_routing import endpoint_routing

app = flask.Flask(__name__)


@app.route("/<path:requested_path>", methods=["GET", "OPTIONS", "POST"])
def forward_request(requested_path: str):
    """Forwards the user request to the requested endpoint, and
    returns the response back to the user"""
    # check if requested endpoint exists #
    if requested_path not in endpoint_routing:
        return flask.Response(f"endpoint '/{requested_path}' not found", status=404)

    # can run any pre-request steps here #
    # e.g. IP-blocking, rate-limiting, security checks etc.

    # forward the request to the requested endpoint #
    endpoint_response = requests.request(
        method=flask.request.method,
        url=endpoint_routing[requested_path],
        timeout=60,
        params=flask.request.args,
        data=flask.request.data,
        # headers=dict(flask.request.headers.items()),
        # files=flask.request.files,
    )

    # can run any post-request steps here #
    # e.g. transformations, data cleaning, compression, request augmentation

    # return the response from the requested endpoint #
    response = flask.Response(
        response=endpoint_response.content,
        status=endpoint_response.status_code,
        headers={
            name: value
            for name, value in endpoint_response.headers.items()
            if name.lower()
            not in [
                "content-encoding",
                "content-length",
                "transfer-encoding",
                "connection",
            ]
        },
    )

    return response
