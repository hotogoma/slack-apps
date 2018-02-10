import os
import re
import json
import urllib.request
from xml.etree import ElementTree


def get_weather():
    """明日の天気情報を取得する"""
    url = os.environ.get('YAHOO_WEATHER_RSS_URL')
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        items = ElementTree.fromstring(body).findall('channel/item')
        today = parse_weather(items[0].findtext('description'))
        tomorrow = parse_weather(items[1].findtext('description'))
        tomorrow['diffMax'] = tomorrow['max'] - today['max']
        tomorrow['diffMin'] = tomorrow['min'] - today['min']
        tomorrow['diffMaxStr'] = diff2str(tomorrow['diffMax'])
        tomorrow['diffMinStr'] = diff2str(tomorrow['diffMin'])
    return tomorrow


def parse_weather(weather):
    """文字列から天気と気温情報を抽出する"""
    match = re.match(r'^(.+) - (-?\d+)℃\/(-?\d+)℃$', weather)
    return {
        'weather': match[1],
        'weather_emoji': replace_emoji(match[1]),
        'max': int(match[2]),
        'min': int(match[3]),
    }


def replace_emoji(weather):
    """天気の文字列を絵文字に変換する"""
    emoji = [
        ('晴', ':sunny:'), ('れ', ''),
        ('曇', ':cloud:'), ('り', ''),
        ('雨', ':umbrella:'),
        ('雪', ':snowflake:'),
        ('時々', '/'),
        ('後', '→'),
    ]
    for k, v in emoji:
        weather = weather.replace(k, v)
    return weather


def diff2str(diff):
    """数値を符号付きの文字列に変換する"""
    if diff == 0:
        return '±0'
    if diff > 0:
        return '+{}'.format(diff)
    return str(diff)


def handler(event, context):
    weather = get_weather()

    title = '明日の天気は {} です'.format(weather['weather_emoji'])
    data = {
        # 'text': 'foo',
        'attachments': [{
            'fallback': title,
            'title': title,
            'fields': [
                {
                    'title': '最高気温',
                    'value': '{}℃ (前日比{}℃)'.format(
                        weather['max'], weather['diffMaxStr']),
                    'short': True,
                },
                {
                    'title': '最低気温',
                    'value': '{}℃ (前日比{}℃)'.format(
                        weather['min'], weather['diffMinStr']),
                    'short': True,
                },
            ],
        }],
        'username': 'weather',
        'icon_emoji': ':partly_sunny_rain:',
    }
    if re.match('雨', weather['weather']):
        data['attachments']['color'] = '#439FE0'

    url = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')
    data = json.dumps(data).encode('ascii')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)
