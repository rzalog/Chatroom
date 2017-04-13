#!/usr/local/bin/python3

import sys
import threading
import util
from socket import *
from ChatObjects import *

username = str()
prompt = '> '
message_buffer = []

class ServerListenThread(threading.Thread):
	def __init__(self, sock):
		self.sock = sock
		threading.Thread.__init__(self)
	def run(self):
		while True:
			serv_response = recv_message(self.sock)
			handle_message(serv_response, self.sock)

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

	if serv_response.func == FUNC_ERROR:
		error_type, error_value = parse_error(serv_response)
		if error_type == ERROR_EXISTING_USER:
			print('Sorry, username "{}" already exists.'.format(error_value))
			return init_user(sock)
	else:
		return name

def handle_message(message, sock):
	if message.func == FUNC_SEND_MSG:
		handle_sent_msg(message)
	if message.func == FUNC_ERROR:
		handle_error(message, sock)

def handle_error(message, sock):
	error_type, error_value = parse_error(message)

def handle_sent_msg(message):
	print('Displaying messages...')
	disp_line = "{}: {}".format(message.user, message.body)
	message_buffer.append(disp_line)
	print_msg_buffer()

def print_msg_buffer():
	util.clear_screen()
	for line in message_buffer:
		print(line)
	print()
	print('{}> '.format(username), end='', flush=True)

def parse_error(message):
	return (message.body.splitlines()[0], message.body.splitlines()[1])

util.clear_screen()

client_sock = init_sock()
print('Connection successful.')

username = init_user(client_sock)

listen_thread = ServerListenThread(client_sock)
listen_thread.start()

while True:
	input_string = input()
	message = Message(username, FUNC_SEND_MSG, input_string)
	send_message(client_sock, message)

client_sock.close()
