"""
Defines the API Gateway endpoint
"""

# standard lib imports #
import json
import logging

# 3rd party package imports #
import flask
import requests

# project module imports #
import config
from endpoint_routing import endpoint_routing

# set up logging #
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# initialize Flask app #
app = flask.Flask(__name__)


@app.before_request
def before_request():
    """This code is run prior to every request"""
    # can run non-endpoint-specific pre-request steps here #
    # e.g. IP-blocking, rate-limiting, security checks etc. #

    if flask.request.origin not in config.ORIGINS_ALLOW:
        return flask.Response("FORBIDDEN", status=403)


@app.route("/<path:requested_path>", methods=["GET", "OPTIONS", "POST"])
def forward_request(requested_path: str):
    """Forwards the client request to the requested endpoint, and
    returns the response back to the client"""
    # check if requested endpoint exists in the defining routings #
    if requested_path not in endpoint_routing:
        return flask.Response(f"endpoint '/{requested_path}' not found", status=404)

    # can run endpoint-specific pre-request steps here #
    # e.g. IP-blocking, rate-limiting, security checks etc. #

    # forward the request to the requested endpoint #
    try:
        endpoint_response = requests.request(
            method=flask.request.method,
            url=endpoint_routing[requested_path],
            timeout=60,
            params=flask.request.args,
            data=flask.request.get_data(parse_form_data=False),
            headers={"Content-Type": flask.request.headers.get("Content-Type")},
        )
    except requests.exceptions.Timeout:
        return flask.Response("REQUEST TIMEOUT", status=408)

    # can run any post-request steps here #
    # e.g. transformations, data cleaning, compression, request augmentation

    # return the response from the requested endpoint #
    endpoint_response_headers_to_return_to_client = {
        name: value
        for name, value in endpoint_response.headers.items()
        if name.lower()
        not in [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        ]
    }
    # if requested endpoint sets cookies, forward those headers on to the client #
    if endpoint_response.cookies:
        endpoint_response_headers_to_return_to_client[
            "Set-Cookie"
        ] = endpoint_response.raw.headers.getlist("Set-Cookie")

    # return the response to the client #
    response = flask.Response(
        response=endpoint_response.content,
        status=endpoint_response.status_code,
        headers=endpoint_response_headers_to_return_to_client,
    )

    return response


@app.after_request
def after_request(response):
    """This code runs immediately before sending the response to the client (after the endpoint code)"""
    # e.g. can set CORS headers here etc. #

    # log request #
    logger.info(
        json.dumps(
            {
                "log_source": "api_gateway",
                "remote_address": flask.request.remote_addr,
                "request_origin": flask.request.origin,
                "response_status": response.status,
                "full_path": flask.request.full_path,
            },
            indent=4,
        )
    )

    return response
