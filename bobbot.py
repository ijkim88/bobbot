#!/usr/bin/env python

"""
Bobbot is a bot for Slack utilizing the Slouch and Slacker APIs. I recommend 
exporting your Slack API token as $SLACK_TOKEN and call bobbot using
'$ bobbot.py $SLACK_TOKEN'

Usage:
    bobbot <slack_token>
    bobbot --help

Options:
    --help  Show this screen
"""

import datetime
import logging
import sys
import nflgame

from docopt import docopt
from slouch import Bot, help

class Bobbot(Bot):
    
    def prepare_bot(self, config):
        pass

Bobbot.command(help)

@Bobbot.command
def ping(opts, bot, event):
    """Usage: ping

    Respond with an at-mention to the sender
    """
    user_id = event['user']
    return "<@%s> I'm here!" % (user_id)

@Bobbot.command
def echo(opts, bot, event):
    """Usage: echo [<text>...]

    Echo <text>...
    """
    if opts['<text>'] is None:
        text = ""
    else:
        text = " ".join(opts['<text>'])

    if (text.startswith('"') and text.endswith('"')) or\
       (text.startswith("'") and text.endswith("'")):
        text = text[1:-1]

    return str(text)

@Bobbot.command
def botid(opts, bot, event):
    """Usage: botid

    Respond with this bot's id
    """
    botid = bot.slack.auth.test().body['user_id']
    return botid

@Bobbot.command
def clear(opts, bot, event):
    """Usage: clear <count>

    Clear bot messages (Max: 100)
    """
    channel = event['channel']
    count = int(opts['<count>'])
    messages = [message for message in bot.slack.im.history(channel).body['messages'] if message['user'] == bot.slack.auth.test().body['user_id']]
    if count > len(messages):
        count = len(messages)
    elif count > 100:
        count = 100

    for message in messages[:count]:
        ts = message['ts']
        bot.slack.chat.delete(channel, ts)

@Bobbot.command
def nflscores(opts, bot, event):
    """Usage: nflscores --team=<team> --week=<week> [--season=<season>]

    Gets NFL scores of <team> for <week>. <season> can be specified, but defaults to the current season/
    """
    team = opts['--team'].strip('"\'')
    week = int(opts['--week'].strip('"\''))
    if opts['--season'] is None:
        season = int(datetime.date.today().strftime('%Y'))
    else:
        season = int(opts['--season'].strip('"\''))

    try:
        games = nflgame.games(season, week=week, home=team, away=team)
    except:
        return "Sorry, I can't find it."

    results = games[0].nice_score().split('at')
    scores = [score.strip() for score in results]
    scores = ['*%s*' % (score) if games[0].winner in score else score for score in scores]

    return ' at '.join(scores).encode('ascii')

if __name__ == '__main__':
    args = docopt(__doc__)
    slack_token = args['<slack_token>']
    config = {}

    log = logging.getLogger('slouch')
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        fmt=('%(asctime)s %(name)s'
             ' (%(filename)s:%(lineno)s)'
             ' %(levelname)s:'
             ' %(message)s'),
        datefmt='%H:%M:%S'))
    log.addHandler(console_handler)

    bot = Bobbot(slack_token, config)
    bot.run_forever()
