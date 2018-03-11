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

crc16 = crcmod.mkCrcFun(0x11021, 0xffff, False, 0x0000)

tmp = bytes.fromhex('01 05 00 00 00')
crc = crc16(tmp)
crc = str(hex(crc)).lstrip('0x')
if (len(crc) != 4):
    crc = '0' + crc;
data = bytes(tmp + bytes.fromhex(crc))
print(data)
GPIO.output(12, GPIO.HIGH)
ser.write(data)
time.sleep(0.1)
GPIO.output(12, GPIO.LOW)

ser.close()
print('\nTerminating program...\n')
GPIO.cleanup()
exit(0)
