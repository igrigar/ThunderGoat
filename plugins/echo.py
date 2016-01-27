def echo(bot, update):
	""" 
	Echo a string
	"""
	bot.sendMessage(update.message.chat_id, text=update.message.text[6:])
