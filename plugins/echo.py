def echo(bot, update):
	bot.sendMessage(update.message.chat_id, text=update.message.text[6:])
