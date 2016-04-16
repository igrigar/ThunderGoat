#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import os
import random

quotes_path = os.path.dirname(os.path.realpath(__file__))[
    :-7] + 'data/quotes.json'


def quote(bot, update):
    """
    Description: Returns a random quote from the archive.
    hand:command
    """

    if os.path.isfile(quotes_path) == False:
        bot.sendMessage(update.message.chat_id,
            text="There are no saved quotes in this chat. You can add them using /addquote.")

    with open(quotes_path, "r") as f:
        quotes = json.load(f)

    group = str(update.message.chat_id)

    if quotes.has_key(group) == False:
        bot.sendMessage(update.message.chat_id,
            text="There are no saved quotes in this chat. You can add them using /addquote.")
    else:
        bot.sendMessage(update.message.chat_id,
            quotes[group][random.randint(0, len(quotes[group]) - 1)])


def addquote(bot, update):
    """
    Description: Adds a new quote to the archive
    hand:command
    """

    group = str(update.message.chat_id)

    # Create the file in case it does not exist.
    if os.path.isfile(quotes_path) == False:
        with open(quotes_path, 'w') as f:
            f.write(json.dumps({}, indent=2, ensure_ascii=True))

    with open(quotes_path, 'r+') as f:
        quotes = json.load(f)

        if quotes.has_key(group):
            quotes[group].append(update.message.text[10:])
        else:
            quotes[group] = []
            quotes[group].append(update.message.text[10:])

        f.seek(0)
        f.write(json.dumps(quotes, indent=2, ensure_ascii=True))
        f.truncate()

    bot.sendMessage(update.message.chat_id, text="New quote added!")
