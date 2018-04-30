#!/usr/bin/python3

import time
import serial
import RPi.GPIO as GPIO
import crcmod

cmds = {'light1' : {'cmd'        : 1,
   
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
                                    'cmd'       : 4},
                                   
                    'autoon'     : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 5},
                                    
                    'cancel'     : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 6}},

        'light2' : {'cmd'        : 2,
   
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
                                    'cmd'       : 4},
                                   
                    'autoon'     : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 5},
                                    
                    'cancel'     : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 6}},


      'socket1' : {'cmd'         : 3,
    
                   'on'          : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 0},
    
                   'off'         : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 1},
     
                  'timeon'       : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 2},
		    
                  'timeoff'      : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 3},
                                    
                  'cancel'       : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 4}},                 
                                    
      'socket2' : {'cmd'         : 4,
    
                   'on'          : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 0},
    
                   'off'         : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 1},
     
                  'timeon'       : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 2},
		    
                  'timeoff'      : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 3},
                                    
                  'cancel'       : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 4}},   
                                    
      'socket3' : {'cmd'         : 5,
    
                   'on'          : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 0},
    
                   'off'         : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 1},
     
                  'timeon'       : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 2},
		    
                  'timeoff'      : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 3},
                                    
                  'cancel'       : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 4}},   
                                    
      'socket4' : {'cmd'         : 6,
    
                   'on'          : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 0},
    
                   'off'         : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 1},
     
                  'timeon'       : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 2},
		    
                  'timeoff'      : {'par'       : True,
                                    'time'      : True,
                                    'cmd'       : 3},
                                    
                  'cancel'       : {'par'       : False,
                                    'time'      : False,
                                    'cmd'       : 4}},   
	
      'boiler' : {'cmd'         : 7,
		    
                  'temp'        : {'par'       : True,
                                   'time'      : False,
                                   'cmd'       : 0},
		    
                  'on'          : {'par'       : False,
                                   'time'      : False,
                                   'cmd'       : 1},
    
                  'off'         : {'par'       : False,
                                   'time'      : False,
                                   'cmd'       : 2}},
	
      'window' : {'cmd'         : 8,
     
                  'open'        : {'par'       : False,
                                   'time'      : False,
                                   'cmd'       : 0},
		    
                  'close'       : {'par'       : False,
                                   'time'      : False,
                                   'cmd'       : 1}}
	
       
       }

GPIO.setwarnings(False)
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
        
    def clearInput(self):
        self.__ser.flushInput()
        
class CRC:
    def __init__(self):
        self.__crc = crcmod.mkCrcFun(0x11021, 0xffff, False, 0x0000)
    
    def getCrc(self, data):
        crc = self.__crc(data)
        crc = crc.to_bytes(2, 'big')
        return crc


    def checkCrc(self, data):
        crc = self.getCrc(data[0:6])
        tmp = data[6:]
        if (tmp == crc):
            return True
        return False


class Device:
    def __init__(self, addr):
        self.__cnt = 0
        self.__addr = addr
        self.__ser = RS485(12, 9600, 1)
        self.__crc = CRC()
        self.reset()
    
        
    def sendCmd(self,dev, func=None, param=None):
        if (dev != 'reset'):
            if (not self.__checkCmd(dev, func, param)):                         
                print('Device, function or parameter was not recognized.')
                return True
    
            data = self.__addr.to_bytes(1, 'big') + self.__cnt.to_bytes(1, 'big') + cmds[dev]['cmd'].to_bytes(1, 'big') + cmds[dev][func]['cmd'].to_bytes(1, 'big')
            if (self.__hasParam(dev, func)):                                                    
                if (self.__hasTimeParam(dev, func)):                                        
                    data = data + param.to_bytes(2, 'big')                                   
                else:
                    data = data + param.to_bytes(1, 'big') + bytes.fromhex('00')        
            else:
                data = data + bytes.fromhex('00 00')
        else:
            data = self.__addr.to_bytes(1, 'big') + self.__cnt.to_bytes(1, 'big') + bytes.fromhex('00 00 00 00')
        data = data + self.__crc.getCrc(data)
    
        self.__ser.clearInput()
        print("Sending cmd: ", end='')
        print(data)
        self.__ser.sendData(data)
    
        attempts = 10
        while(True):
                    if(attempts == 0):
                        print('Error: cannot send CMD: ', end='')
                        print(dev)
                        return False
    
                    if (not self.__checkAck()):   
                        time.sleep(2)
                        print('Sending CMD again: ' + str(data))
                        self.__ser.sendData(data)
                        attempts = attempts - 1
                    else:
                        self.__cnt = (self.__cnt + 1) % 256
                        return True
            
   
    def reset(self):
        self.sendCmd('reset')
        self.__cnt = 0
        
    def getAddr(self):
        return self.__addr
    
    def __checkAck(self):        
        expectedAck = bytes.fromhex('00') + self.__cnt.to_bytes(1, 'big') + bytes.fromhex('00') + self.__addr.to_bytes(1, 'big') + bytes.fromhex('00 00')    
        expectedAck = expectedAck + self.__crc.getCrc(expectedAck)
        
        print('Waiting for ACK')
        ack = self.__ser.getData(8)
        print('Got: ' + str(ack))
        
        if (ack == expectedAck):
            print('ACK OK')
            return True
        else:
            print('Incorrect ACK, expected: ' + str(expectedAck))
            return False
    
    def __checkCmd(self, dev, func, param):
        if (dev not in cmds):
            return False
        if (func not in cmds[dev]):
            return False
        if (param == None and cmds[dev][func]['par']):
            return False
        if (param != None and not cmds[dev][func]['par']):
            return False
        return True
    
    def __hasParam(self, dev, func):
        return cmds[dev][func]['par']
    
    def __hasTimeParam(self, dev, func):
        return cmds[dev][func]['time']
