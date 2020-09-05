from utils import Client

if __name__ == '__main__':
	username = input('Enter your username: ')
	client = Client(username)
	client.connect()