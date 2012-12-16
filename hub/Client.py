import json

CLIENT_ADMIN = 1
CLIENT_SLAVE = 2

clients = []


def Add(c):
	clients.append(c)

	if c['type'] == CLIENT_ADMIN:
		print("\033[1;33madmin added [%s from %s]\033[0m" % (c['username'], c['address']))
	elif c['type'] == CLIENT_SLAVE:
		print("\033[1;33mslave added [%s from %s]\033[0m" % (c['hostname'], c['address']))

	return True


def Remove(addr):
	try:
		for c in clients:
			if c['address'] == addr:
				print("\033[1;33madmin removed [%s from %s]\033[0m" % (c['username'], c['address']))
				clients.remove(c)
	except ValueError:
		pass


def List(show = ['admins', 'slaves']):
	out = {}

	if 'admins' in show:
		out['admins'] = []
		for c in clients:
			if c['type'] == CLIENT_ADMIN:
				out['admins'].append(c)

	if 'slaves' in show:
		out['slaves'] = []
		for c in clients:
			if c['type'] == CLIENT_SLAVE:
				out['slaves'].append(c)

	return json.dumps(out)


def Auth(addr, client_type, clientname, password):
	if client_type == "adm":
		if clientname == "admin" and password == "1234":
			return Add({
				'type'     : CLIENT_ADMIN,
				'address'  : addr,
				'username' : clientname,
			})

	elif client_type == "slave":
		if password == "imslave!":
			return Add({
				'type'     : CLIENT_SLAVE,
				'address'  : addr,
				'hostname' : clientname,
			})

	return False


def Authorized(addr):
	for c in clients:
		if addr == c['address']:
			return c['type']

	return False
