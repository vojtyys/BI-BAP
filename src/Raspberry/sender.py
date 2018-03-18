#!/usr/bin/python3

import time
import serial
import RPi.GPIO as GPIO
import crcmod

cmds = {'light' : 0,
       	'socket' : 1,
	'boiler' : 2,
	'window' : 3
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
	
	def __del__(self):
		self.__ser.close()
	
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
	crc = str(hex(crc)).lstrip('0x')
	
	if (len(crc) == 0):
		crc = '0000'
	elif (len(crc) == 1):
		crc = '000' + crc	
	elif (len(crc) == 2):
		crc = '00' + crc
	elif (len(crc) == 3):
		crc = '0' + crc
		
	crc = bytes.fromhex(crc)
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
		self.__ser = RS485(12, 9600, 3)
		
	def sendCmd(self,cmd):
		tmp = str(hex(self.__addr)).lstrip('0x')
		if (len(tmp) ==1):
			tmp = '0' + tmp
		data = bytes.fromhex(tmp)
		
		if(self.__cnt == 0):
			data = bytes(data + bytes.fromhex('00'))
		else:
			tmp = str(hex(self.__cnt)).lstrip('0x')
			if (len(tmp) == 1):
				tmp = '0' + tmp
			data = bytes(data + bytes.fromhex(tmp))
		
		data = bytes(data + bytes.fromhex(cmd))
		crc = getCrc(data)
		data = bytes(data + crc)
		print("Sending cmd: ", end='')
		print(data)
		self.__ser.sendData(data)
		while(True):
			print('Waiting for ACK')
			ack = self.__ser.getData(7)
			print('Got: ', end='')
			print(ack)
			if (len(ack) < 7):
				print('Incorrect CMD len, resending CMD')
				self.__ser.sendData(data)
			else:
				if(checkCrc(ack) == False):
					print('Incorrect CRC, resending CMD')
					self.__ser.sendData(data)
				else:
					print('ACK OK')
					self.__cnt = (self.__cnt + 1) % 256
					break


mega = Device(1)
try:
	while(True):
		mega.sendCmd('05 00 00')
		time.sleep(0.5)
except KeyboardInterrupt:
	print('\nTerminating program...\n')
	GPIO.cleanup()
	exit(0)
