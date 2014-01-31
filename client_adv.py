# -*- coding: utf-8 -*-
import sys, socket, json, select
class Client(object):

	def __init__(self):
		# Initialiser en tilkobling
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def start(self, host, port):
		def isData():
			return select.select([sys.stdin], [], [], 0) ==	([sys.stdin], [], [])
		self.connection.connect((host, port))
		nick = raw_input('name: ')
		data = {'nick':nick, 'message':" just connected"}
		data = json.dumps(data)
		self.send(data)
		inputData = [self.connection, sys.stdin]
		connIn = 0
		while True:
			inData, outData, ex = select.select(inputData, [], [])
			for s in inData:
				if s == sys.stdin:
					line = sys.stdin.readline()
					if len(line) < 1: continue
					if line:
						data = {'nick':nick, 'message':line[:len(line)-1]}
						data = json.dumps(data)
						self.send(data)
						print "Sent", data,"successfully"
						print connIn
				if inData == self.connection:
					data = self.connection.recv(1024)
					if data:
						dataJ = json.loads(data)
						print data['time'], " ", dataJ['nick'],":", data['message']
#			while connIn in select.select([0,self.connection], [],[],0)[0]:
#				print "I wanna get here, but never recieve anything!"
#				data = json.loads(connIn)
#				print "Data:",data
#			connIn += 1
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
