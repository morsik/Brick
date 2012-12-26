import json

import Client

tasks = []

STATE_BROKEN = -1
STATE_WAITING = 0
STATE_PULLED = 1
STATE_WORKING = 2

def Add(client, name, cmd):
	for t in tasks:
		if name == t['name']:
			return False

	tasks.append({
		'name' : name,
		'cmd' : cmd,
		'state' : STATE_WAITING,
		'slave' : None,
	})

	for c in Client.clients:
		if c['type'] == Client.CLIENT_SLAVE:
			d = getWaitingTask(c)
			if d:
				c['conn'].send("%s" % d)
#			Client.SendToAll(getWaitingTask(c), ['slaves'])
	return True

def Delete(name):
	return False

def List():
	return json.dumps({'tasklist' : tasks})

def finishTask(task):
	for t in tasks:
		if t['name'] == task:
			Client.setState(t['slave']['address'], STATE_WAITING)
			tasks.remove(t)
			return True
	return False

def getWaitingTask(slave):
	if slave['state'] > STATE_WAITING:
		return False

	for t in tasks:
		if t['state'] <= STATE_WAITING:
			t['state'] = STATE_PULLED
			t['slave'] = {
				'hostname' : slave['hostname'],
				'address' : slave['address'],
			}
			slave['state'] = STATE_PULLED

			return json.dumps({
				'task': {
					'name' : t['name'],
					'cmd' : t['cmd'],
				},
			})
	return False

def setTask(task, work_state):
	for t in tasks:
		if t['name'] == task:
			t['state'] = work_state
			if work_state == STATE_BROKEN:
				t['slave'] = None
			return True
	return False

def getTaskBySlaveAddr(addr):
	for t in tasks:
		if t['slave'] and 'address' in t['slave']:
			if t['slave']['address'] == addr:
				return t['name']
	return False
