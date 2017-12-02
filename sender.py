#!/usr/bin/python3
import time
import serial
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)

ser = serial.Serial('/dev/ttyS0')
ser.baudrate = 9600
while True:
    try:
        data = bytes(input('Enter addres and command or ^C to exit: '), 'ascii')
        GPIO.output(12, GPIO.HIGH)
        ser.write(data)
        time.sleep(0.1)
        GPIO.output(12, GPIO.LOW)
    except(KeyboardInterrupt):
        ser.close()
        print('\nTerminating program...\n')
        GPIO.cleanup()
        exit(143)
