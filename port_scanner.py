#!/bin/python3

import sys
import socket as skt
from datetime import datetime as dt

if len(sys.argv) == 2:
	target = skt.gethostbyname(sys.argv[1])
else:
	print("No argument found")
	print("Syntax: python3 port_scanner.py <ip>")
	
print("-"*50)
print("PORT SCANNER Scanning target {}".format(target))
print("Time Started: " + str(dt.now()))
print("-"*50)

skt.setdefaulttimeout(0.3	)

try:
	for port in range(50,85):
		s = skt.socket(skt.AF_INET,skt.SOCK_STREAM)
		result = s.connect_ex((target,port))
		if result == 0:
			print("Port {} is open.".format(port))
		s.close()
except KeyboardInterrupt:
	print("Exiting Program")
	sys.exit()
	
except skt.gaierror:
	print("IP address cannot be translated")
	sys.exit()
	
except skt.error:
	print("Couldn't establish socket connection")
	sys.exit()
