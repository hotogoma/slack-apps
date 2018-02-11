import os
import json
import random
import urllib.parse
import urllib.request


GOOGLE_CSE_URL = 'https://www.googleapis.com/customsearch/v1'


def search_image(query):
    """Google Custom Search Engine から画像を検索してランダムに一枚を返す"""
    params = urllib.parse.urlencode({
        'searchType': 'image',
        'key': os.environ.get('GOOGLE_CSE_KEY'),
        'cx': os.environ.get('GOOGLE_CSE_ID'),
        'q': query,
    })
    url = '{}?{}'.format(GOOGLE_CSE_URL, params)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        assert 'items' in body
    return random.choice(body['items'])


def handler(event, context):
    assert event['queryStringParameters']['token'] \
        == os.environ.get('SLACK_SLASH_COMMAND_TOKEN')
    image = search_image(event['queryStringParameters']['text'])
    body = {
        'response_type': 'in_channel',
        'attachments': [
            {
                'title': image['title'],
                'title_link': image['image']['contextLink'],
                'image_url': image['link'],
            }
        ],
    }
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(body),
    }
