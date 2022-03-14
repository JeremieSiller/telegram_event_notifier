import requests
from requests_oauthlib import OAuth2Session
import consts as c

#creates token
def authenticate(code):
	try:
		token = c.oauth.fetch_token(token_url=c.token_url, code=code, client_secret=c.secret)
	except:
		return -1
	return token

#takes an old_token and refreshes it to create a new one should be called at least every 2 hours
#maybe there is a cleaner way to solve this but the pyhton oauthlib library is really bad documented
#returns 1 on error and 0 on success
def	refresh_token(old_token):
	data = {
		'client_id': c.uid,
		'client_secret': c.secret,
		'refresh_token': old_token['refresh_token'],
		'grant_type': 'refresh_token',
	}
	response = requests.post(url=c.token_url, data=data)
	if (response.status_code != 200):
		return 1
	old_token['access_token'] = response.json()['access_token']
	old_token['expires_in'] = response.json()['expires_in']
	old_token['refresh_token'] = response.json()['refresh_token']
	old_token['created_at'] = response.json()['created_at']
	old_token['expires_at'] = (response.json()['expires_in'] + response.json()['created_at'])
	return 0