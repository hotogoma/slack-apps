import os
import json
import datetime
import urllib.request


def check_garbage_day(date):
    assert type(date) == datetime.date
    weeknum = int((date.day + 6) / 7)
    if date.weekday() in (1, 4):  # 火曜・金曜
        return ':fire: 可燃ごみ'
    if date.weekday() == 2:  # 水曜
        if weeknum in (2, 4):  # 第二・第四
            return ':battery: 不燃ごみ'
        else:  # 第一・第三・第五
            return ':fallen_leaf: 草木'
    if date.weekday() == 3:  # 木曜
        return ':recycle: かん・びん・紙・有害ごみ'
    if date.weekday() == 5:  # 土曜
        if weeknum in (2, 4):  # 第二・第四
            return ':recycle: ペットボトル'
    return None


def handler(event, context):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    garbage_day = check_garbage_day(tomorrow)
    if garbage_day is None:
        return

    title = '明日は {} の日です'.format(garbage_day)
    data = {
        'attachments': [
            {
                'fallback': title,
                'title': title,
            }
        ],
        'username': 'ごみの日',
        'icon_emoji': ':wastebasket:',
    }

    url = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')
    data = json.dumps(data).encode('ascii')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)
