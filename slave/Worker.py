import sys
from threading import Thread

import Brick

_working = False

def start_task(connection, cmdline):
	wt = Worker(connection, cmdline)
	wt.start()

class Worker(Thread):
	def __init__(self, connection, cmdline):
		self.connection = connection
		self.cmdline = cmdline
		Thread.__init__(self, name="Worker")

	def run(self):
		print("cmdline: \033[0;33m%s\033[0m" % self.cmdline)
		self.setWorking(True)

		import Backend.Generic
		Backend.Generic.BackendExecute(self.cmdline)

		self.setWorking(False)
		self.connection.send('task finished\n')

	def isFree(self):
		global _working
		if _working:
			return False
		return True

	def setWorking(self, isworking):
		global _working
		_working = isworking
