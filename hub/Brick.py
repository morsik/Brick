#!/usr/bin/env python2

import select
import sys
import socket
from time import sleep
import Client
import Request

TCP_IP = "0.0.0.0"
TCP_PORT = 6666
BUFFER_SIZE = 4096

connections = []

server = None

def main():
	global server

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		server.bind((TCP_IP, TCP_PORT))
	except socket.error as e:
		print("\033[1;33m%s\033[0m" % e)
		sys.exit(1)
	server.listen(5)

	queue = {}

	while True:
		rlist, wlist, xlist = select.select([server] + connections, [server] + connections, [])

		for c in rlist:
			if c is server:
				conn, address = c.accept()
				addr = "%s:%s" % address
				print("[%s] BEGIN" % (addr))
				conn.setblocking(0)
				connections.append(conn)
				queue[addr] = {
					'data' : "",
					'length' : None,
				}
			else:
				addr = "%s:%s" % (c.getpeername())
				data = c.recv(BUFFER_SIZE)
				if not data:
					del queue[addr]
					connections.remove(c)
					print("[%s] END" % (addr))
					Client.Remove(addr)
					break

				queue[addr]['data'] += data
				while True:
					if queue[addr]['length'] is None:
						if '\n' not in queue[addr]['data']:
							break
					message, queue[addr]['data'] = queue[addr]['data'].split('\n', 1)
					queue[addr]['length'] = None
					reply = Request.Parse(addr, message)
					c.send("%s\n" % (reply))

		sleep(0.01)

if __name__ == "__main__":
	try:
		print("Starting \033[0;36mBrick Hub\033[0m")
		main()
	except KeyboardInterrupt:
		print("\033[0GShutting down \033[0;36mBrick Hub\033[0m")
		server.close()
