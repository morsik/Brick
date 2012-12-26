import select
import socket
import sys
import Queue

from ConnectionSocket import ConnectionSocket
from SignalHandler import signals
import settings

class ConnectionSocketServer(ConnectionSocket):
	def __init__(self):
		ConnectionSocket.__init__(self)

		self.connections = {}
		self.connection_inputs = []
		self.connection_outputs = []

		try:
			self.socket.bind((settings.HUB_HOST, settings.HUB_PORT))
		except socket.error as err:
			print("\033[1;33m%s\033[0m" % err)
			sys.exit(1)

		self.socket.listen(5)
	
	def pool(self):
		rlist, wlist, xlist = select.select(
			[self.socket] + self.connection_inputs,
			[self.socket] + self.connection_outputs,
			[self.socket] + self.connection_inputs,
		)

		for c in rlist:
			if c is self.socket:
				"""Incoming connection"""
				
				new_connection, new_address = c.accept()
				address = "%s:%s" % new_address
				print("[%s] BEGIN" % (address))
				c.setblocking(False)

				self.connection_inputs.append(new_connection)
				self.connections[address] = ConnectionSocket(use_socket=new_connection, queue=Queue.Queue())

				signals.emit('Connection::Connected', self.connections[address])
			else:
				"""Current connection"""

				address = "%s:%s" % c.getpeername()

				data = self.connections[address].recv()
				if data:
					self.connections[address].appendQueue(data)

					if self.connections[address].socket in self.connection_outputs:
						self.connection_outputs.append(self.connections[address].socket)

					signals.emit('Connection::DataReceived', self.connections[address], data)
				else:
					print("Closing %s after reading no data" % (address))

					if self.connections[address].socket in self.connection_outputs:
						self.connection_outputs.remove(self.connections[address].socket)
					self.connection_inputs.remove(self.connections[address].socket)
					self.connections[address].socket.close()

					del self.connections[address]

					signals.emit('Connection::Disconnected', address)

		for c in wlist:
			connection = ConnectionSocket(socket=c)

			try:
				next_msg = self.connections[connection.socket].queue.get_nowait()
			except Queue.Empty():
				print("Output queue for %s is empty!" % connection.socket.getpeername())
				self.connection_outputs.remove(connection.socket)
			else:
				connection.send(next_msg)

		for c in xlist:
			address = "%s:%s" % connection.socket.getpeername()

			print("Handling exceptional condition for %s!" % address)
			self.connection_inputs.remove(self.connections[address].socket)
			if self.connections[address].socket in self.connection_outputs:
				self.connection_outputs.remove(self.connections[address].socket)
			self.connections[address].socket.close()

			del self.connections[address]

		return True
