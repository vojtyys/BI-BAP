#!/usr/bin/python3

import os
import sys

#připojení modulu pyhouse do systémové cesty, aby mohl být importován
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pyhouse

#slovník zařízení pro jejich přidávání, odebírání a ovládání
devices = {}
#funkce pro zobrazení použití
def showUsage():
    print('''             Usage: add name address - use to add new device
                    del name - use to remove device
                    devices - list of devices
                    reset - reset communication
                    send name remote_device function [parameter] - send CMD
                    C^c, C^d - exit
                    help - show usage''')
#na počátku je vypsáno jak interpretr používat                    
showUsage()
try:
    while True:
        #čtení příkazů
        line = input('\nType a command: ')
        words = line.split() #rozdělení přečtené řádky na slova
        try:
            #detekce klícových slov
            
            #výpis přidaných zařízení
            if (words[0] == 'devices'):
                for key in devices:
                    print(key, end=', ')
                    print('addr: ' + str(devices[key].getAddr()))
                    
            #výpis nápovědy        
            elif (words[0] == 'help'):
                showUsage()
                
            #přidání nového univerzáního modulu    
            elif (words[0] == 'add'):
                #kontrola adresy
                if (not words[2].isdecimal()):
                    print('Address is not a number: ' + words[2])
                    continue
                #zařízení již bylo přidáno    
                if (words[1] in devices):
                    print('Device already added: ' + words[1])
                    continue
                    
                #přidání modulu    
                dev = pyhouse.Device(int(words[2]))
                devices[words[1]] = dev
                print(words[1] + ' added')
            
						#odebrání modulu    
            elif (words[0] == 'del'):
                #modulu neexistuje
                if(words[1] not in devices):
                    print('Device does not exists: ' + words[1])
                    continue
                
								#odebrání    
                del devices[words[1]]
                print(words[1] + ' removed')
            
						#provedení reset příkazu    
            elif(words[0] == 'reset'):
                #modul neexistuje
                if (words[1] not in devices):
                    print('Device does not exists: ' + words[1])
                    continue
                    
                dev = devices[words[1]]    
                dev.reset()
						
						#odeslání příkazu				    
            elif (words[0] == 'send'):
                #modul neexistuje
                if (words[1] not in devices):
                    print('Device not found: ' + words[1])
                    continue
                    
                #získání modulu    
                dev = devices[words[1]]
                
                #přečtena 4 slova - je to send modul dev func, pokud ne metoda sendCmd nás vyvede z omylu a vyhodí výjímku
                if(len(words) == 4):
                    try:
                        if(not dev.sendCmd(words[2], words[3])):
                            print('CMD sending unsuccessfull')
                    except Exception as e:
                        print(e.args[0])
                        continue
                #přečteno 5 slov, je to send modul dev func param, pokud ne sendCmd vyhodí vyjímku  
                elif (len(words) == 5):
                    try:
                        if(not dev.sendCmd(words[2], words[3], int(words[4]))):
                            print('CMD sending unsuccessfull')
                    except Exception as e:
                        print(e.args[0]) 
                        continue
                #nesprávný počet slov         
                else:
                    print('Invalid count of parameters')
            
						#nerozpoznáno klíčové slovo        
            else:
                print('Unknow command: ' + words[0])
        #pokus o přístup k chybějícím slovům       
        except IndexError:
            print('Incomplete command')

#ukončení pomocí c^c nebo c^d a odebrání modulu pyhouse ze systémové cesty
except KeyboardInterrupt:
    sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
    exit(0)
except EOFError:
    sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
    exit(0)
