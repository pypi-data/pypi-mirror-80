import base64
import json
import requests
import jwt
import os

SWITCH_JWT_SECRET = os.getenv("SWITCH_JWT_SECRET", "my_secret_key")
SWITCH_BASE_URL = os.getenv("SWITCH_BASE_URL")


def _encode_payload(data):
    """encodes the data dict into a base64 string
    Args:
        data: (dict) request data including (headers, body, query_params, path_params, http_method) keys
    Returns:
        (string) base64 string represting the passed data dict
    """
    return base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')


def _generate_token(author):
    """generates a signed token to be passed to authenticate with the switch service
    Args:
        author: (string) identifying string which will be passed to your subscribers if they wish to know the source
                         of the message
    Returns:
        (string) the generated token
    """
    return jwt.encode({
        'Author': author
    }, SWITCH_JWT_SECRET, algorithm='HS256').decode('utf-8')


def publish(topic, author, options):
    """Fires a message into the topic queue to trigger all subscirbers with the provided options
    Args:
        topic: (string) name of the topic to trigger
        author: (string) identifying string which will be passed to your subscribers if they wish to know the source
                         of the message
        options: (dict) request data including (headers, body, query_params, path_params, http_method) keys
    Returns:
        (bool) success of failure of publish request
    Raises:
        HTTP_ERROR: if the request failed or got any respone code from 4XX, 5XX,..
    """
    if type(topic) != str or type(options) != dict:
        return False

    encoded_data = _encode_payload(data=options)
    generated_token = _generate_token(author=author)

    url = f'{SWITCH_BASE_URL}/publish'
    headers = {"Authorization": f"bearer {generated_token}"}
    payload = {"Payload": encoded_data, "Topic": topic}

    response = requests.post(url=url,
                             data=json.dumps(payload),
                             headers=headers)
    response.raise_for_status()
    return True
