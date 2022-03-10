import secrets
import sys
from traceback import print_tb
import telegram
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
import requests
import time
# from telegram.ext import Updater


try:
	load_dotenv()
	token = os.environ['TOKEN']
except:
	print("Error\nNo TOKEN was found, create a .env file and put a variable called TOKEN in it")
	exit(1)

bot = telegram.Bot(token=token)
print("Connected to following bot:")
print(bot.get_me())
msg = bot.get_updates()[-1]
user = msg.message.from_user.id

uid = os.environ['UID']
secret = os.environ['SECRET']
print('secret', secret)

url = 'https://api.intra.42.fr/oauth/authorize?client_id=8187b1956521b380a86c2e054f4f10e80e3f737f6474eda1480f00bdc4fa8c05&redirect_uri=http%3A%2F%2Flocalhost&response_type=code'
bot.send_message(text='Please authorize via following link:\n{}'.format(url), chat_id = user)
# print("link: ", url)
# payload = input("code: ")

oauth = OAuth2Session(client_id=uid, redirect_uri="http://localhost")

time.sleep(20)
msg = bot.get_updates()[-1]
payload = msg.message.text.split()[1]
print('|', payload, '|')

# try:
token = oauth.fetch_token(token_url='https://api.intra.42.fr/oauth/token', code=payload, client_secret=secret)
print(token)
# print('where')
# while (1):
response = requests.get("https://api.intra.42.fr/oauth/token/info", token)
user = response.json()
print(user)

myobj = {
	'grant_type': 'refresh_token',
	'&refresh_token': token['refresh_token'],
	'&client_id' : uid,
	'&client_secret' : secret
}

#https://api.intra.42.fr/oauth/token
response = requests.post(url='https://api.intra.42.fr/oauth/token',data=myobj)
print(response)
# except:
	# print('failed')
# user = updates[-1].message.from_user.id
# name = updates[-1].message.from_user.first_name
# if updates[-1].message.text == 'whats your name':
# 	msg = "Toni"
# else:
# 	msg = "Hi {}".format(name)

# bot.send_message(text=msg, chat_id=user)