import consts as c
import requests
import dateutil.parser as dp
import datetime

#not correct when event is for more than a day
def caluclate_duration(begins_at, ends_at):
	p_b = dp.parse(begins_at)
	p_e = dp.parse(ends_at)
	print(p_b)
	print(p_e)
	s_b = p_b.time()
	s_e = p_e.time()
	today = datetime.date.today()
	d_start = datetime.datetime.combine(today, s_b)
	d_end = datetime.datetime.combine(today, s_e)
	print(d_start)
	print(d_end)
	return ( d_end - d_start )

def event_args(args, tok):
	if len(args) == 1:
		response = requests.get("https://api.intra.42.fr/v2/events/{}".format(args[0]), tok)
		if response.status_code != 200:
			msg = "Sorry could not request the event\nthis could be because you are trying to access an event you are not authorized to or because\the api is down. If none of that is the case, please report the issue to jsiller\n"
		else:
			json = response.json()
			msg = "You accessed the event {name} with the id {id}\n".format(name=json['name'], id=json['id'])
			msg += "\nDescription: {}\n".format(json['description'])
			print(json['begin_at'])
			print(json['end_at'])
			msg += "\nLocation: {}\n".format(json['location'])
			msg += "\nBegins at: {}\n".format(json['begin_at'])
			msg += "\nDuration in hours: {}\n".format(caluclate_duration(json['begin_at'], json['end_at']))
			msg += "\nDo you want to get notified 30 minutes before the event?\n\t\trun \"/events {} N30\"\n".format(args[0])
			msg += "\t\tyou can change the time to any time betweeen 1 and 4320\n"
			msg += "\t\tto get notified one day before the event use 1440\n"
			msg += "\nDo you want to subscribe to the event?\n\t\trun \"/events {} S\"\n".format(args[0])
			msg += "\nDo you want add the event to your calender?\n\t\trun \"/events {} C\"\n".format(args[0])
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
			msg = "Calendly is not implemented yet"
		elif args[1][0] == 'N':
			msg = "Notifications are not implemented yet\n"
	elif len(args) >= 2:
		msg = "/events takes max. 2 arguements run /events EVENT_ID to get infors about a specific event"
	return msg