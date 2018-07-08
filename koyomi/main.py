import os
import json
from datetime import datetime, timezone, timedelta
import urllib.request
import koyomi


GOOGLE_CALENDAR_ID = 'japanese__ja@holiday.calendar.google.com'


def fetch_holiday_info(dt):
    assert type(dt) == datetime

    date = datetime(dt.year, dt.month, dt.day, 9, tzinfo=dt.tzinfo)

    params = {
        'timeMin': date.isoformat(),
        'timeMax': (date + timedelta(seconds=1)).isoformat(),
        'timeZone': 'JST',
        'key': os.environ.get('GOOGLE_API_KEY'),
    }
    url = 'https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(GOOGLE_CALENDAR_ID)

    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(req) as res:
        body = json.load(res)

    if len(body['items']) > 0:
        return body['items'][0]['summary']

    return None


def datetime_to_slack_message(dt):
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

    return { 'attachments': [attachment] }


def handler(event, context):
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(tz=JST)
    data = datetime_to_slack_message(now)
    data = json.dumps(data).encode('ascii')
    url = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)
