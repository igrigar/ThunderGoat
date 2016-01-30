import os
import json

def set(bot, update):
    """
    Assings a value to a key. Command format: key, value
    hand:command
    """

    # Check message format
    try:
        update.message.text.index(":")
    except:
        bot.sendMessage(update.message.chat_id, text="Bad format. Correct format is '/set [key]:[value]'")
        return

    path = os.path.realpath(__file__)[:-7] + "/data/get-set"
    filename = "/archive" + str(update.message.chat_id) + ".json"
    correct = 0

    # Check for the current entries archive
    # In case this chat doesn't have an archive yet, we create and initialize it
    if not (os.path.isfile(path + filename)):
        # Check for the folder
        if not os.path.exists(path):
            os.makedirs(path)

        # Create and initialize the new file
        with open(path+filename, "w+") as archive:
            # initialize new blank file
            archive.write("{'values' : []}")

    # Update the file when it already exists
        # Open the archive
    readable = open(path+filename).read()
        # Parse JSON
    dic = json.loads(readable)
        # Obtain the value for the given key if it exists
    dic[update.message.text['values'][5:update.message.text.index(":")-1]] = update.message.text[update.message.text.index(":")+1:]
        # Update the file
    with open('my_file.json', 'w+') as writable:
        writable.write(json.dumps(dic))

    # return success
    bot.sendMessage(update.message.chat_id, text="Entries updated!")



def get(bot, update):
    '''
    Obtains the key for a certain value.
    hand:command
    '''

    if (os.path.isfile(path + filename)):
        path = os.path.realpath(__file__)[:-7] + "/data/get-set/archive" + str(update.message.chat_id) + ".json"
        # Open the archive
        archive = open(path).read()
        # Parse JSON
        dic = json.loads(archive)
        # Obtain the value for the given key if it exists
        try:
            value = dic[update.message.text[5:]]
            bot.sendMessage(update.message.chat_id, text=str(input) + " is " + value, reply_to_message_id=update.message.message_id)
        except:
            bot.sendMessage(update.message.chat_id, text="No matching key was found", reply_to_message_id=update.message.message_id)
    else:
        bot.sendMessage(update.message.chat_id, text="No matching key was found", reply_to_message_id=update.message.message_id)
