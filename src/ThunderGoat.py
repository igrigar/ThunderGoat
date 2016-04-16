#!/usr/bin/env python
# -*- coding: utf8 -*-

import logging
import json
import os
import sys
from telegram.ext import Updater

# Dictionary of command(key) and its description.
help_dic = {}

def main():

    # Record where is located bot's main file, AKA this very one.
    bot_dir = os.path.dirname(os.path.realpath(__file__))[:-3]
    plugin_dir = bot_dir + 'plugins/'

    # Check that the config dir and config file exist.
    if os.path.exists(bot_dir + 'etc/') == False or \
            os.path.isfile(bot_dir + 'etc/config.json') == False:

        # Send error message and end execution.
        print "ERROR: There must exist a file 'config.json' in dir 'etc'"
        exit()

        # Get the config.
    with open(bot_dir + '/etc/config.json', 'r') as f:
        config = json.load(f)

    # Tuning up the bot.
    updater = Updater(str(config["token"]))
    dp = updater.dispatcher
    daemon_queue = updater.job_queue

    # Import all modules.
    sys.path.append(bot_dir)
    import plugins

    # Parse all the files for the function names, I'm not really a fan of
    # this, but it works.
    for module in os.listdir(os.path.dirname(plugin_dir)):
        if module == '__init__.py' or module[-3:] != '.py':
            continue

        description = ''
        desc = 0

        with open(plugin_dir + module, 'r') as f:
            for line in f:

                if line.replace(' ', '')[:3] == 'def':
                    command = line.replace(' ', '')[3:].split('(', 1)[0]
                    mod = 'plugins.' + module[:-3]

                    # Create the handler.
                    var = sys.modules[mod]
                    handler = getattr(var, command)
                    continue

                # Get the description.
                if line.replace(' ', '').split(':', 1)[0].lower() == 'description':

                    desc = 1
                    description += line.split(': ', 1)[1]

                # Check if the command requires a command or a message handler.
                elif line.replace(' ', '').split(':', 1)[0].lower() == 'hand':
                    desc = 0
                    var = line.replace(' ', '').split(':', 1)[1].rstrip()

                    if var == 'command':
                        dp.addTelegramCommandHandler(command, handler)
                        help_dic[str(command)] = description.replace('\n', '')
                        description = ''
                        print 'From module:', mod, 'Function:', command, var

                    elif var == 'message':
                        dp.addTelegramMessageHandler(handler)
                        print 'From module:', mod, 'Function:', command, var

                    elif var.split(':')[0] == 'daemon':
                        periodic = True
                        if int(var.split(':')[1].rstrip()) == 0:
                            periodic = False
                        daemon_queue.put(handler, int(
                            var.split(':')[1].rstrip()), repeat=periodic)
                        print 'From module:', mod, 'Function:', command, var, 't(s):', var.split(':')[1].rstrip()

                elif desc == 1:
                    description += line.replace('    ', ' ', 1)

    del module

    dp.addTelegramCommandHandler("help", help)

    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    logger = logging.getLogger(__name__)

    # Starting the bot itself.
    updater.start_polling()
    updater.idle()


def help(bot, update):

    search = str(update.message.text[6:])
    if help_dic.has_key(search) or help_dic.has_key('/' + search):
        bot.sendMessage(update.message.chat_id, text=help_dic[search])

    elif search == 'all':
        msg = ''
        for command in help_dic:
            msg += command + ':\t' + help_dic[command] + '\n'

        bot.sendMessage(update.message.chat_id, text=msg)
    else:
        bot.sendMessage(update.message.chat_id,
            text='That command does not exist, please chek all commands with /help all')


if __name__ == '__main__':
    main()
