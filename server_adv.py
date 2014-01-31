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
			datajson = self.request.recv(1024)
			if not datajson: continue
			data = json.loads(datajson)
			#Making new json object
			time = datetime.now().strftime("%Y-%m-%d %H:%M")
			outData = {'time':time, 'nick':data['nick'],'message':data['message']}
			outData = json.dumps(outData)
			if not outData: continue
			print datetime.now().strftime("%Y-%m-%d %H:%M") + ' ' +data['nick'] + ': ' + data['message']
			for i in clients:
				i.request.sendall(outData)

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

