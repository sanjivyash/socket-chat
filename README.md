# Command Line Chat App

This is a command line application that allows a common chat platform between multiple users

## Installation and Setup

The following snippet should set everything up:
```
git clone https://github.com/sanjivyash/socket-chat.git
cd socket-chat
mkdir config
touch config/.env
```

The ```config/.env``` file has to have the following constants:
- ```HOST```        : The name of the host where the server is set up
- ```PORT```        : The port where the server is hosted on the ```HOST```
- ```HEADER```      : The number of digits in the length of the longest message you can possibly send
- ```CLIENT_LIMIT```: The maximum number of clients you want to connect to the server simultaneously

Inside the development environment, I used the following file:  
```
HOST=localhost
PORT=2304
HEADER=4
CLIENT_LIMIT=5
```

## Usage

Run the server file first with ```python server/server.py```. If no error is displayed and the server is established, you can create as many terminals (or cmd) as the number of clients you want to have.

Now, run each client file with ```python client/client,py``` and input a unique username for each client. Your chat app has been set up. Any message that is sent by one client is received by all other clients.

## Future Plans

I plan to make the UI cleaner by mounting this command line server on a ```Flask``` app, but I am not too fond of frontend, so that plan might take a while.  
