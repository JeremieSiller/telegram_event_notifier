from distutils.log import fatal
from sqlite3 import Row
from turtle import update
from xml.dom.minidom import Document
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
import requests
from icalendar import Calendar
from authenticate import authenticate, refresh_token
import database
import consts as c
import helper
import dateutil.parser as dp
import time
import event_inspector
import notification_db as notifydb

def not_authenticated(context, chat_id):
	msg = "You are not authenticated, please run /start to get started"
	context.bot.send_message(chat_id=chat_id, text=msg)

def invalid_request(context, chat_id):
	msg = "Request not possbile.\nprobably because the api is down or some internal error occured\nplease report this to jsiller"
	context.bot.send_message(chat_id=chat_id, text=msg)

def start(update: Update, context: CallbackContext):
	tmp = database.find_token(update.effective_chat.id)
	if (len(context.args) == 1):
		msg = "your code is: {}".format(context.args[0])
		tmp = authenticate(context.args[0])
		if (tmp == -1):
			msg = "Error authentication failed, please try again later"
		else:
			database.insert_token(tmp, update.effective_chat.id)
	else:
		if tmp == -1:
			msg = "Welcome to the 42 event notifier.\nTo get started authenticate your intra with the following link and press the start button when you return: {}".format(c.auth_link)
		else:
			if helper.is_token_expired(tmp) == 1:
				msg = "Your token expired, please authenticate again by clicking following link:\n{}".format(c.auth_link)
			else:
				if refresh_token(tmp) == 1:
					msg = "Your token expired, please authenticate again by clicking following link:\n{}".format(c.auth_link)
				else:
					database.insert_token(tmp, update.effective_chat.id)
					msg = "You are already authenticated\ntype /help to get a list of commands\n"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def unkown(update: Update, context: CallbackContext):
	msg = "Sorry I did not understand that\nRun /help to get a list of commands"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def msg(update: Update, context: CallbackContext):
	msg = "Sorry I did not understand that\nRun /help to get a list of commands"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def getuser(update: Update, context: CallbackContext):
	tok = database.find_token(update.effective_chat.id)
	if tok == -1 or helper.is_token_expired(tok) == 1:
		not_authenticated(context, update.effective.chat_id)
		return
	response = requests.get("https://api.intra.42.fr/v2/me", tok)
	msg = response.json()['login']
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def help(update: Update, context: CallbackContext):
	msg =	"/help - get a list of commands\n/start - get started\n/username - get your intra name\n/events - get a list of upcoming events"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def events(update: Update, context: CallbackContext):
	tok = database.find_token(update.effective_chat.id)
	if tok == -1 or helper.is_token_expired(tok) == 1:
		not_authenticated(context, update.effective.chat_id)
		return
	if (len(context.args) >= 1):
		msg = event_inspector.event_args(context.args, tok, update.effective_chat.id)
	else:
		response = requests.get("https://api.intra.42.fr/v2/me", tok)
		if (response.status_code != 200):
			invalid_request(context, update.effective.chat_id)
			return
		campus_id = response.json()['campus_users'][0]['campus_id']
		response = requests.get("https://api.intra.42.fr/v2/campus/{}/events".format(campus_id), tok)
		if (response.status_code != 200):
			invalid_request(context, update.effective.chat_id)
			return
		msg = "there are following events comming up at your campus: \n"
		js = response.json()
		ev = {}
		for events in js:
			p = dp.parse(events['begin_at'])
			s = p.timestamp()
			if time.time() < s:
				ev[s] = events
				# msg = msg + events['name'] +'\n'
		for key in sorted(ev):
			msg += ev[key]['name'] + ' at: ' + ev[key]['begin_at'] + ' id: ' + str(ev[key]['id']) + '\n'
		msg += '\n' + "If you want to run more actions on a specific event (subsrice, get notified...)\ntext me with /events EVENT_ID. e.g. /events 8"
	if type(msg) == type(Calendar()):
		context.bot.send_document(chat_id=update.effective_chat.id, document=msg.to_ical(), filename="event.ics")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def delete_notification(cur, args, chat_id):
	if (len(args) != 2):
		return "/notifications can only be exectued without or with exactly two arguements" 
	try:
		id = int(args[0])
	except:
		return "Error: {} is not a valid event_id".format(args[0])
	try:
		minutes = int(args[1])
	except:
		return "Error: {} is not a valid integer".format(args[1])
	cur.execute('''SELECT * FROM notifications WHERE chat_id=? AND seconds_till=? AND event_id=?''', (chat_id, minutes, id))
	rows = cur.fetchall()
	if len(rows) == 0:
		return "Error: there is no notification registered for id: {} and minutes: {}".format(id, minutes)
	cur.execute('''DELETE FROM notifications WHERE chat_id=? AND seconds_till=? AND event_id=?''', (chat_id, minutes, id))
	return "Successfully deleted the notification\n"

def notifications(update: Update, context: CallbackContext):
	msg = "These are all your active notifications:\n\n"
	con = notifydb.open_database()
	cur = con.cursor()
	cur.execute('''SELECT * FROM notifications WHERE chat_id=?''',(update.effective_chat.id, ))
	rows = cur.fetchall()
	if (len(rows) == 0):
		msg = "You do not have any active notifications\nrun /help for a list of commands"
	else:
		if len(context.args) == 0:
			for x in rows:
				string = "Event {name} with the id: {id} will notify you {minutes} minutes before the start of the event\n"\
					.format(name=x[4], id=x[2], minutes=int(x[5]))
				msg += string
			msg += "\nif you want to delete a notification run /notifications EVENT_ID MINUTES\n"
		else:
			msg = delete_notification(cur, context.args, update.effective_chat.id)
			con.commit()
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
	notifydb.close_database(con)