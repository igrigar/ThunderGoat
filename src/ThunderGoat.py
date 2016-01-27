import os
import sys
from telegram import Updater

def main():

	bot_dir = os.path.dirname(os.path.realpath(__file__))[:-3]
	plugin_dir = bot_dir+'plugins/'
	
	# Get bot auth token. 
	token = ''
	with  open(bot_dir+'etc/token', 'r') as token_f:
		token = token_f.readline().rstrip()
	token_f.close()

	# Creating the updater and the dispatcher.
	updater = Updater(token)
	dp = updater.dispatcher
	
	# Import all modules.
	sys.path.append(bot_dir)
	import plugins

	# Parse all the files for the function names, I'm not really a fan of this, but it works.
	for module in os.listdir(os.path.dirname(plugin_dir)):
		if module == '__init__.py' or module[-3:] != '.py':
			continue
		with open(plugin_dir+module, 'r') as f:
			for line in f:
				if line[:3] != 'def':
					continue
				command = line[4:].split('(', 1)[0]
				mod = 'plugins.'+module[:-3]

				# For debug purposes print the loaded functions and the module they belong.
				print command+' '+ mod
								
				var = sys.modules[mod]
				handler = getattr(var, command)

				# Add all functions from all modules to the dispatcher.
				dp.addTelegramCommandHandler(command, handler)
		f.close()
	del module	
	
	updater.start_polling()
	updater.idle()	

if __name__ == '__main__':
	main()
