import Client

def Parse(addr, message):
	print "[%s] %s" % (addr, message)
	data = message.strip().split(' ')
	try:
		isauth = Client.Authorized(addr)
		if not isauth:
			if data[0] == "auth":
				if Client.Auth(addr, data[1], data[2], data[3]):
					return "ok Brick 0.1"
				else:
					return "fail"
			else:
				return "access denied"

		elif isauth == Client.CLIENT_ADMIN:
			if data[0] == "list":
				if len(data) > 1:
					if data[1]:
						return Client.List([data[1]])
				else:
					return Client.List()

		elif isauth == Client.CLIENT_SLAVE:
			return "no actions"

	except IndexError:
		return "request invalid"
	return "request invalid"
