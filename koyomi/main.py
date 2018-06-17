import os
import json
from datetime import datetime, timezone, timedelta
import urllib.request
import koyomi


JST = timezone(timedelta(hours=+9), 'JST')


def handler(event, context):
    now = datetime.now(tz=JST)
    week = '月火水木金土日'[now.weekday()]
    title = now.strftime('%m月%d日({}{}){} です').format(week, '', '')  # TODO 祝日

    data = {
        'attachments': [
            {
                'fallback': title,
                'title': title,
                'fields': [],
            }
        ],
        'username': 'koyomi',
        'icon_emoji': ':calendar:',
    }

    k = koyomi.today()
    if k is not None:
        data['attachments']['fields'].append({
            'title': k.name,
            'value': k.description,
        })

    url = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')
    data = json.dumps(data).encode('ascii')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)
