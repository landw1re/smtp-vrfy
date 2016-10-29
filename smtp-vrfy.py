#!/usr/bin/env python

import socket
import sys
import argparse
import os

def check_ip(ip_address):
	ip = str(ip_address.strip())
	octets = ip.split('.')
	ip_invalid_msg = "{} is not a valid IPv4 IP address".format(ip)
	if len(octets) != 4:
		raise argparse.ArgumentTypeError(ip_invalid_msg)
		return False
	for octet in octets:
		if not octet.isdigit():
			raise argparse.ArgumentTypeError(ip_invalid_msg)
			return False
		i = int(octet)
		if i < 0 or i > 255:
			raise argparse.ArgumentTypeError(ip_invalid_msg)
			return False
	return ip

def check_file_exists(file):
	if(os.path.isfile(file)):
		return file
	else:
		no_file_exists_msg = "the file {} does not exist".format(file)
		raise argparse.ArgumentTypeError(no_file_exists_msg)
		return False

def verify_username(smtp_connection, username):
	# VRFY a user
	smtp_connection.send('VRFY ' + username + '\r\n')
	result = smtp_connection.recv(1024)
	print result

def open_smtp_connection(ip_address):
	# Create a Socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect to the Server
	con = s.connect((ip_address, 25))
	# Receive the banner
	banner = s.recv(1024)
	print "----- Connecting to Host {} -----".format(ip_address)
	print banner
	
	return s

def close_smtp_connection(smtp_connection):
	smtp_connection.close()

def iterate_usernames(ip_address, **kwargs):
	if('username' in kwargs):
		s_connect = open_smtp_connection(ip_address)
		verify_username(s_connect, kwargs['username'])
		close_smtp_connection(s_connect)
        elif('username_list' in kwargs):
		s_connect = open_smtp_connection(ip_address)
		with open(kwargs['username_list']) as f:
			for line in f:
				verify_username(s_connect, line.strip())
		close_smtp_connection(s_connect)


def main():

	parser = argparse.ArgumentParser(description='''Check a host for an open SMTP port
        and verify if a username exists on the mail server
        ''')
	parser.add_argument('-i', type=check_ip, dest="ip_address", metavar="<ip address>", 
        		help="valid IPv4 IP address")
	parser.add_argument('-u', dest="username", metavar="<username>", 
        		help="username to verify")
	parser.add_argument('--user-list', dest="user_file", metavar="<FILE>", type=check_file_exists, 
			help="file containing a list of usernames (1 username per line)")
	parser.add_argument('--ip-list', dest="ip_file", metavar="<FILE>", type=check_file_exists, 
			help="file containing a list of IP addresses (1 IP per line)")
	#parser.add_argument('-o', dest="out_file", metavar="<FILE>", type=argparse.FileType('w+'), 
	#		help="file to write output to")
	args = parser.parse_args()

	if(args.ip_address != None and args.ip_file != None):
		ip_invalid_option_msg = '''the -i option and --ip-list option cannot
					be used at the same time'''
		raise argparse.ArgumentTypeError(ip_invalid_option_msg)

	if(args.username != None and args.user_file != None):
                username_invalid_option_msg = '''the -u option and --user-list option cannot
                                        be used at the same time'''
                raise argparse.ArgumentTypeError(username_invalid_option_msg)

	
	if(args.ip_address != None):
		if(args.username != None):
			iterate_usernames(args.ip_address, username=args.username)
		elif(args.user_file != None):
			iterate_usernames(args.ip_address, username_list=args.user_file)
	elif(args.ip_file != None):
		with open(args.ip_file) as f:
                	for line in f:
                        	ip = check_ip(line)
				if(args.username != None):
					iterate_usernames(ip, username=args.username)
				elif(args.user_file != None):
					iterate_usernames(ip, username_list=args.user_file)


if __name__ == "__main__":
	main()

