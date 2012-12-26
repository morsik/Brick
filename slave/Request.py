import socket
import json

import Brick
import Worker

waitfor = None

def Parse(conn, message):
	global waitfor

	if Brick.DEBUG and message:
		print("\033[0;36mrecv\033[0m> \033[0;33m%s\033[0m" % (message))

	"""General problems"""
	if message == 'access denied':
		print("\033[1;31mAccess denied.\033[0m")
		return None
	elif message == 'request invalid':
		print("\033[1;33mInvalid request.\033[0m")
		return None
	elif message == 'no actions':
		print("\033[1;33mNo actions.\033[0m")
		return None
	elif message == 'False' or message == 'True' or message == 'None':
		return None

	if not message:
		"""Authorize after fresh connection"""
		waitfor = 'auth_response'
		return "auth slave %s imslave!" % (socket.gethostname())

	else:
		if waitfor == 'auth_response':
			data = message.split(' ')

			waitfor = None
			if data[0] == 'ok':
				print("Connected to \033[0;36m%s\033[0m \033[0;33m%s\033[0m at %s:%s" % (data[1], data[2], Brick.TCP_IP, Brick.TCP_PORT))
				return 'task get'
			elif message == 'fail':
				print("\033[1;33mAuthorization failed!\033[0m")
				return None
		else:
			"""We're not waiting for something specific?"""
			"""Assume it's json going from Hub"""

			data = json.loads(message)
			if 'tasklist' in data:
				if Worker.isFree():
					return 'task get'
				else:
					return 'fail'
			elif 'task' in data:
				print("Starting task \033[0;36m%s\033[0m" % data['task']['name'])
				conn.send('task started\n')
				ret = Worker.start_task(conn, data['task']['cmd'])

	return None
