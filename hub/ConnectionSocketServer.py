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
		self.connection_inputs = [self.socket]
		self.connection_outputs = []
		self.message_queues = {}

		try:
			self.socket.bind((settings.HUB_HOST, settings.HUB_PORT))
		except socket.error as err:
			print("\033[1;33m%s\033[0m" % err)
			sys.exit(1)

		self.socket.listen(5)
	
	def pool(self):
		readable, writable, exception = select.select(
			self.connection_inputs,
			self.connection_outputs,
			self.connection_inputs,
		)

		for s in readable:
			if s is self.socket:
				"""Incoming connection"""
				
				new_connection, new_address = s.accept()
				address = "%s:%s" % new_address
				print("[%s] BEGIN" % (address))
				s.setblocking(False)

				self.connection_inputs.append(new_connection)
				self.connections[address] = ConnectionSocket(use_socket=new_connection)
				self.message_queues[new_connection] = Queue.Queue()

				signals.emit('Connection::Connected', self.connections[address])
			else:
				"""Current connection"""

				address = "%s:%s" % s.getpeername()

				data = self.connections[address].recv()
				if data:
					self.message_queues[s].put(data)

					if s not in self.connection_outputs:
						self.connection_outputs.append(s)

					signals.emit('Connection::DataReceived', self.connections[address], data)
				else:
					print("Closing %s after reading no data" % (address))

					if s in self.connection_outputs:
						self.connection_outputs.remove(s)
						writable.remove(s)

					self.connection_inputs.remove(self.connections[address].socket)
					self.connections[address].socket.close()

					del self.message_queues[s]
					del self.connections[address]

					signals.emit('Connection::Disconnected', address)

		for s in writable:
			try:
				next_msg = self.message_queues[s].get_nowait()
			except Queue.Empty:
				address = "%s:%s" % s.getpeername()
				print("Output queue for %s is empty!" % address)
				self.connection_outputs.remove(s)
			else:
				print("XXX: %s" % next_msg)
				address = "%s:%s" % s.getpeername()
				print next_msg
				#self.connections[address].send(next_msg)

		for s in exception:
			address = "%s:%s" % connection.socket.getpeername()

			print("Handling exceptional condition for %s!" % address)
			self.connection_inputs.remove(s)
			if s in self.connection_outputs:
				self.connection_outputs.remove(s)
			self.connections[address].socket.close()

			del self.connections[address]

		return True
