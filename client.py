#!/usr/local/Cellar/python3/3.5.2_1/bin/python3.5

import sys
from socket import *
from ChatObjects import *

def init_sock():
	if (len(sys.argv)) < 3:
		print("Error: Server name and port number required.")
		exit()
	server_name = sys.argv[1]
	portno = int(sys.argv[2])
	client_sock = socket(AF_INET, SOCK_STREAM)
	client_sock.connect( (server_name, portno) )
	return client_sock

def init_user(sock):
	name = input("Enter username: ")
	init_user_msg = Message(name, FUNC_CREATE_USER)
	send_message(client_sock, init_user_msg)
	serv_response = recv_message(client_sock)
	handle_message(serv_response, client_sock)

def handle_message(message, sock):
	if message.func == FUNC_SEND_MSG:
		print_msg(message)
	if message.func == FUNC_ERROR:
		handle_error(message, sock)

def handle_error(message, sock):
	error_type = message.body.splitlines()[0]
	error_value = message.body.splitlines()[1]
	if error_type == ERROR_EXISTING_USER:
		print('Sorry, username "{}" is already taken'.format(error_value))
		init_user(sock)

def print_msg(message):
	print("{}: {}".format(message.user, message.body))



client_sock = init_sock()
print('Connection successful.')

init_user(client_sock)

client_sock.close()
