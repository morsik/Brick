CLIENT_ADMIN = 1
CLIENT_SLAVE = 2

admins = []

def Add(addr):
	admins.append(addr)
	print "\033[1;33madmin added [%s]\033[0m" % (addr)

def Remove(addr):
	try:
		admins.remove(addr)
		print "\033[1;33madmin removed [%s]\033[0m" % (addr)
	except ValueError:
		pass

def List():
	print "Connected Admins:"
	for addr in admins:
		print "  %s" % (addr)

def Auth(username, password):
	if username == "admin" and password == "1234":
		return {
			'clientType' : CLIENT_ADMIN,
		}

	return None

def Authorized(addr):
	if addr in admins:
		return True
	else:
		return False
