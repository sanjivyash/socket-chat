import sys
import os
import time
import math
import socket
import pickle 
from threading import Thread
from dotenv import load_dotenv


# GLOBAL CONSTANTS
PATH = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(PATH)

HOST = socket.gethostbyname(os.getenv('HOST'))
PORT = int(os.getenv('PORT'))
HEADER = int(os.getenv('HEADER'))
CLIENT_LIMIT = int(os.getenv('CLIENT_LIMIT'))

SIZE = len(pickle.dumps(f'{0:0{HEADER}d}'))
BUFFER = int(math.pow(2, math.ceil(math.log(SIZE, 2)))) # smallest power of 2 >= SIZE


# UTILITY CLASS
class Server:

	def __init__(self):
		self.clients = {}
		self.address = {}
		self.server = None


	def bind(self):
		'''
			DESC: create a server and bind to an IP
			ARGS: self
			RETURN: None
		'''
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			
			self.server.bind((HOST, PORT))
			self.server.listen(CLIENT_LIMIT)
			print(f'Listening on {HOST}:{PORT}')
 
		except socket.error as e:
			print(f'[ERROR] {e}')


	def receive_message(self, client, header):
		'''
			DESC: receive message from a client
			ARGS: 
				client (socket client): client from whom the message is received
				header (int): length of the message
			RETURN: msg (str): the decoded plaintext message
		'''
		chunk = b''

		while len(chunk) < header:
			packet = client.recv(BUFFER)
			chunk += packet 

		msg = pickle.loads(chunk[:header])
		return msg 


	def send_message(self, username, msg):
		'''
			DESC: relay messages to all clients
			ARGS: 
				msg (str): message to be sent 
				username (str): username of the sender of the message
			RETURN: None
		'''
		msg = pickle.dumps(f'{username} >> {msg}')
		header = f'{len(msg):0{HEADER}d}'

		for key, client in self.clients.items():
			if key != username:
				 client.send(pickle.dumps(header))
				 time.sleep(0.01)
				 client.send(msg)


	def communicate(self, username):
		'''
			DESC: communicate with a given client
			ARGS: 
				username (str): username to identify client
			RETURN: None 
		'''
		client = self.clients[username]

		while True:
			packet = client.recv(BUFFER)
			header = int(pickle.loads(packet))
			msg = self.receive_message(client, header)
			
			if msg == '[quit]':
				break	

			self.send_message(username, msg)

		del self.clients[username]
		
		self.send_message('[BOT]', f'[{username}] has left the chat... Press F for respect')
		print(f'Connection with {self.address[username]} terminated')
		client.close()
	
		del self.address[username]
		sys.exit()


	def connect(self):
		'''
			DESC: receive connections from different clients
			ARGS: self
			RETURN: None 
		'''
		while True:
			client, address = self.server.accept()
			print(f'Connection established from {address}')

			username = pickle.loads(client.recv(BUFFER))
			self.send_message('[BOT]', f'{username} has joined the chat')

			self.clients[username] = client
			self.address[username] = address

			thread = Thread(target=self.communicate, args=(username,), daemon=True)
			thread.start() 