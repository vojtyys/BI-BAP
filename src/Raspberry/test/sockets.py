#!/usr/bin/python3

import os
import sys
import time
import pyhouse

#Adresa testované jednotky
ADDR = 2

def fail():
    print("Test failed")
    sys.exit(0)

def commandFailed():
    print('Cannot send command')
    fail()
    
print('Starting test')
a = pyhouse.Device(1)

if(not a.reset()):
    print("Connection between devices cannot be established")
    fail()
    
print('Sockets should turn on')
if(not a.sendCmd('socket1', 'on')):
    commandFailed()
if(not a.sendCmd('socket2', 'on')):
    commandFailed()
if(not a.sendCmd('socket3', 'on')):
    commandFailed()
if(not a.sendCmd('socket4', 'on')):
    commandFailed()
    
time.sleep(5)

print('Sockets should turn off')
if(not a.sendCmd('socket1', 'off')):
    commandFailed()
if(not a.sendCmd('socket2', 'off')):
    commandFailed()
if(not a.sendCmd('socket3', 'off')):
    commandFailed()
if(not a.sendCmd('socket4', 'off')):
    commandFailed()
    
time.sleep(5)  

print('Time test - sockets should turn on after 10 s and turn off after another 5 s')
if(not a.sendCmd('socket1', 'timeon', 10)):
    commandFailed()
if(not a.sendCmd('socket2', 'timeon', 10)):
    commandFailed()
if(not a.sendCmd('socket3', 'timeon', 10)):
    commandFailed()
if(not a.sendCmd('socket4', 'timeon', 10)):
    commandFailed()  
    
if(not a.sendCmd('socket1', 'timeoff', 5)):
    commandFailed()
if(not a.sendCmd('socket2', 'timeoff', 5)):
    commandFailed()
if(not a.sendCmd('socket3', 'timeoff', 5)):
    commandFailed()
if(not a.sendCmd('socket4', 'timeoff', 5)):
    commandFailed()  
    
time.sleep(9)
print('Sockets should be on now')
time.sleep(4)
print('Sockets should be off now') 

print("Sockets test completed.")
exit(0)
