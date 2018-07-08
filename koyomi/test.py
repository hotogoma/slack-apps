from unittest import TestCase
from main import *
from datetime import datetime, timezone, timedelta


JST = timezone(timedelta(hours=+9), 'JST')


class TestKoyomi(TestCase):

    def test_koyomi_date(self):
        message = datetime_to_slack_message(datetime(2018, 8, 7, tzinfo=JST))
        attachment = message['attachments'][0]
        self.assertEqual(attachment['fallback'], '08月07日(火) です')
        self.assertEqual(attachment['title'], '08月07日(火) です')
        koyomi = attachment['fields'][0]
        self.assertEqual(koyomi['title'], '立秋')
        self.assertEqual(koyomi['value'], '初めて秋の気立つがゆへなれば也')


    def test_normal_date(self):
        message = datetime_to_slack_message(datetime(2018, 8, 9, tzinfo=JST))
        attachment = message['attachments'][0]
        self.assertEqual(attachment['fallback'], '08月09日(木) です')
        self.assertEqual(attachment['title'], '08月09日(木) です')
        koyomi = attachment['fields']
        self.assertEqual(len(koyomi), 0)


    def test_holiday_date(self):
        message = datetime_to_slack_message(datetime(2018, 8, 11, tzinfo=JST))
        # TODO
