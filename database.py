import sqlite3
from requests_oauthlib import OAuth2Session
import oauthlib

def open_database():
	con = sqlite3.connect('tokens.db')
	return con

def close_database(con):
	con.close()

def insert_token(token, chat_id):
	con = open_database()
	cur = con.cursor()
	cur.execute("INSERT INTO tokens(access_token,token_type,expires_in,refresh_token,created_at,expires_at,chat_id)VALUES(?,?,?,?,?,?,?)", (
		token['access_token'], token['token_type'], token['expires_in'], token['refresh_token'],token['created_at'],token['expires_at'],chat_id))
	con.commit()
	close_database(con)

def find_token(chat_id):
	con = open_database()
	cur = con.cursor()
	t = cur.execute("SELECT * FROM tokens WHERE chat_id=?", (chat_id,))
	if not t:
		return 1
	token = oauthlib.oauth2.rfc6749.tokens.OAuth2Token({})
	for tok in t:
		token['access_token'] = tok[0]
		token['token_type'] = tok[1]
		token['expires_in'] = tok[2]
		token['refresh_token'] = tok[3]
		token['scope'] = ['public']
		token['created_at'] = tok[4]
		token['expires_at'] = tok[5]
	close_database(con)
	return token
