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

SIZE = len(pickle.dumps(f'{0:0{HEADER}d}'))
BUFFER = int(math.pow(2, math.ceil(math.log(SIZE, 2)))) # smallest power of 2 >= SIZE


# UTILITY CLASS
class Client:

	def __init__(self, username):
		self.client = None 
		self.username = username


	def connect(self):
		'''
			DESC: connect to the server
			ARGS: self
			RETURN: None
		'''
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((HOST, PORT))
			print(f'Connected to {HOST}:{PORT}')
			self.client.send(pickle.dumps(self.username))

			thread = Thread(target=self.communicate, daemon=True)
			thread.start()
			self.send_messages()

		except socket.error as e:
			print(f'[ERROR] {e}')


	def send_messages(self):
		'''
			DESC: send message to the server
			ARGS: 
				message (str): message to be sent
			RETURN: None
		'''
		while True:
			message = input(f'{self.username} >> ')
			msg = pickle.dumps(message)
			header = f'{len(msg):0{HEADER}d}'

			self.client.send(pickle.dumps(header))
			time.sleep(0.1)
			self.client.send(msg)

			if message == '[quit]':
				break

		print('[BOT] >> You have left the chat')
		self.client.close()


	def receive_message(self, header):
		'''
			DESC: receive message from the server
			ARGS: 
				client (socket client): client from whom the message is received
				header (int): length of the message
			RETURN: msg (str): the decoded plaintext message
		'''
		chunk = b''

		while len(chunk) < header:
			packet = self.client.recv(BUFFER)
			chunk += packet 

		msg = pickle.loads(chunk[:header])
		return msg 


	def communicate(self):
		'''
			DESC: communicate with the server
			ARGS: self
			RETURN: none
		'''
		while True:
			packet = self.client.recv(BUFFER)
			header = int(pickle.loads(packet))

			msg = self.receive_message(header)
			print(f'\n{msg}\n{self.username} >> ', end="")