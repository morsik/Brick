import Client
import Task

def Parse(connection, message):
	addr = connection.remote_addr()
	print("%-21s | \033[0;33m%-12s\033[0m | %s" % (addr, Client.getByAddr(addr), message))
	data = message.strip().split(' ')
	try:
		isauth, client = Client.Authorized(addr)

		if not isauth:
			if data[0] == 'auth':
				if Client.Auth(addr, data[1], data[2], data[3]):
					connection.send('ok BrickHub 0.1')
					return
				else:
					connection.send('fail')
					return
			else:
				connection.send('access denied')
				return

		elif isauth == Client.CLIENT_ADMIN:
			if data[0] == 'list':
				if len(data) > 1:
					if data[1]:
						connection.send(Client.List([data[1]]))
						return
				else:
					connection.send(Client.List())
					return
			elif data[0] == 'task':
				if len(data) > 1:
					if data[1] == 'add':
						if len(data) > 2:
							Task.Add(client, data[2], ' '.join(data[3:]))
							return
					if data[1] == 'del':
						if len(data) > 2:
						 	Task.Del(data[2])
							return
					elif data[1] == 'list':
						connection.send(Task.List())
						return

		elif isauth == Client.CLIENT_SLAVE:
			if data[0] == 'task':
				if data[1] == 'list':
					connection.send(Task.List())
					return
				elif data[1] == 'get':
					task = Task.getWaitingTask(client)
					if task:
						connection.send(task)
					return
				elif data[1] == 'started':
					Task.setTask(Task.getTaskBySlaveAddr(addr), Task.STATE_WORKING)
					return
				elif data[1] == 'finished':
					Task.finishTask(Task.getTaskBySlaveAddr(addr))
					return
			connection.send('no actions')
			return

	except IndexError:
		pass

	connection.send('request invalid')
