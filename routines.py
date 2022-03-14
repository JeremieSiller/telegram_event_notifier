from distutils.log import fatal
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
import requests
from authenticate import authenticate, refresh_token
import database
import consts as c
import helper

token = {}

def start(update: Update, context: CallbackContext):
	global token 
	if (len(context.args) == 1):
		msg = "your code is: {}".format(context.args[0])
		tmp = authenticate(context.args[0])
		if (tmp == -1):
			msg = "Error authentication failed, please try again later"
		else:
			database.insert_token(tmp, update.effective_chat.id)
			token[update.effective_chat.id] = tmp
	else:
		tmp = database.find_token(update.effective_chat.id)
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
					token[update.effective_chat.id] = tmp
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def unkown(update: Update, context: CallbackContext):
	msg = "Sorry I did not understand that\nRun /help to get a list of commands"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def msg(update: Update, context: CallbackContext):
	msg = "Sorry I did not understand that\nRun /help to get a list of commands"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def getuser(update: Update, context: CallbackContext):
	response = requests.get("https://api.intra.42.fr/v2/me", token[update.effective_chat.id])
	print(response)
	msg = response.json()['login']
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def help(update: Update, context: CallbackContext):
	msg =	"/help - get a list of commands\n/start - get started\n/username - get your intra name\n/events - get a list of upcoming events"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def events(update: Update, context: CallbackContext):
	response = requests.get("https://api.intra.42.fr/v2/me", token[update.effective_chat.id])
	campus_id = response.json()['campus_users'][0]['campus_id']
	response = requests.get("https://api.intra.42.fr/v2/campus/{}/events".format(campus_id), token[update.effective_chat.id])
	msg = "there are following events comming up at your campus: \n"
	js = response.json()
	for events in js:
		msg = msg + events['name'] +'\n'
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)