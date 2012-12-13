import Client

def Parse(addr, message):
	print "[%s] %s" % (addr, message)
	data = message.strip().split(' ')
	try:
		if not Client.Authorized(addr):
			if data[0] == "auth":
				authdata = Client.Auth(data[1], data[2])
				if authdata:
					Client.Add(addr)
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

	except IndexError:
		return "request invalid"
	return "request invalid"
