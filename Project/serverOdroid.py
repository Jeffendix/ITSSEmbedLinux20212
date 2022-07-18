#!/usr/bin/python3


"""
What needs to be done:
pip install dht11
Set DHT11 pin in TODO1 below

Write a script to run the whole setup & server at Odroid startup:
    ifconfig eth0 10.10.0.1
    udhcpd -f


Copy source:

Simple networking tutorial
https://www.tutorialspoint.com/python/python_networking.htm

DHT11 library:
https://github.com/shamelesscode/python-dht11-sensor-odroid

Socket documentation:
https://docs.python.org/3.0/library/socket.html
"""

import socket
import threading
import time # For sleep()
#NOT AVAILABLE: import IN # For setsockopt()

##import RPi.GPIO as GPIO
##import dht11

# initialize GPIO
##GPIO.setwarnings(False)
##GPIO.setmode(GPIO.BCM)
##GPIO.cleanup()

# TODO1:
# read data using pin 14
##instance = dht11.DHT11(pin = 14)

# Return "temperatureC humidity%"
# e.g.: "31.2C 80.8%"
# Return "Eerrorcode" on error
def readSensorData():
    ##result = instance.read()
    ##if result.is_valid:
    ##    return result.temperature + "C " + result.humidity + "%"
    ##return "E" + result.error_code 
    return "SENSOR_DATA"


# An array of connections
# that are hungrily waiting for 
# sensor outputs
connectionPool = []
addrPool = []
poolLock = threading.Lock()   # Protect connectionPool from racing
def listenNewConnections():
    s = socket.socket()
    
    # Bind this socket to the only available Odroid LAN port
    # Source: https://stackoverflow.com/questions/7221577/how-to-bind-socket-to-an-interface-in-python-socket-so-bindtodevice-missing
    #IN_SO_BINDTODEVICE = 25 # Patch for missing import IN  
    #s.setsockopt(socket.SOL_SOCKET, IN_SO_BINDTODEVICE, str("eth0" + '\0').encode('utf-8'))

    # Bind to ALL interfaces (Odroid has only eth0, sadly)
    ODROID_SERVER_IP = ''
    ODROID_SERVER_PORT = 1211
    s.bind((ODROID_SERVER_IP, ODROID_SERVER_PORT))
    s.listen(10)

    while True:
        c, addr = s.accept()
        print(str(addr) + " joined")
        poolLock.acquire()
        connectionPool.append(c)
        addrPool.append(addr)
        poolLock.release()
        

def periodicallySendSensorOutput():
    while True:
        poolLock.acquire()

        sensorData = readSensorData()
        if sensorData[0] == "E":
            print("Read error: " + sensorData[1:] + ". Retrying...")

        else:
            i = 0 # A clumsy way to determine dead connections
            try:
                for j in range(0, len(connectionPool)):
                    i = j
                    connectionPool[i].sendall(bytes(sensorData, 'utf-8'))

            except:
                print("Lost connection to " + str(addrPool[i]))
                connectionPool.pop(i)
                addrPool.pop(i)

            poolLock.release()

            if len(connectionPool) > 0:
                print("Sensor output has been sent to someone.")

        # A website tells me sensor can only be read every 2s 
        time.sleep(2.1) 


#<<< MAIN EXECUTION POINT >>>

print("Odroid server booted!")

# Create a separate thread to listen for new connections
LNC = threading.Thread(target=listenNewConnections)
LNC.start()

periodicallySendSensorOutput()
