#!/usr/bin/env python2

import select
import sys
import socket
from time import sleep
import Request

TCP_IP = "127.0.0.1"
TCP_PORT = 6666
BUFFER_SIZE = 4096

client = None
connected = None

def connect():
	global client, connected
	try:
		if connected == False:
			sleep(1)
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((TCP_IP, TCP_PORT))
		connected = True
	except socket.error as err:
		client = None
		if connected or connected == None:
			print("\033[1;31mCan't connect to %s:%s\033[0m: %s" % (TCP_IP, TCP_PORT, err[1]))
			connected = False


def main():
	global client, connected

	data = ""
	tosend = ""

	while True:
		try:
			if client:
				tosend = Request.Parse(data)
				if tosend:
					client.send(tosend, 4096)

				data = client.recv(BUFFER_SIZE).strip()
			else:
				if connected or connected == None:
					print("Not connected. Connecting. Autoreconnect every 1 second")
				connect()

		except socket.error as err:
			print("\033[1;31mConnection to %s:%s failed\033[0m: %s" % (TCP_IP, TCP_PORT, err[1]))
			connected = False
			connect()


if __name__ == "__main__":
	try:
		print("Starting \033[0;33mBrick Slave\033[0m")
		main()
	except KeyboardInterrupt:
		print("\033[0GShutting down \033[0;33mBrick Slave\033[0m")
		if client:
			client.close()
