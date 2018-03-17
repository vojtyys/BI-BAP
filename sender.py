#!/usr/bin/python3
import time
import serial
import RPi.GPIO as GPIO
import crcmod


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)

ser = serial.Serial('/dev/ttyS0')
ser.baudrate = 9600
ser.timeout = 1

cmdCnt = 0x0
crc16 = crcmod.mkCrcFun(0x11021, 0xffff, False, 0x0000)

def checkCrc(data):
    crc = crc16(data[0:5])
    crc = str(hex(crc)).lstrip('0x')
    if (len(crc) != 4):
        crc = '0' + crc
    crc = bytes.fromhex(crc)
    tmp = data[5:]
#  print(tmp)
#    print(crc)
    if (tmp == crc):
        return True
    return False

class Device:
	def __init__(self, addr):
		self.__cnt = 0
		self.__addr = addr
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
		crc = crc16(data)
		crc = str(hex(crc)).lstrip('0x')
		if (len(crc) != 4):
			crc = '0' + crc
		data = bytes(data + bytes.fromhex(crc))
		print("Sending cmd: ", end=' ')
		print(data)
		GPIO.output(12, GPIO.HIGH)
		ser.write(data)
		ser.flush()
		GPIO.output(12, GPIO.LOW)
		while(True):
			print('Waiting for ACK')
			ack = ser.read(7)
			print('Got: ', end='')
			print(ack)
			if (len(ack) < 7):
				print('Incorrect CMD len, resending CMD')
				GPIO.output(12, GPIO.HIGH)
				ser.write(data)
				ser.flush()
				GPIO.output(12, GPIO.LOW)   
			else:
				if(checkCrc(ack) == False):
					print('Incorrect CRC, resending CMD')
					GPIO.output(12, GPIO.HIGH)
					ser.write(data)
					ser.flush()
					GPIO.output(12, GPIO.LOW)
				else:
					print('ACK OK')
					self.__cnt = self.__cnt + 1
					break



	



mega = Device(1)
mega.sendCmd('05 00 00')

ser.close()
print('\nTerminating program...\n')
GPIO.cleanup()
exit(0)
