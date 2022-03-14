import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
import sqlite3
import oauthlib

#iniate variables
token_url = 'https://api.intra.42.fr/oauth/token'
auth_link = ''
redirect_link = ''
telegram_token = ''
uid = ''
secret = ''
oauth = oauthlib.oauth2.rfc6749.tokens.OAuth2Token({})

load_dotenv()
try:
	telegram_token = os.environ['TOKEN']
except:
	print("Error\nNo TOKEN was found, create a .env file and put a variable called TOKEN in it")
	exit(1)

try:
	uid = os.environ['UID']
except:
	print("Error\nNo UID was found, create a .env file and put a variable called UID in it")
	exit(1)

try:
	secret = os.environ['SECRET']
except:
	print("Error\nNo SECRET was found, create a .env file and put a variable called SECRET in it")
	exit(1)

try:
	auth_link = os.environ['AUTH_LINK']
except:
	print("Error\nNo AUTH_LINK was found, create a .env file and put a variable called SECRET in it")
	exit(1)

try:
	redirect_link = os.environ['REDIRECT_LINK']
except:
	print("Error\nNo REDIRECT_LINK was found, create a .env file and put a variable called SECRET in it")
	exit(1)


try:
	oauth = OAuth2Session(client_id=uid, redirect_uri=redirect_link)
except:
	print("Error\nCould not create oauth-session, probably because the client id or the secret is wrong")
	exit(1)

try:
	con = sqlite3.connect('tokens.db')
	cur = con.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS tokens(access_token text, token_type text, expires_in int, refresh_token text, created_at int, expires_at double, chat_id int PRIMARY KEY)''')
	con.commit()
	con.close()
except:
	print("Error\nCould not create token-database")
	exit(1)

try:
	con = sqlite3.connect('notifications.db')
	cur = con.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS notifications(chat_id INT, notification_time timestamp, event_id INT, event_start_time timestamp, event_name TEXT, seconds_till INT)''')
	con.commit()
	con.close()
except:
	print("Error\nCould not create-notfication-database")
	exit(1)