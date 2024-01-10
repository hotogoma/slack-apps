import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packages'))

import json
import urllib.request
import koyomi


def post_message_to_slack(message: dict):
    data = json.dumps(message).encode('ascii')
    url = os.getenv('SLACK_INCOMING_WEBHOOK_URL')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)


def handler(event, context):
    k = koyomi.today()
    if k is None:
        return
    post_message_to_slack({
        'username': k.name,
        'icon_emoji': ':calendar:',
        'text': k.description,
    })
