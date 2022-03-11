from distutils.log import fatal
from urllib import response
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
import requests
from authenticate import authenticate
import sqlite3
import databse

url = 'https://api.intra.42.fr/oauth/authorize?client_id=8187b1956521b380a86c2e054f4f10e80e3f737f6474eda1480f00bdc4fa8c05&redirect_uri=http%3A%2F%2F1-E-4.42heilbronn.de&response_type=code'
token = {}

def start(update: Update, context: CallbackContext):
	if (len(context.args) == 1):
		msg = "your code is: {}".format(context.args[0])
		global token 
		t = authenticate(context.args[0])
		if (t == -1):
			msg = "Error authentication failed, please try again later"
		else:
			up = {update.effective_chat.id : t}
			token.update(up)
			print('old token: ', t)
			# print('chat:', update.effective_chat.id)
			databse.insert_token(t, update.effective_chat.id)
			print('new token :', databse.find_token(update.effective_chat.id))
			token[update.effective_chat.id] = databse.find_token(update.effective_chat.id)
			print(type(token[update.effective_chat.id]))
	else:
		msg = "Welcome to the 42 event notifier.\n To get started authenticate your intra with the following link and press the start button when you return: {}".format(url)
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