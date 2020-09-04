import os
import time
import math
import socket
import pickle 
from threading import Thread
from dotenv import load_dotenv

# loading the global variables
PATH = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(PATH)

HOST = socket.gethostbyname(os.getenv('HOST'))
PORT = int(os.getenv('PORT'))
HEADER = int(os.getenv('HEADER'))

SIZE = len(pickle.dumps(f'{0:0{HEADER}d}'))
BUFFER = int(math.pow(2, math.ceil(math.log(SIZE, 2)))) # smallest power of 2 >= SIZE


def client_connect(username):
	# try the socket connection
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((HOST, PORT))
		print(f'Connected to {HOST}:{PORT}')
		client.send(pickle.dumps(username))

		return client 
	except socket.error as e:
		print(f'[ERROR] {e}')


def recieve_messages(client, username):
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

				print(f'\n{msg}\n{username} >> ', end="")
				new_msg = True


def main():
	username = input('Enter your username: ')
	client = client_connect(username)
	thread = Thread(target=recieve_messages, args=(client, username), daemon=True)
	thread.start()	

	while True:
		message = input(f'{username} >> ')
		msg = pickle.dumps(message)
		header = f'{len(msg):0{HEADER}d}'

		client.send(pickle.dumps(header))
		time.sleep(0.1)
		client.send(msg)

		if message == '[quit]':
			client.close()
			break


if __name__ == '__main__':
	main()