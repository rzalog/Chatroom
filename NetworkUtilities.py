from socket import *

def send_message(to_sock, message):
	'''
	Wrapper for socket sending, encodes for you
	'''
	sentBytes = to_sock.send(message.encode())
	return sentBytes

def recv_message(from_sock, buf_len):
	'''
	Wrapper for socet receiving, decodes for you
	'''
	recv = from_sock.recv(buf_len)
	return recv.decode()