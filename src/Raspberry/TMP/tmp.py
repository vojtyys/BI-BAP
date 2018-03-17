#!/usr/bin/python3
import time
import serial
import RPi.GPIO as GPIO
import crcmod


GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.LOW)
while(True):
    GPIO.output(10, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(10, GPIO.LOW)
    time.sleep(2)
#ser = serial.Serial('/dev/ttyS0')
#ser.baudrate = 9600
#ser.timeout = 3
#try:
#   while(True):
#GPIO.output(12, GPIO.HIGH)
#ser.flush()
#    print('a')
#data = ser.read()
#print(data)
#GPIO.output(12, GPIO.LOW)
#except KeyboardInterrupt:
#   GPIO.output(12, GPIO.LOW);
#   print("END")
