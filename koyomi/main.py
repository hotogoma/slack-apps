import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packages'))

import json
from datetime import datetime, timezone, timedelta
import urllib.request
import koyomi


GOOGLE_CALENDAR_ID = 'japanese__ja@holiday.calendar.google.com'
GOOGLE_CALENDAR_API_BASE = 'https://www.googleapis.com/calendar/v3'


def fetch_holiday_info(dt):
    assert type(dt) == datetime

    date = datetime(dt.year, dt.month, dt.day, 9, tzinfo=dt.tzinfo)

    params = {
        'timeMin': date.isoformat(),
        'timeMax': (date + timedelta(seconds=1)).isoformat(),
        'key': os.environ.get('GOOGLE_API_KEY'),
    }
    url = '{}/calendars/{}/events'.format(GOOGLE_CALENDAR_API_BASE, GOOGLE_CALENDAR_ID)

    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(req) as res:
        body = json.load(res)

    if len(body['items']) > 0:
        return body['items'][0]['summary']

    return None


def datetime_to_slack_message(dt: datetime) -> dict:
    assert type(dt) == datetime

    week = '月火水木金土日'[dt.weekday()]
    holiday = fetch_holiday_info(dt)
    if holiday:
        week += '祝'
    else:
        holiday = ''
    title = dt.strftime('%m月%d日({}) {}です').format(week, holiday)
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

    message = {
        'username': 'koyomi',
        'icon_emoji': ':calendar:',
        'attachments': [attachment],
    }

    # 祝日か二十四節気のときだけ投稿する
    return message if holiday or k else None:


def post_message_to_slack(message: dict):
    data = json.dumps(message).encode('ascii')
    url = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)


def handler(event, context):
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(tz=JST)
    message = datetime_to_slack_message(now)
    if message:
        post_message_to_slack(message)
