#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import json

data_path = os.path.dirname(os.path.realpath(__file__))[:-7] + "data/get_set.json"


def set(bot, update):
    """
    Description: Assings a value to a key. Command format: key, value
    hand:command
    """

    # Check message format
    try:
        update.message.text.index(":")
    except:
        bot.sendMessage(update.message.chat_id,
                        text="Bad format. Correct format is '/set [key]:[value]'")
        return

    group = str(update.message.chat_id)
    key = str(update.message.text.split(':', 1)[0][5:])
    value = str(update.message.text.split(':', 1)[1])

    # Check that data file exists.
    if not (os.path.isfile(data_path)):

        # Create and initialize the new file
        with open(data_path, "w+") as archive:
            # initialize new blank file
            archive.write(json.dumps({group: {key: value}}))

        bot.sendMessage(update.message.chat_id, text="Entries updated!")
        return

    else:

        with open(data_path, "r+") as archive:
            data = json.load(archive)

            if data.has_key(group):
                data[group][key] = value
            else:
                data[group] = {}
                data[group][key] = value

            archive.seek(0)
            archive.write(json.dumps(data, indent=2, ensure_ascii=True))
            archive.truncate()

    # return success
    bot.sendMessage(update.message.chat_id, text="Entries updated!")


def get(bot, update):
    """
    Description: Obtains the key for a certain value.
    hand:command
    """
    group = str(update.message.chat_id)
    key = update.message.text[5:]

    if os.path.isfile(data_path):

        with open(data_path, "r") as archive:
            data = json.load(archive)

        try:
            bot.sendMessage(update.message.chat_id, text=str(data[group][key]),
                reply_to_message_id=update.message.message_id)
        except:
            bot.sendMessage(update.message.chat_id, text="No matching key was found",
                reply_to_message_id=update.message.message_id)

    else:
        bot.sendMessage(update.message.chat_id, text="No matching key was found", reply_to_message_id=update.message.message_id)
