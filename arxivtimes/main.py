import os
import re
import json
import datetime
import dateutil.parser
import urllib.request


def get_new_posts(delta):
    assert type(delta) == datetime.timedelta
    url = 'https://arxivtimes.herokuapp.com/'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read().decode()
    matched = re.search(r'^var POSTS = (.+?);$', body, flags=re.MULTILINE)
    assert matched
    data = json.loads(matched[1])
    since = datetime.datetime.now(datetime.timezone.utc) - delta
    posts = []
    for post in data['recent']:
        post['created_at'] = dateutil.parser.parse(post['created_at'])
        if post['created_at'] > since:
            posts.append(post)
        else:
            break
    return posts


def to_slack_attachment(post):
    attachment = {
        'title': post['title'],
        'title_link': post['url'],
        'text': post['headline'],
        'mrkdwn_in': ['text'],
        'footer': post['user_id'],
        'footer_icon': post['avatar_url'],
        'ts': int(post['created_at'].timestamp()),
    }
    matched = re.search(r'^(.+)!\[.*?\]\((.+?)\)', attachment['text'], flags=re.DOTALL)
    if matched:
        attachment['text'] = matched[1]
        attachment['image_url'] = matched[2]
    if len(post['labels']) > 0:
        labels = ' '.join(['`{}`'.format(label) for label in post['labels']])
        attachment['text'] = labels + '\n' + attachment['text']
    return attachment


def handler(event, context):
    posts = get_new_posts(datetime.timedelta(hours=1))
    if len(posts) == 0:
        return
    url = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')
    data = { 'attachments': [to_slack_attachment(post) for post in posts] }
    data = json.dumps(data).encode('ascii')
    req = urllib.request.Request(url, data)
    urllib.request.urlopen(req)
