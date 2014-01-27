# -*- coding: utf-8 -*-
import SocketServer, json, select, sys
from datetime import datetime

clients = []
class CLientHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		print "Clients:", clients
		# Hent IP-adressen til klienten
		self.ip = self.client_address[0]
		clients.append(self)

		# Hent portnummeret til klienten
		self.port = self.client_address[1]
		print self.port

		# Si ifra at en ny klient har koblet til serveren
		print 'Client connected @' + self.ip + ':' + str(self.port)
		connIn = 0
		while True:
			data = self.request.recv(1014)
			#Already tried with BaseRequestHandler, SocketServer, but this works..
			'''while connIn in select.select(clients,[],[],0)[0]:
				print "HELLO FROM CONNIN"'''
			# Motta data fra klienten
			# Setter maks datastørrelse til 1kb
			if not data: break
			# Last inn JSON-objektet
			data = json.loads(data)

			# Si ifra at klienten har sendt en melding
			print datetime.now().strftime("%Y-%m-%d %H:%M") + ' ' + data['nick'] + ': ' + data['message']
			for i in clients:
				i.request.sendall(data['message'])
				#print "Sent message,", data['message'], "to:", data['nick']

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass


# Kjøres når programmet starter
if __name__ == "__main__":
	# Definer host og port for serveren
	HOST = 'localhost'
	PORT = 1337

	# Sett opp serveren
	server = ThreadedTCPServer((HOST, PORT), CLientHandler)

	# Aktiver serveren. Den vil kjøre til den avsluttes med Ctrl+C
	server.serve_forever()

