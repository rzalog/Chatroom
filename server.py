#!/usr/local/Cellar/python3/3.5.2_1/bin/python3.5

import sys
from socket import *
from ChatObjects import *

active_client_socks = dict()
active_users = set()

def handle_message(message, client_sock):
	if message.func == "CREATE":
		return create_user(message, client_sock)

def create_user(message, client_sock):
	ret = bool()
	user = message.user
	if user not in active_users:
		print('Created user {}'.format(message.user))
		active_client_socks[client_sock] = user
		active_users.add(user)
		response = Message(USER_SERVER, FUNC_SEND_MSG, 'Welcome, {}!'.format(user))
		send_message(client_sock, response)
		ret = False
	else:
		print('Attempt to create duplicate user {}'.format(user))
		response_str = ERROR_EXISTING_USER + '\r\n' + user + '\r\n'
		response = Message(USER_SERVER, FUNC_ERROR, response_str)
		send_message(client_sock, response)
		ret = True
	return ret

def remove_user(client_sock):
	user = active_client_socks[client_sock]
	del active_client_socks[client_sock]
	active_users.remove(user)
	print('Removed user {}.'.format(user))

if len(sys.argv) < 2:
	print('Error: Port number required.')
	exit()

portno = int(sys.argv[1])
serv_sock = socket(AF_INET, SOCK_STREAM)

serv_sock.bind ( ('', portno) )
serv_sock.listen(1)

print('Server is listening.')

active_users.add('rzalog')

keep_connection_open = True
client_sock, client_addr = serv_sock.accept()

while keep_connection_open:
	client_msg = recv_message(client_sock)
	keep_connection_open = handle_message(client_msg, client_sock)

client_sock.close()