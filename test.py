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
    def test_echo_hello_world(self, mock_requests):
        response = echo("Hello World", self.bot, self.events)
        self.assertEqual(
            "Hello World",
            response,
        )

    @patch('slacker.requests')
    def test_echo_hello_comma_world(self, mock_requests):
        response = echo("Hello,World", self.bot, self.events)
        self.assertEqual(
            "Hello,World",
            response,
        )

    @patch('slacker.requests')
    def test_echo_blank(self, mock_requests):
        response = echo("", self.bot, self.events)
        self.assertEqual(
            "",
            response,
        )

    @patch('slacker.requests')
    def test_echo_double_quotes(self, mock_requests):
        response = echo('"Hello World"', self.bot, self.events)
        self.assertEqual(
            'Hello World',
            response,
        )

    @patch('slacker.requests')
    def test_echo_double_quotes(self, mock_requests):
        response = echo("'Hello World'", self.bot, self.events)
        self.assertEqual(
            'Hello World',
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

    @patch('slacker.requests')
    def test_nflscores_week1_SF_2015(self, mock_requests):
        opts = (
            '--season=2015',
            '--week=1',
            '--team=SF',
        )
        response = nflscores(opts, self.bot, self.events)
        self.assertEqual(
            'MIN (3) at *SF (20)*',
            response,
        )

    @patch('slacker.requests')
    def test_nflscores_input_quotes(self, mock_requests):
        opts = (
            '--season="2015"',
            "--week='1'",
            '--team=SF',
        )
        response = nflscores(opts, self.bot, self.events)
        self.assertEqual(
            'MIN (3) at *SF (20)*',
            response,
        )

    @patch('slacker.requests')
    def test_nflscores_no_results(self, mock_requests):
        opts = (
            '--season=2015',
            '--week=99',
            '--team=SF',
        )
        response = nflscores(opts, self.bot, self.events)
        self.assertEqual(
            "Sorry, I can't find it.",
            response,
        )

if __name__ == '__main__':
    unittest.main()
