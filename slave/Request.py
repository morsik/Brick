import socket

import Brick

waitfor = None

def Parse(message):
	global waitfor

	if Brick.DEBUG and message:
		print("\033[0;36mrecv\033[0m> %s" % (message))

	"""General problems"""
	if message == 'access denied':
		print("\033[1;31mAccess denied.\033[0m")
		return None
	elif message == 'request invalid':
		print("\033[1;33mInvalid request.\033[0m")
		return None

	data = message.split(' ')

	if not message:
		"""Authorize after fresh connection"""
		waitfor = 'auth_response'
		return "auth slave %s imslave!" % (socket.gethostname())

	else:
		if waitfor == 'auth_response':
			waitfor = None
			if data[0] == 'ok':
				print("Connected to \033[0;36m%s\033[0m \033[0;33m%s\033[0m at %s:%s" % (data[1], data[2], Brick.TCP_IP, Brick.TCP_PORT))
				return None
			elif message == 'fail':
				print("\033[1;33mAuthorization failed!\033[0m")
				return None

	return None
