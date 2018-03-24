#!/usr/bin/python3

import time
import serial
import RPi.GPIO as GPIO
import crcmod

cmds = {'light' : {'cmd'        : 1,
		   
		   'on'         : {'par'       : False,
			           'time'      : False,
			           'cmd'       : 0},
		   
		   'off'        : {'par'       : False,
			           'time'      : False,
			           'cmd'       : 1},
		   
		   'dim'        : {'par'       : True,
			           'time'      : False,
			           'cmd'       : 2},
		   
		   'timeon'     : {'par'       : True,
				   'time'      : True,
				   'cmd'       : 3},
	
                   'timeoff'    : {'par'       : True,
				   'time'      : True,
				   'cmd'       : 4}},
	
       	'socket' : {'cmd'       : 2,
		    
		    'on'        : {'par'       : False,
			           'time'      : False,
			           'cmd'       : 0},
		    
		    'off'       : {'par'       : False,
			           'time'      : False,
			           'cmd'       : 1}},
	
	'boiler' : {'cmd'       : 3,
		    
		    'temp'      : {'par'       : True,
			           'time'      : False,
			           'cmd'       : 0}},
	
	'window' : {'cmd'       : 4,
		    
		    'open'      : {'par'       : False,
				   'time'      : False,
				   'cmd'       : 0},
		    
		    'close'     : {'par'       : False,
				   'time'      : False,
				   'cmd'       : 1}},
	
	'led'    : {'cmd'       : 5,
		    
		    'on'        : {'par'       : False,
				   'time'      : False,
				   'cmd'       : 0},
		    
		    'off'       : {'par'       : False,
				   'time'      : False,
				   'cmd'       : 1}}
       }

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)

class RS485:
	def __init__(self, OEPin, baudrate, timeout):
		self.__ser = serial.Serial('/dev/ttyS0')
		self.__ser.baudrate = baudrate
		self.__ser.timeout = timeout
		self.__OE = OEPin
		
	
	def sendData(self, data):
		GPIO.output(self.__OE, GPIO.HIGH)
		self.__ser.write(data)
		self.__ser.flush()
		GPIO.output(self.__OE, GPIO.LOW)
		
	def getData(self, cnt):
		data = self.__ser.read(cnt)
		return data


crc16 = crcmod.mkCrcFun(0x11021, 0xffff, False, 0x0000)

	
def getCrc(data):
	crc = crc16(data)
	crc = crc.to_bytes(2, 'big')
	return crc


def checkCrc(data):
	crc = getCrc(data[0:6])
	tmp = data[6:]
	if (tmp == crc):
		return True
	return False


class Device:
	def __init__(self, addr):
		self.__cnt = 0
		self.__addr = addr
		self.__ser = RS485(12, 9600, 1)
		self.__cmds = {}
	
		
	def sendCmd(self,dev, func=None, param=None):
		if (dev != 'reset'):
			if (not self.__checkCmd(dev, func, param)):                         
				print('Device, function or parameter was not recognized.')
				return
	
			data = self.__addr.to_bytes(1, 'big') + self.__cnt.to_bytes(1, 'big') + self.__cmds[dev]['cmd'].to_bytes(1, 'big') + self.__cmds[dev][func]['cmd'].to_bytes(1, 'big')
			if (self.__hasParam(dev, func)):                                                    
				if (self.__hasTimeParam(dev, func)):                                        
					data = data + bytes.fromhex('00 00')                                   #TODO
				else:
					data = data + param.to_bytes(1, 'big') + bytes.fromhex('00')		
			else:
				data = data + bytes.fromhex('00 00')
		else:
			data = self.__addr.to_bytes(1, 'big') + bytes.fromhex('00 00 00 00 00')
		data = data + getCrc(data)
	
		print("Sending cmd: ", end='')
		print(data)
		self.__ser.sendData(data)
	
		attempts = 10
		while(True):
                    if(attempts == 0):
                        print('Error: cannot send CMD: ', end='')
                        print(dev)
                        break
	
                    if (not self.__checkAck()):     
                        print('Sending CMD again: ' + str(data))
                        self.__ser.sendData(data)
                        attempts = attempts - 1
                    else:
                        self.__cnt = (self.__cnt + 1) % 256
                        break
			
	def addCmd(self, cmd):
		if (cmd not in cmds):
			print('Unknown command ' + cmd)
			return
		self.__cmds[cmd] = cmds[cmd]
	
	def __checkAck(self):		
		expectedAck = bytes.fromhex('00') + self.__cnt.to_bytes(1, 'big') + bytes.fromhex('00') + self.__addr.to_bytes(1, 'big') + bytes.fromhex('00 00')	
		expectedAck = expectedAck + getCrc(expectedAck)
		
		print('Waiting for ACK')
		ack = self.__ser.getData(7)
		print('Got: ' + str(ack))
		
		if (ack == expectedAck):
			print('ACK OK')
			return True
		else:
			print('Incorrect ACK, expected: ' + str(expectedAck))
			return False
	
	def __checkCmd(self, dev, func, param):
		if (dev not in self.__cmds):
			return False
		if (func not in self.__cmds[dev]):
			return False
		if (param == None and self.__cmds[dev][func]['par']):
			return False
		if (param != None and not self.__cmds[dev][func]['par']):
			return False
		return True
	
	def __hasParam(self, dev, func):
		return self.__cmds[dev][func]['par']
	
	def __hasTimeParam(self, dev, func):
		return self.__cmds[dev][func]['time']
	
		


mega = Device(1)
mega.sendCmd('light', 'on')
mega.addCmd('light')
mega.addCmd('foo')
mega.addCmd('led')

	
mega.sendCmd('light', 'on')
nano = Device(10)
nano.sendCmd('light', 'on')
nano.addCmd('light')
nano.addCmd('foo')
nano.addCmd('led')

for i in range(0, 260):
    mega.sendCmd('led', 'on')
    nano.sendCmd('led', 'on')
    mega.sendCmd('led', 'off')
    nano.sendCmd('led','off')


print('\nTerminating program...\n')
GPIO.cleanup()
exit(0)
