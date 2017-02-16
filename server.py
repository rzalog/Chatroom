#!/usr/local/Cellar/python3/3.5.2_1/bin/python3.5

import sys
import threading
import select
from socket import *
from ChatObjects import *

client_socks = []
active_client_socks = dict()
active_users = set()

class AcceptNewClientsThread(threading.Thread):
	def __init__(self, client_socks):
		self.client_socks = client_socks
		threading.Thread.__init__(self)
	def run(self):
		while True:
			client_sock, client_addr = serv_sock.accept()
			client_socks.append(client_sock)

def handle_message(message, client_sock):
	if message == 0:
		#remove_user(client_sock)
		return
	elif message.func == FUNC_CREATE_USER:
		create_user(message, client_sock)
	elif message.func == FUNC_SEND_MSG:
		print("we got a sent message")
		recv_sent_message(message)

def create_user(message, client_sock):
	user = message.user
	if user not in active_users:
		print('Created user {}'.format(message.user))
		active_client_socks[client_sock] = user
		active_users.add(user)
		response = Message(USER_SERVER, FUNC_SEND_MSG, 'Welcome, {}!'.format(user))
		send_message(client_sock, response)
	else:
		print('Attempt to create duplicate user {}'.format(user))
		response_str = ERROR_EXISTING_USER + '\r\n' + user + '\r\n'
		response = Message(USER_SERVER, FUNC_ERROR, response_str)
		send_message(client_sock, response)

def recv_sent_message(message):
	for client_sock in client_socks:
		print('Sent message to {}'.format(active_client_socks[client_sock]))
		send_message(client_sock, message)

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
serv_sock.listen(10)

print('Server is listening.')
accept_new_clients_thread = AcceptNewClientsThread(client_socks)
accept_new_clients_thread.start()

active_users.add('rzalog')

while True:
	read_socks, write_socks, error_socks = select.select(client_socks,
		client_socks, client_socks, 0)
	for sock in read_socks:
		message = recv_message(sock)
		handle_message(message, sock)

client_sock.close()