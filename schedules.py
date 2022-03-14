from authenticate import refresh_token
import consts as c
from telegram import Update
from telegram.ext import CallbackContext
import database


#refreshes all tokens in database every 20 minutes 
# -> better would be a job that triggers X minutes before it expires -> not sure how to do that
def refresh_all_20(context: CallbackContext):
	con = database.open_database()
	cur = con.cursor()
	cur.execute("SELECT chat_id from tokens")
	row = cur.fetchall()
	for i in row:
		tmp = database.find_token(chat_id=i[0])
		if  tmp == -1:
			# token expired send message -> maybe somehow check if api down
			# remove token from database so message wont be send twice
			print('token expired')
			pass
		else:
			if refresh_token(tmp) == -1:
				print('token expired')
				pass
			else:
				database.insert_token(tmp, i[0])
				print('token refreshed')
	database.close_database(con)