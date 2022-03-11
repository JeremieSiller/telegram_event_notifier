from setup import telegram_token
from setup import uid
from setup import secret
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import routines

#initate telegram udater
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

#activate logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#adding command handlers from routines.py
dispatcher.add_handler(CommandHandler('start', routines.start))
dispatcher.add_handler(CommandHandler('username', routines.getuser))
dispatcher.add_handler(CommandHandler('help', routines.help))
dispatcher.add_handler(CommandHandler('events', routines.events))

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
