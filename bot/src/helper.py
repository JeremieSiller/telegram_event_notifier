import consts as c
import time

#checks if token expires in next 5 minutes or is already expires. Return 0 if token is valid, 1 if not
def is_token_expired(token):
	s = time.time()
	if token['expires_at'] - s < 3000:
		return 1
	return 0