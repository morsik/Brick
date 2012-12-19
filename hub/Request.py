import Client
import Task

def Parse(addr, message):
	print("%-21s | \033[0;33m%-12s\033[0m | %s" % (addr, Client.getByAddr(addr), message))
	data = message.strip().split(' ')
	try:
		isauth, client = Client.Authorized(addr)
		if not isauth:
			if data[0] == 'auth':
				if Client.Auth(addr, data[1], data[2], data[3]):
					return 'ok BrickHub 0.1'
				else:
					return 'fail'
			else:
				return 'access denied'

		elif isauth == Client.CLIENT_ADMIN:
			if data[0] == 'list':
				if len(data) > 1:
					if data[1]:
						return Client.List([data[1]])
				else:
					return Client.List()
			elif data[0] == 'task':
				if len(data) > 1:
					if data[1] == 'add':
						if len(data) > 2:
							return Task.Add(client, data[2], ' '.join(data[3:]))
					if data[1] == 'del':
						if len(data) > 2:
							return Task.Del(data[2])
					elif data[1] == 'list':
						return Task.List()

		elif isauth == Client.CLIENT_SLAVE:
			if data[0] == 'task':
				if data[1] == 'list':
					return Task.List()
				elif data[1] == 'get':
					return Task.getWaitingTask(client)
				elif data[1] == 'started':
					return Task.setTask(Task.getTaskBySlaveAddr(addr), Task.STATE_WORKING)
				elif data[1] == 'finished':
					return Task.finishTask(Task.getTaskBySlaveAddr(addr))
			return 'no actions'

	except IndexError:
		return 'request invalid'

	return 'request invalid'
