#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
from operator import itemgetter
import json

spam_rank = {}

backup_file = os.path.dirname(os.path.realpath(__file__))[
    :-7] + 'data/spam_backup.json'


def spam_reader(bot, update):
    """
    Definition: read messages and count the number of messages per user in a
        group. To accomodate to a JSON format, the dictionary has the following
        tructure (JSON):
            {chat_id : [[user, #msgs], ...], ...}
    Hand: message
    """

    group = str(update.message.chat_id)

	# Get the alias or the name + surname.
    if update.message.from_user.username != '':
        user = '@' + str(update.message.from_user.username)
    else:
        user = update.message.from_user.first_name + \
            '_' + update.message.from_user.last_name

    # Check if there is an entry in the dictionary and update it.
    if spam_rank.has_key(group):
        if spam_rank[group].has_key(user):
            spam_rank[group][user] += 1
        else:
            spam_rank[group][user] = 1
    else:
        spam_rank[group] = {}
        spam_rank[group][user] = 1


def stats(bot, update):
    """
    Description: send the ranking sorted by value to the group.
    Hand: command
    """

    msg = ''
    group = str(update.message.chat_id)
    podium = 1

    if spam_rank.has_key(group) == False:
        bot.sendMessage(update.message.chat_id,
            text='There are no stats in this conversation. Let the spam start!!')
        return

    sorted_rank = sorted(spam_rank[group].items(), key=itemgetter(1), reverse=True)

    for user in sorted_rank:
        msg += str(user[0]) + ':\t' + str(user[1]) + '\n'

    bot.sendMessage(update.message.chat_id, text=msg)


def spam_checkpoint(bot):
    """
    Description: save the current stats in case the bot goes down to have some
        backup in the file spam_backup.json.
    Hand: daemon : 30
    """

    with open(backup_file, 'w') as f:
        f.write(json.dumps(spam_rank, indent=2, ensure_ascii=True))


def spam_load(bot):
    """
    Description: load all the data contained in the backup file.
    Hand: daemon : 0
    """

    if (os.path.isfile(backup_file)):
        with open(backup_file, 'r') as f:
            spam_rank = json.load(f)
