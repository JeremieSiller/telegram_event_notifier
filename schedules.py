from authenticate import refresh_token
import consts as c
from telegram import Update
from telegram.ext import CallbackContext
import database
import notification_db as notifydb
import pytz
import datetime

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
	database.close_database(con)

#sends out notifications if they are outdated
def notifty(context: CallbackContext):
	con = notifydb.open_database()
	cur = con.cursor()
	now = datetime.datetime.now()
	now = pytz.UTC.localize(now)
	cur.execute('''SELECT * FROM notifications WHERE notification_time > ?''', (now, ))
	rows = cur.fetchall()
	for x in rows:
		print(type(x))
		print(x)
		msg = "The event {name} (id: {event_id}) starts in less than {minutes} minutes.\nTo get more information run /events {event_id}"\
			.format(name=x[4],event_id=x[2], minutes=(int(x[5])))
		context.bot.send_message(chat_id=x[0], text=msg)
		print(msg)
	cur.execute('''DELETE FROM notifications WHERE notification_time > ?''', (now, ))
	con.commit()
	notifydb.close_database(con)
