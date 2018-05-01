#!/usr/bin/python3

import time
import serial
import RPi.GPIO as GPIO
import crcmod

#slovník popisující podporovaná zařízení, jejich funkce, přijímání parametrů a kódování pro odesílání
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
#nastavení enable pinu pro ovládání směru komunikace po RS485
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)

#třída pro komunikaci na RS485
class RS485:
    #konstruktor přijímá int baudrate a int timeout pro čtení dat v s
    def __init__(self, baudrate, timeout):
        self.__ser = serial.Serial('/dev/ttyS0')   #otevření sériové  linky
        self.__ser.baudrate = baudrate             #nastavení parametrů
        self.__ser.timeout = timeout
        self.__OE = 12
        
    # metoda pro odeslání dat, data jsou typu byte
    def sendData(self, data):
        GPIO.output(self.__OE, GPIO.HIGH)
        self.__ser.write(data)
        self.__ser.flush()
        GPIO.output(self.__OE, GPIO.LOW)
    
		#meoda pro čtení příchozích dat, parametr int cnt - počet dat k přijetí v B    
    def getData(self, cnt):
        data = self.__ser.read(cnt)
        return data
    
		#metoda pro vyčištění příchozího bufferu    
    def clearInput(self):
        self.__ser.flushInput()

#třída pro práci s crc        
class CRC:
    #inicializace CRC
    def __init__(self):
        self.__crc = crcmod.mkCrcFun(0x11021, 0xffff, False, 0x0000)
    #vypočítá CRC pro vstupní data typu byte, vrátí vypočítanou hodnotu typu byte
    def getCrc(self, data):
        crc = self.__crc(data)
        crc = crc.to_bytes(2, 'big')
        return crc

		#kontroluje CRC přijatých dat, parametrem jsou přijatá data typu byte obsahující CRC, vrací true/false
    def checkCrc(self, data):
        crc = self.getCrc(data[0:6])
        tmp = data[6:]
        if (tmp == crc):
            return True
        return False

#třída pro reprezentaci připojeného univerzálního modulu
class Device:
    #konstruktor přijímá int addr - adresu univerzálního modulu
    def __init__(self, addr):
        self.__cnt = 0
        self.__addr = addr
        self.__ser = RS485(12, 9600, 1)
        self.__crc = CRC()
        self.reset()
    
     #metoda pro odeslání CMD, parametry jsou: str dev - nazev ovladaneho zarizeni, str func - název funkce k provedeni, int param - parametr funkce   
    def sendCmd(self, dev, func=None, param=None):
        if (dev != 'reset'):
            self.__checkCmd(dev, func, param)  #kontrola vstupních parametrů                       
                
            #vytvoření dat k odeslání
            #připojí se adresa cílové jednotky, číslo paketu, zařízení a funkce
            data = self.__addr.to_bytes(1, 'big') + self.__cnt.to_bytes(1, 'big') + cmds[dev]['cmd'].to_bytes(1, 'big') + cmds[dev][func]['cmd'].to_bytes(1, 'big')
            #pokud funkce přijímá parametry, připojí se
						if (self.__hasParam(dev, func)):                                                    
                if (self.__hasTimeParam(dev, func)):  #připojení 2B časového parametru                                      
                    data = data + param.to_bytes(2, 'big')                                   
                else:   #připojení 1B parametru
                    data = data + param.to_bytes(1, 'big') + bytes.fromhex('00')        
            else: #funkce nepřijímá parametry
                data = data + bytes.fromhex('00 00')
        else: #vytvoření reset příkazu
            data = self.__addr.to_bytes(1, 'big') + self.__cnt.to_bytes(1, 'big') + bytes.fromhex('00 00 00 00')
         
				#připojení CRC    
        data = data + self.__crc.getCrc(data)
    
        #pokud po sběrnici přišlo něco nečekaného, například při debugování univerzálních modulů přes sériovou linku, je to ignorováno
        self.__ser.clearInput()
        #print("Sending cmd: ", end='')
        #print(data)
        self.__ser.sendData(data)   #odeslání dat
    
        #opakování odeslání zprávy, pokud nepřijde platné potvrzení nebo vyprší počet pokusů
        attempts = 9
        while(True):
                    if(attempts == 0): #vypršel počet pokusů, zprávu se nepodařilo odeslat
                        #print('Error: cannot send CMD: ', end='')
                        #print(dev)
                        return False
    
                    if (not self.__checkAck()): #ack nepřišlo nebo přišla poškozená data  
                        time.sleep(1) #čekání s novým odesláním 1s, pokud byla data porušená rušením, možná mezitím odezní
                        #print('Sending CMD again: ' + str(data))
                        self.__ser.sendData(data) #posílání zprávy znovu
                        attempts = attempts - 1
                    else:
                        self.__cnt = (self.__cnt + 1) % 256   #zpráva odeslána úspěšně, inkrementace čísla zprávy
                        return True
            
    #příkaz k resetování číslování posílaných paketů , vrátí true, pokud se povedlo spojit s univerzálním modulem a resetoat čítače, jinak vrátí false
    def reset(self):
        ret = self.sendCmd('reset')
        if (ret):
            self.__cnt = 0
        return ret
    
		#vrací int adresu univerzáního modulu    
    def getAddr(self):
        return self.__addr
    
    #kontrola potvrzovacího paketu, vrací true, pokud je v pořádku, jinak false
    def __checkAck(self): 
		    #vytvoření očekávané zprávy k porovnání       
        expectedAck = bytes.fromhex('00') + self.__cnt.to_bytes(1, 'big') + bytes.fromhex('00') + self.__addr.to_bytes(1, 'big') + bytes.fromhex('00 00')    
        expectedAck = expectedAck + self.__crc.getCrc(expectedAck)
        
        #print('Waiting for ACK')
        ack = self.__ser.getData(8) #čekání na příjem potvrzovacího paketu
        #print('Got: ' + str(ack))
        
        if (ack == expectedAck):  #kontrola
            #print('ACK OK')
            return True
        else:
            #print('Incorrect ACK, expected: ' + str(expectedAck))
            return False
            
    #kontrola, jestli jde o známé zařízení, funkci a jestli je v pořádku parameter, pokud ne, vyhodí Exception s popisem chyby v args[0]
    def __checkCmd(self, dev, func, param):
        if (dev not in cmds):  #kontrola existence zařízení
            raise Exception('Unknown device')
        if (func not in cmds[dev]):  #kontrola existence funkce
            raise Exception('Unknown function')
        if (param == None and self.__hasParam(dev, func)):  #parametr není a má být
            raise Exception('Parameter expected')
        if (param != None and not self.__hasParam(dev, func)):  #parametr je a nemá být
            raise Exception('Unexpected parameter')
        if (self.__hasParam(dev, func)):
            if (not isinstance(param, int)):  #parametr není int
                raise Exception('Invalid parameter, not int')
            if (self.__hasTimeParam(dev, func)):
                if (param < 0 or param > 65535): #časový parametr mimo rozsah
                    raise Exception('Parameter out of range')
            else:
                if (param < 0 or param > 255):  #parametr mimo rozsah
                    raise Exception('Parameter out of range')
    
    #kontrola, jestli funkce nad daným zařízením přijímá parametr, vrací true/false
    def __hasParam(self, dev, func):
        return cmds[dev][func]['par']
    
    #kontrola, jestli funkce nad daným zařízením přijímá časový parametr, vrací true/false
    def __hasTimeParam(self, dev, func):
        return cmds[dev][func]['time']
