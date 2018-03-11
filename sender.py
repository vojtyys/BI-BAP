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

crc16 = crcmod.mkCrcFun(0x11021, 0xffff, False, 0x0000)

def checkCrc(data):
    crc = crc16(data[0:5])
    crc = str(hex(crc)).lstrip('0x')
    if (len(crc) != 4):
        crc = '0' + crc
    crc = bytes.fromhex(crc)
    tmp = data[5:]
#  print(tmp)
    print(crc)
    if (tmp == crc):
        return True
    return False
	
tmp = bytes.fromhex('01 05 12 80 f0')
crc = crc16(tmp)
crc = str(hex(crc)).lstrip('0x')
if (len(crc) != 4):
    crc = '0' + crc;
data = bytes(tmp + bytes.fromhex(crc))
#data = bytes(tmp + bytes.fromhex('00ff'))
print(data)
GPIO.output(12, GPIO.HIGH)
ser.write(data)
ser.flush()
GPIO.output(12, GPIO.LOW)

data = ser.read(7)
print('Got: ')
print(data)
if (len(data) < 7):
    print('Incorrect ACK')
    print(data)
else:
    if(checkCrc(data) == False):
        print('Incorrect CRC')
    else:
        print('ACK OK')

ser.close()
print('\nTerminating program...\n')
GPIO.cleanup()
exit(0)
