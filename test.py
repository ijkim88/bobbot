#!/usr/bin/env python

import json
import unittest

from mock import patch, Mock
from bobbot import *

class TestBobbot(unittest.TestCase):

    def setUp(self):
        self.bot = Bobbot('DUMMY_TOKEN', {})
        self.events = {
            'channel': 'D12345',
            'user': 'testuser',
        }

    def tearDown(self):
        pass

    @patch('slacker.requests')
    def test_ping(self, mock_requests):
        response = ping(None, self.bot, self.events)
        user = self.events['user']
        self.assertEqual(
            "<@%s> I'm here!" % (user), 
            response,
        )

    @patch('slacker.requests')
    def test_botid(self, mock_requests):
        data = json.dumps({
            'ok': 'true',
            'team_id': 'T12345',
            'user_id': 'U12345',
        })

        mock_requests.get.return_value = Mock(
            status_code=200,
            text=data,
        )

        response = botid(None, self.bot, self.events)
        self.assertEqual(
            "U12345",
            response,
        )

    @patch('slacker.requests')
    def test_clear(self, mock_requests):
        """
        Need to figure out a way to write this test
        """
        pass

if __name__ == '__main__':
    unittest.main()
