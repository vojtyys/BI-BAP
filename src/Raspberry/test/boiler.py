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
    
print('Setting temperature to 80°C')
if(not a.sendCmd('boiler', 'temp', 40)):
    commandFailed()
    
time.sleep(5)

print('Turning on temperature tracking --- boiler should turn on in 30 s')
if(not a.sendCmd('boiler', 'on')):
    commandFailed()
    
time.sleep(30)
print('Boiler should be on now')
time.sleep(5)

print('Setting temperature to 0°C --- boiler should turn off in 30 s')

if(not a.sendCmd('boiler', 'temp', 0)):
    commandFailed()

time.sleep(30)
print('Boiler should be off now')
time.sleep(5)

print('Setting temperature to 80°C and turning off temperature tracking - boiler should NOT turn on in 30 s')

time.sleep(30)
print("Boiler test completed")
exit(0)
