import sqlite3
from requests_oauthlib import OAuth2Session
import oauthlib

def open_database():
	con = sqlite3.connect('tokens.db')
	return con

def close_database(con):
	con.close()

#REPLACES token for current chat id in database
def insert_token(token, chat_id):
	con = open_database()
	cur = con.cursor()
	cur.execute("REPLACE INTO tokens(access_token,token_type,expires_in,refresh_token,created_at,expires_at,chat_id)VALUES(?,?,?,?,?,?,?)", (
		token['access_token'], token['token_type'], token['expires_in'], token['refresh_token'],token['created_at'],token['expires_at'],chat_id))
	con.commit()
	close_database(con)

#finds token of @param chat_id in database, returns -1 if no token exists
def find_token(chat_id):
	con = open_database()
	cur = con.cursor()
	cur.execute("SELECT * FROM tokens WHERE chat_id=?", (chat_id,))
	row = cur.fetchone()
	if row == None:
		return -1
	token = oauthlib.oauth2.rfc6749.tokens.OAuth2Token({})
	token['access_token'] = row[0]
	token['token_type'] = row[1]
	token['expires_in'] = row[2]
	token['refresh_token'] = row[3]
	token['scope'] = ['public']
	token['created_at'] = row[4]
	token['expires_at'] = row[5]
	close_database(con)
	return token
