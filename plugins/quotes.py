import os
import random

def quote(bot, update):
    """
    Returns a random quote from the archive
    hand:command
    """

    # First choose the correct path
    path = os.path.dirname(os.path.realpath(__file__))[:-7] + "data/quotes/archive" + str(update.message.chat_id) + ".txt"

    if (os.path.isfile(path)):
        with open(path, "r") as archive:
            # The number of quotes are written at the beginning of each archive file
            parameter = archive.readline()

            # Strip that line and transform it into int
            nquotes = int(parameter.strip("Quotes:\n"))

            #Choose a random quote among them
            all_quotes = archive.readlines()
            quote = all_quotes[random.randint(0, nquotes-1)]

        # Send the message with the chosen quote
        bot.sendMessage(update.message.chat_id, text=quote)

    # Maybe this chat has not yet any saved quotes
    else:
        bot.sendMessage(update.message.chat_id, text="There are no saved quotes in this chat. You can add them using /addquote.")


# def addquote(bot, update):
def addquote(bot, update):
    """
    Adds a new quote to the archive
    hand:command
    """
	path = os.path.dirname(os.path.realpath(__file__))[:-7] + "data/quotes/archive" + str(update.message.chat_id) + ".txt"

    if (os.path.isfile(path)):
        # Open the file in a safe way, no memory leaks
        with open(path, "r+") as archive:

            # Update the number of quotes
            parameters = archive.readline()
            nquotes = int(parameters.strip("Quotes:\n")) + 1
            archive.seek(0, 0)
            archive.write(("Quotes: " + str(nquotes) +"\n").encode('utf-8'))

            # Write the new quote
            archive.seek(0, 2)
            archive.write((update.message.text[10:] + "\n").encode('utf-8'))

    # In case this group has not yet an archive we create it and add everything
    else:

        # Maybe there is no quotes folder, create it
        if not os.path.exists("../data/quotes"):
            os.makedirs("../data/quotes")

        # In any case, create a new file and initialize it
        with open("../data/quotes/archive" + str(update.message.chat_id) + ".txt", "w+") as archive:
            archive.write("Quotes: 1\n")
            archive.write((update.message.text[10:] + "\n").encode('utf-8'))

    bot.sendMessage(update.message.chat_id, text="New quote added!")
