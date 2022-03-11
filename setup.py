import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

#iniate variables

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

redirect_uri = "http://1-E-4.42heilbronn.de"

try:
	oauth = OAuth2Session(client_id=uid, redirect_uri=redirect_uri)
except:
	print("Error\nCould not create oauth-session, probably because the client id or the secret is wrong")