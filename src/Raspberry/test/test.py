#!/usr/bin/python3

import os
import sys
import time
import pyhouse

a = pyhouse.Device(1)
b = pyhouse.Device(2)
a.reset()
b.reset()

a.sendCmd('light1', 'on')
time.sleep(5)
a.sendCmd('light1', 'off')
time.sleep(5)
a.sendCmd('light1', 'dim', 1)
a.sendCmd('light1', 'dim', 50)
a.sendCmd('light1', 'on')
b.sendCmd('socket1', 'on')
b.sendCmd('window', 'open')
time.sleep(5)
b.sendCmd('socket1', 'off')
b.sendCmd('boiler', 'temp', 30)
b.sendCmd('boiler', 'on')
a.sendCmd('light1', 'off')
time.sleep(45)
b.sendCmd('boiler', 'temp', 0)

    

	



print('\nTerminating program...\n')
exit(0)