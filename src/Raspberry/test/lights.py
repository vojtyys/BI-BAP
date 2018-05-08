#!/usr/bin/python3

import os
import sys
import time
import pyhouse

#Adresa testované jednotky
ADDR = 1

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
    
print('Light1 full on')
if(not a.sendCmd('light1', 'on')):
    commandFailed()

print('Light2 full on')
if(not a.sendCmd('light2', 'on')):
    commandFailed()
    
time.sleep(5)

print('Light1 full off')
if(not a.sendCmd('light1', 'off')):
    commandFailed()

print('Light2 full off')
if(not a.sendCmd('light2', 'off')):
    commandFailed()
    
time.sleep(5)

print('Light1 dim 10 - light should stay off')
if(not a.sendCmd('light1', 'dim', 10)):
    commandFailed()

print('Light2 dim 10 - light should stay off')
if(not a.sendCmd('light2', 'dim', 10)):
    commandFailed()
    
time.sleep(5)

print('Light1 on - light should turn on and set dim level 10')
if(not a.sendCmd('light1', 'on')):
    commandFailed()

print('Light2 on - light should turn on and set dim level 10')
if(not a.sendCmd('light2', 'on')):
    commandFailed()
    
time.sleep(5)

print('Light1 full off')
if(not a.sendCmd('light1', 'off')):
    commandFailed()

print('Light2 full off')
if(not a.sendCmd('light2', 'off')):
    commandFailed()
    
time.sleep(5)

print('Light1 time test - light should turn on after 10 s and turn off after another 5 s')
if(not a.sendCmd('light1', 'timeon', 10)):
    commandFailed()
if(not a.sendCmd('light1', 'timeoff', 15)):
    commandFailed()

print('Light2 time test - light should turn on after 10 s and turn off after another 5 s')
if(not a.sendCmd('light2', 'timeon', 10)):
    commandFailed()
if(not a.sendCmd('light2', 'timeoff', 15)):
    commandFailed()
    
time.sleep(10)
print('Lights should turn on now')
time.sleep(5)
print('Lights should turn off now')

time.sleep(5)
print('Autoon test - cover BH1750 sensor by hand, lights should turn on in 30 s')
if(not a.sendCmd('light1', 'autoon')):
    commandFailed()
if(not a.sendCmd('light2', 'autoon')):
    commandFailed()

time.sleep(30)
print('Lights should be turned on')
print("Lights test completed, try light buttons functionality.")
exit(0)
