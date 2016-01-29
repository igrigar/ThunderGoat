import os
import operator
from datetime import datetime
from threading import Timer
 
spam_rank = {}

def spamreader(bot, update):
    """
    Definition: read messages and count the number of messages per user in a group.
    Hand: message
    """
   
    """
    Generatig key for the dictionary; strucute ->
        1:username:chatId when the user has set a username (@whatever).
        0:firstname_lastname:chatId when user has not a username.
    """    
    hash_key = ''
    if update.message.from_user.username != '':
        hash_key = '1:'+update.message.from_user.username+':'+str(update.message.chat_id)
    else:
        hash_key = '0:'+update.message.from_user.first_name+'_'+update.message.from_user.last_name+':'+str(update.message.chat_id)

    # Check if there is an entry in the dictionary and update it.
    if spam_rank.has_key(hash_key):
        spam_rank[hash_key] = int(spam_rank[hash_key]) + 1
    else:
        spam_rank[hash_key] = 1

def stats(bot, update):
    """
    Description: send the ranking sorted by value to the group.
    Hand: command
    """
    
    msg = ''
    sorted_rank = sorted(spam_rank.items(), key=operator.itemgetter(1), reverse=True)

    # Generate message with the spammer rank of a certain group.
    for user, value in sorted_rank:
        if str(user).split(':')[2] == str(update.message.chat_id):

            # Add the '@' if the key is the username.
            if int(str(user).split(':')[0]) == 1:
                msg = msg+'@'

            msg = msg+str(user).split(':')[1]+': '+str(value)+'\n'
    
    bot.sendMessage(update.message.chat_id, text=msg)
