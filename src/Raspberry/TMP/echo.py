#!/usr/bin/python3
import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)

ser = serial.Serial('/dev/ttyS0');
ser.baudrate = 9600
ser.timeout = 1
try:
    while(True):
        data=input('Enter data: ').encode('ascii')
        GPIO.output(12, GPIO.HIGH)
        ser.write(data)
        ser.flush()
        GPIO.output(12, GPIO.LOW)
        data = ser.read(50)
        print(data)
except KeyboardInterrupt:
    ser.close()
    GPIO.output(12, GPIO.LOW)
    GPIO.cleanup()
    print("END")
