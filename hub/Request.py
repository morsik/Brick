import Client

def Parse(addr, message):
	print "[%s] %s" % (addr, message)
	data = message.strip().split(' ')
	try:
		if not Client.Authorized(addr):
			if data[0] == "auth":
				if Client.Auth(addr, data[1], data[2], data[3]):
					return "ok"
				else:
					return "fail"
			else:
				return "access denied"

		else:
			if data[0] == "slave":
				if data[1] == "list":
					return "slaves: none"

				elif data[1] == "add":
					return "fail"

				elif data[1] == "del":
					return "fail"

			if data[0] == "list":
				if len(data) > 1:
					if data[1]:
						return Client.List([data[1]])
				else:
					return Client.List()

	except IndexError:
		return "request invalid"
	return "request invalid"
