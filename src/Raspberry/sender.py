#!/usr/bin/python3

import time
import serial
import RPi.GPIO as GPIO
import crcmod

cmds = {'light' : {'cmd' : 0,
		   'on'  : 0,
		   'off' : 1,
		   'dimlevel' : 2},
	
       	'socket' : {'cmd' : 1,
		    'on'  : 0,
		    'off' : 1},
	
	'boiler' : {'cmd' : 2,
		    'temp' : 0},
	
	'window' : {'cmd' : 3,
		    'open' : 0,
		    'close' : 1},
	
	'led'    : {'cmd' : 4,
		    'on'  : 0,
		    'off' : 1}
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
	crc = getCrc(data[0:5])
	tmp = data[5:]
	if (tmp == crc):
		return True
	return False


class Device:
	def __init__(self, addr):
		self.__cnt = 0
		self.__addr = addr
		self.__ser = RS485(12, 9600, 1)
		self.__cmds = {}
	
		
	def sendCmd(self,cmd, param1):
		
		data = self.__addr.to_bytes(1, 'big')
		
		data = data + self.__cnt.to_bytes(1, 'big')
		
		if (cmd not in self.__cmds):
			print('Unknown command')
			return
		
		if (param1 not in self.__cmds[cmd]):
			print('Unknow function')
			return
		
		tmpParam2 = bytes.fromhex('00')
		data = data + self.__cmds[cmd]['cmd'].to_bytes(1, 'big') + self.__cmds[cmd][param1].to_bytes(1, 'big') + tmpParam2
		crc = getCrc(data)
		data = bytes(data + crc)
		print("Sending cmd: ", end='')
		print(data)
		self.__ser.sendData(data)
		attempts = 10
		while(True):
                    if(attempts == 0):
                        print('Error: cannot send CMD: ', end='')
                        print(cmd)
                        break

                    expectedAck = bytes.fromhex('00') + self.__cnt.to_bytes(1, 'big') + bytes.fromhex('00') + self.__addr.to_bytes(1, 'big') + bytes.fromhex('00')
                    expectedAck = expectedAck + getCrc(expectedAck)
                    print('Waiting for ACK')
                    ack = self.__ser.getData(7)
                    print('Got: ', end='')
                    print(ack)
                    if (ack != expectedAck):
                        print('Incorrect ACK, expected: ' + str(expectedAck))
                        print('Sending CMD again: ' + str(data))
                        self.__ser.sendData(data)
                        attempts = attempts - 1
                    else:
                        print('ACK OK')
                        self.__cnt = (self.__cnt + 1) % 256
                        break
			
	def addCommand(self, cmd):
		if (cmd not in cmds):
			print('Unknown command')
			return
		self.__cmds[cmd] = cmds[cmd]
				
	
		


mega = Device(1)
mega.sendCmd('light', 'on')
mega.addCommand('light')
mega.addCommand('foo')

	
mega.sendCmd('light', 'on')
nano = Device(10)
nano.sendCmd('light', 'on')
nano.addCommand('light')
nano.addCommand('foo')

nano.sendCmd('light', 'off')
for i in range(0, 260):
    mega.sendCmd('light', 'on')
    nano.sendCmd('light', 'on')

print('\nTerminating program...\n')
GPIO.cleanup()
exit(0)
