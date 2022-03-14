from pickle import TRUE
import consts as c
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import routines
import schedules

def run():
	#initate telegram udater
	updater = Updater(token=c.telegram_token, use_context=True)
	dispatcher = updater.dispatcher
	jobs = updater.job_queue

	#activate logging
	# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	#addidng schedules
	jobs.run_repeating(schedules.refresh_all_20, interval=60 * 20, first=10)
	jobs.run_repeating(schedules.notifty, interval=60, first=1)

	#adding command handlers from routines.py
	dispatcher.add_handler(CommandHandler('start', routines.start))
	dispatcher.add_handler(CommandHandler('username', routines.getuser))
	dispatcher.add_handler(CommandHandler('help', routines.help))
	dispatcher.add_handler(CommandHandler('events', routines.events))
	dispatcher.add_handler(CommandHandler('notifications', routines.notifications))

	#adding random message handler:
	dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), routines.msg))

	#unkown handler must be added last
	dispatcher.add_handler(MessageHandler(Filters.command, routines.unkown))

	#start updater
	updater.start_polling()

	#wait for ctr + c signal (SIGINT)
	updater.idle()

	#stop updater
	updater.stop()

if __name__ == '__main__':
	run()
