#!/usr/bin/env python2

import select
import sys
import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 6666
BUFFER_SIZE = 4096

client = None

def main():
	global client

	connected = False

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect((TCP_IP, TCP_PORT))
	except socket.error as err:
		print("\033[1;31mCan't connect to %s:%s\033[0m: %s" % (TCP_IP, TCP_PORT, err[1]))
		return False

	while True:
		if not connected:
			client.send("auth slave %s imslave!\n" % socket.gethostname())
			data = client.recv(BUFFER_SIZE).strip()
			print("\033[0;36mdebug\033[0m> %s" % data)
			if data.split(' ')[0] == 'ok':
				print("Server version: %s" % data.split(' ', 1)[1])
				connected = True
			
		else:
			data = client.recv(BUFFER_SIZE).strip()
			print("\033[0;36mdebug\033[0m> %s\n" % data)
		

if __name__ == "__main__":
	try:
		print("Starting \033[0;33mBrick Slave\033[0m")
		main()
	except KeyboardInterrupt:
		print("\033[0GShutting down \033[0;33mBrick Slave\033[0m")
		client.close()
