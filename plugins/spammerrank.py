import os
from operator import itemgetter
import json
 
spam_rank = {}

def spamreader(bot, update):
    """
    Definition: read messages and count the number of messages per user in a group.
        To accomodate to a JSON format, the dictionary has the following structure (JSON):
            {chat_id : [[user, #msgs], ...], ...}
    Hand: message
    """    

    key = str(update.message.chat_id)
    user = ''

    if update.message.from_user.username != '':
        user = '@'+str(update.message.from_user.username)
    else:
        user = update.message.from_user.first_name+'_'+update.message.from_user.last_name

    # Check if there is an entry in the dictionary and update it.
    if spam_rank.has_key(key):
        user_list = spam_rank[key]

        for lists in user_list:
            if lists[0] == user:
                lists[1] = lists[1] + 1
            

        spam_rank[key] = user_list

    else:
        spam_rank[key] = list()
        spam_rank[key].append([user, 1])
   
def stats(bot, update):
    """
    Description: send the ranking sorted by value to the group.
    Hand: command
    """

    msg = ''
    key = str(update.message.chat_id)

    if spam_rank.has_key(key) == False:
        bot.sendMessage(update.message.chat_id, text='There are no stats in this conversation. Let the spam start!!')
        return

    sorted_rank = sorted(spam_rank[key], key=itemgetter(1), reverse=True)

    for item in sorted_rank:
        msg += str(item[0])+':\t'+str(item[1])+'\n'
         
    bot.sendMessage(update.message.chat_id, text=msg)

def spam_checkpoint(bot):
    """
    Description: save the current stats in case the bot goes down to have some backup in the file spam_backup.json.
    Hand: daemon : 30
    """

    backup_file = os.path.dirname(os.path.realpath(__file__))[:-7]+'data/spam_backup.json'

    with open(backup_file, 'w') as f:
        f.write(json.dumps(spam_rank, ensure_ascii=True))

def spam_load(bot):
    """
    Description: load all the data contained in the backup file.
    Hand: daemon : 0
    """

    backup_file = os.path.dirname(os.path.realpath(__file__))[:-7]+'data/spam_backup.json'

    if (os.path.isfile(backup_file)):
        with open(backup_file, 'r') as f:
            temp = json.load(f)

        for key in temp:
            spam_rank[key] = temp[key]

def spam_boradcast(bot):
    """
    Description: broadcast the spammer rank to all the groups.
    Hand: daemon : 86400
    """
