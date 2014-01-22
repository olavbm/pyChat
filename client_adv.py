# -*- coding: utf-8 -*-
import socket, json, select, sys

class Client(object):

	def __init__(self):
		# Initialiser en tilkobling
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def start(self, host, port):
		def isData():
			return select.select([sys.stdin], [], [], 0) ==	([sys.stdin], [], [])
		# Start tilkoblingen
		self.connection.connect((host, port))
		# Be brukeren om å skrive inn brukernavn
		nick = raw_input('name: ')
		data = {'nick':nick, 'message':" just connected"}
		data = json.dumps(data)
		self.send(data)
		connIn = 0
		while True:
			while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
				line = sys.stdin.readline()
				if len(line) < 1: continue
				if line:
					data = {'nick':nick, 'message':line}
					data = json.dumps(data)
					self.send(data)
					print "Sent", data,"successfully"
	#		while connIn in select.select([self.connection.recv(1024)], [], [], 0):
			while self.connection.recv(1024):
				print "Got here", connIn
				recievedData = connIn
				print recievedData
			connIn += 1
	def send(self, data):
		self.connection.send(data)


# Kjøres når programmet startes
if __name__ == "__main__":
	# Definer host og port for serveren
	HOST = 'localhost'
	PORT = 1337
	# Initialiser klienten
	client = Client()
	# Start klienten
	client.start(HOST, PORT)
