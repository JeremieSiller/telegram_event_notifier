import requests
from requests_oauthlib import OAuth2Session
from setup import oauth
from setup import secret

def authenticate(code):
	try:
		token = oauth.fetch_token(token_url='https://api.intra.42.fr/oauth/token', code=code, client_secret=secret)
	except:
		return -1
	return token