#!/usr/bin/python3

"""
Copied from https://www.tutorialspoint.com/python/python_networking.htm
"""
import socket
import time

#<<< MAIN EXECUTION POINT >>>

s = socket.socket()
ODROID_SERVER = "192.168.2.2"
#ODROID_SERVER = "127.0.0.1"
ODROID_PORT = 1211 


print("Connecting to " + ODROID_SERVER + ":" + str(ODROID_PORT))
s.connect((ODROID_SERVER, ODROID_PORT))

print("Connected!")
while True:
    msg = s.recv(1024)
    if msg != '':
        print(str(msg))
    time.sleep(1)
