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
    
print('Window should open now, press open limit switch to stop it')
if(not a.sendCmd('window', 'open')):
    commandFailed()
    
time.sleep(15)

print('Window should close now, press closed limit switch to stop it')
if(not a.sendCmd('window', 'close')):
    commandFailed()
    
time.sleep(15)

print('Testing changing direction - this will send open command and close command few seconds after')
if(not a.sendCmd('window', 'open')):
    commandFailed()
time.sleep(5)
if(not a.sendCmd('window', 'close')):
    commandFailed()

time.sleep(5)
print('Now system will change direction from closing to opening')
time.sleep(5)
if(not a.sendCmd('window', 'open')):
    commandFailed()

print('Test of limits') 
print('Open limit test')   
print('Please press and hold open limit switch, open command will be send in 10 s, it should do nothing')

time.sleep(10)

if(not a.sendCmd('window', 'open')):
    commandFailed()
    
time.sleep(5)

print('Close limit test')
print('Please press and hold close limit switch, close command will be send in 10 s, it should do nothing')

time.sleep(10)
if(not a.sendCmd('window', 'close')):
    commandFailed() 
    
time.sleep(5)
print('Try window buttons now')
time.sleep(1)
print("Window test completed")
exit(0)
