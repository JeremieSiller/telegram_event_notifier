from urllib import response
import requests
from requests_oauthlib import OAuth2Session

#takes an old_token and refreshes it to create a new one should be called at least every 2 hours
#maybe there is a cleaner way to solve this but the pyhton oauthlib library is really bad documented
def	refresh_token(old_token, uid, secret):
	data = {
		'client_id': uid,
		'client_secret': secret,
		'refresh_token': old_token['refresh_token'],
		'grant_type': 'refresh_token',
	}
	response = requests.post(url='https://api.intra.42.fr/oauth/token', data=data)
	if (response.status_code != 200):
		return -1
	print(response.content)
	old_token['access_token'] = response.json()['access_token']
	old_token['expires_in'] = response.json()['expires_in']
	old_token['refresh_token'] = response.json()['refresh_token']
	old_token['created_at'] = response.json()['created_at']
	old_token['expires_at'] = (response.json()['expires_in'] + response.json()['created_at'])
	print(old_token['expires_at'])
	print(type(old_token['created_at']))
	return 0

