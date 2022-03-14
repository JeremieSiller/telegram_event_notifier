from urllib import response
import consts as c
import requests
import dateutil.parser as dp
import datetime
from icalendar import Calendar, Event
from dateutil import parser
import notification_db as notifydb
import pytz

#not correct when event is for more than a day
def caluclate_duration(begins_at, ends_at):
	p_b = dp.parse(begins_at)
	p_e = dp.parse(ends_at)
	s_b = p_b.time()
	s_e = p_e.time()
	today = datetime.date.today()
	d_start = datetime.datetime.combine(today, s_b)
	d_end = datetime.datetime.combine(today, s_e)
	return ( d_end - d_start )

#parses JSON time to datetime
def getdatetime(datestring):
	return parser.parse(datestring)


def notify(args, tok, chat_id):
	num_string = args[1][1:]
	try:
		num = int(num_string)
	except:
		return "Error {} is not a valid integer".format(num_string)
	if num <= 1 or num > 4320:
		return "Error {} is not an integer between 1 and 4320".format(num_string)
	response = requests.get("https://api.intra.42.fr/v2/events/{}".format(args[0]), tok)
	if response.status_code != 200:
		return "Sorry could not request the event\nthis could be because you are trying to access an event you are not authorized to or because\the api is down. If none of that is the case, please report the issue to jsiller\n"
	json = response.json()
	msg = notifydb.check_entrys(chat_id=chat_id, event_id=args[0], num=num)
	if msg != 0:
		return msg
	utc = pytz.UTC
	notify_time = getdatetime(json['begin_at']) - datetime.timedelta(seconds=num + 600)
	now_time = datetime.datetime.now()
	now_time = utc.localize(now_time)
	if (notify_time < now_time):
		return "Sorry I'm not a time machine"
	notifydb.insert_notification(chat_id, notify_time, json['id'], getdatetime(json['begin_at']), json['name'], num)
	return "successfully created notfication"
	

def event_args(args, tok, chat_id):
	if len(args) == 1:
		try:
			num = int(args[0])
		except:
			msg = "Error {} is not a valid int".format(args[0])
			return msg
		response = requests.get("https://api.intra.42.fr/v2/events/{}".format(args[0]), tok)
		if response.status_code != 200:
			msg = "Sorry could not request the event\nthis could be because you are trying to access an event you are not authorized to or because the api is down. If none of that is the case, please report the issue to jsiller\n"
		else:
			json = response.json()
			msg = "You accessed the event {name} with the id {id}\n".format(name=json['name'], id=json['id'])
			msg += "\nDescription: {}\n".format(json['description'])
			msg += "\nLocation: {}\n".format(json['location'])
			msg += "\nBegins at: {}\n".format(json['begin_at'])
			msg += "\nDuration in hours: {}\n".format(caluclate_duration(json['begin_at'], json['end_at']))
			msg += "\nDo you want to get notified 30 minutes before the event?\n\t\trun \"/events {} N30\"\n".format(args[0])
			msg += "\t\tyou can change the time to any time betweeen 1 and 4320\n"
			msg += "\t\tto get notified one day before the event use 1440\n"
			# msg += "\nDo you want to subscribe to the event?\n\t\trun \"/events {} S\" -- not working (yet)\n".format(args[0])
			msg += "\nDo you want to add the event to your calender?\n\t\trun \"/events {} C\"\n".format(args[0])
	elif len(args) == 2:
		if args[1] == 'S':
			# print("DEBUG")
			# data = {}

			# data['event_id'] = str(9130)
			# data['user_id'] = str(83428)
			# data2 = {}
			# data2['events_user'] = data
			# print(data2)
			# header = { }
			# header['Authorization'] = 'Bearer ' + str(tok['access_token'])
			# header["Content-Type"] = 'application/json'
			# print(header)
			# response = requests.post("https://api.intra.42.fr/v2/events_users",  headers=header, data=data2)
			# print(response.status_code)
			# print(response.json())
			return "this bot has no authorization to do this... :("
		elif args[1] == 'C':
			response = requests.get("https://api.intra.42.fr/v2/events/{}".format(args[0]), tok)
			if response.status_code != 200:
				msg = "Sorry could not request the event\nthis could be because you are trying to access an event you are not authorized to or because\the api is down. If none of that is the case, please report the issue to jsiller\n"
			json = response.json()
			cal = Calendar()
			event = Event()
			cal.add('method', 'PUBLISH')
			event.add('summary', json['name'])
			event.add('description', json['description'])
			event.add('location', json['location'])
			event.add('dtstart', getdatetime(json['begin_at']))
			event.add('dtend', getdatetime(json['end_at']))
			event.add('dstamp', getdatetime(json['end_at']))
			cal.add_component(event)
			return cal
		elif args[1][0] == 'N':
			msg = notify(args, tok, chat_id)
		else:
			msg = "Unknown instruction: {}".format(args[1])
	else:
		msg = "/events takes max. 2 arguements run /events EVENT_ID to get information about a specific event"
	return msg