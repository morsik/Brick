#!/usr/bin/env python2

import select
import sys
import socket
from time import sleep

import Client
import Request
from ConnectionSocketServer import ConnectionSocketServer
from SignalHandler import signals

def main():
	server = ConnectionSocketServer()

	signals.connect('Connection::Connected', Client.Add)
	signals.connect('Connection::Disconnected', Client.Remove)
	signals.connect('Connection::DataReceived', Request.Parse)

	while server.pool():
		sleep(0.01)

if __name__ == "__main__":
	try:
		print("Starting \033[0;36mBrick Hub\033[0m")
		main()
	except KeyboardInterrupt:
		print("\033[0GShutting down \033[0;36mBrick Hub\033[0m")
		server.close()
