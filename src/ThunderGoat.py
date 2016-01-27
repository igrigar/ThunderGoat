import os
import sys
from telegram import Updater

def start(bot, update):
	bot.sendMessage(update.message.chat_id, text='I will kill ya all')

def main():
	
	bot_dir = os.path.dirname(os.path.realpath(__file__))[:-3]
	
	# Import all modules.
	sys.path.append(bot_dir+'plugins/')
	for module in os.listdir(os.path.dirname(bot_dir+'plugins/')):
		if module == '__init__.py' or module[-3:] != '.py':
			continue
		__import__(module[:-3], locals(), globals())
	del module
	
	# Get bot auth token. 
	token = ''
	with  open(bot_dir+'etc/token', 'r') as token_f:
		token = token_f.readline().rstrip()
	token_f.close()

	# Creating the updater and the dispatcher.
	updater = Updater(token)
	dp = updater.dispatcher
	

	# Loading modules to the bot.
	dp.addTelegramCommandHandler('start', start)
	dp.addTelegramCommandHandler('echo', echo)

	updater.start_polling()
	updater.idle()	


if __name__ == '__main__':
	main()
