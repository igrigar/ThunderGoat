import os
from telegram import Updater

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text='I will kill ya all')

def main():
	
	# Get bot auth token. 
	my_token = ''
	with  open('../etc/token', 'r') as token_f:
		my_token = token_f.readline().rstrip()
	token_f.close()

	# Creating the updater and the dispatcher.
	updater = Updater(token='126577938:AAHYlTIDYKoLP_wNUYRPX2BYtgJA3FLpKX4')
	dp = updater.dispatcher
	

	# Loading modules to the bot.
	dp.addTelegramCommandHandler('start', start)

	updater.start_polling()
	updater.idle()	

if __name__ == '__main__':
	main()
