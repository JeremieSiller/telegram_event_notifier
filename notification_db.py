import sqlite3

def open_database():
	con = sqlite3.connect('notifications.db')
	return con

def close_database(con):
	con.close()


def insert_notification(chat_id, notification_time, event_id, event_start_time, event_name, num):
	con = open_database()
	cur = con.cursor()
	con.execute("INSERT INTO notifications(chat_id, notification_time, event_id, event_start_time, event_name, seconds_till)VALUES(?,?,?,?,?,?)", (
		chat_id, notification_time, event_id, event_start_time, event_name, num)
	)
	con.commit()
	close_database(con)

def check_entrys(chat_id, event_id, num):
	con = open_database()
	cur = con.cursor()
	cur.execute("SELECT * FROM notifications WHERE chat_id=? AND event_id=?", (chat_id, event_id))
	row = cur.fetchall()
	if (len(row) >= 3):
		close_database(con)
		return "There are not more than 3 notifications allowed.\nRun /notifications to manage your notifications"
	cur = con.cursor()
	cur.execute("SELECT * FROM notifications WHERE chat_id=? AND event_id=? AND seconds_till=?", (chat_id, event_id, num))
	row = cur.fetchone()
	if row == None:
		close_database(con)
		return 0
	close_database(con)
	return "Already setup the notification"
