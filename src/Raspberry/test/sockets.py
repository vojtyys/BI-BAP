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
a = pyhouse.Device(ADDR)

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
    
if(not a.sendCmd('socket1', 'timeoff', 15)):
    commandFailed()
if(not a.sendCmd('socket2', 'timeoff', 15)):
    commandFailed()
if(not a.sendCmd('socket3', 'timeoff', 15)):
    commandFailed()
if(not a.sendCmd('socket4', 'timeoff', 15)):
    commandFailed()  
    
time.sleep(10)
print('Sockets should be on now')
time.sleep(5)
print('Sockets should be off now') 
time.sleep(1)
print("Sockets test completed.")
exit(0)
