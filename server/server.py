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


# GLOBAL VARIABLES
clients = {}


# try the socket connection
def server_connect():
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		server.bind((HOST, PORT))
		server.listen(CLIENT_LIMIT)
		print(f'Listening on {HOST}:{PORT}')

		return server 
	except socket.error as e:
		print(f'[ERROR] {e}')


# client connection
def connection(username, server):
	client = clients[username]

	new_msg = True
	header = 0
	packet = b''

	while True:
		chunk = client.recv(BUFFER)
		
		if new_msg:
			packet += chunk 
			header = int(pickle.loads(packet))

			packet = b''
			new_msg = False
		
		else:
			packet += chunk
			
			if header <= len(packet):
				msg = pickle.loads(packet[:header])
				packet = packet[header:]

				if msg == '[quit]':
					break

				msg = pickle.dumps(f'{username} >> {msg}')
				header = f'{len(msg):0{HEADER}d}'

				for key, value in clients.items():
					if key != username:
						value.send(pickle.dumps(header))
						time.sleep(0.1)
						value.send(msg)

				new_msg = True

	print(f'[{username}] has left the chat... Press F for respect')
	client.close()

	del clients[username]
	sys.exit()


# receive the client connections 		
def main():
	server = server_connect()

	while True:
		client, address = server.accept()
		print(f'Connection established from {address}')

		username = pickle.loads(client.recv(BUFFER))
		clients[username] = client
		print(f'{username} has joined the chat')

		thread = Thread(target=connection, args=(username, server), daemon=True)
		thread.start()


if __name__ == '__main__':
	main()