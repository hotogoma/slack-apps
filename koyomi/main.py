import os
import json
from datetime import datetime, timezone, timedelta
import urllib.request
import koyomi


def datetime_to_slack_message(dt):
    assert type(dt) == datetime

    week = '月火水木金土日'[dt.weekday()]
    title = dt.strftime('%m月%d日({}{}){} です').format(week, '', '')  # TODO 祝日
    attachment = {
        'fallback': title,
        'title': title,
        'fields': [],
    }

    # 二十四節気
    k = koyomi.from_date(dt.year, dt.month, dt.day, tz=dt.tzinfo)
    if k is not None:
        attachment['fields'].append({
            'title': k.name,
            'value': k.description,
        })

    return { 'attachments': [attachment] }


def handler(event, context):
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(tz=JST)
    data = datetime_to_slack_message(now)
    data = json.dumps(data).encode('ascii')
    url = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)
