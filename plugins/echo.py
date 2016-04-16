def echo(bot, update):
    """
    Description: echoes the string that follows the command /echo.
    Hand: command
    """
    bot.sendMessage(update.message.chat_id, text=update.message.text[6:])
