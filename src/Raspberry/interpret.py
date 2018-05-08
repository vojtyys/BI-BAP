#!/usr/bin/python3

import os
import sys
import pyhouse

#slovník zařízení pro jejich přidávání, odebírání a ovládání
devices = {}
#funkce pro zobrazení použití
def showUsage():
    print('''             Usage: add name address - use to add new device
                        name should be choosed by user,
                        address is address of remote device 
                    del name - use to remove device
                        name is name used by add command
                    devices - list of added devices
                    reset name - reset packet counters local and on remote device
                        name is name used by add command
                    send name remote_device function [parameter] - send CMD packet to remote device
                        name is name of remote device added by add command
                        remote_device should be light1, light2, socket1, socket2, socket3, socket4, window or boiler
                        function depends on choosen remote_device
                            lightX has:  on - turn on light, without parameter
                                         off - turn off light, without parameter
                                         dim - set light intensity as parameter in range 0-255
                                         timeon - turn on light after N seconds, passed as parameter in range 0-65535
                                         timeoff - turn off light after N seconds, passed as parameter in range 0-65535
                                         autoon - turn on light when room become dark
                                         cancel - cancel sheduled timeon, timeoff and autoon
                            socketX has: on - turn on socket
                                         off - turn off socket
                                         timeon - turn on socket after N seconds, passed as parameter in range 0-65535
                                         timeoff - turn off socket after N seconds, passed as parameter in range 0-65535
                                         cancel - cancel sheduled timeon and timeoff
                            window has:  open - to open window
                                         close - to close window
                            boiler has:  temp - set target room temperature, passed as parameter in range 0-255
                                         on - start holding target temperature
                                         off - stop holding target temperature 
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
                if (not dev.reset()):
                    print('Cannot send reset CMD')
                else:
                    print('ok')
                        
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
                            print('Cannot send cmd')
                        else:
                            print('ok')
                    except Exception as e:
                        print(e.args[0])
                        continue
                #přečteno 5 slov, je to send modul dev func param, pokud ne sendCmd vyhodí vyjímku  
                elif (len(words) == 5):
                    #kontrola, jestli je parametr číslo
                    if (not words[4].lstrip('-+').isdecimal()):
                        print('Parameter is not a number')
                        continue
                    try:
                        if(not dev.sendCmd(words[2], words[3], int(words[4]))):
                            print('Cannot send cmd')
                        else:
                            print('ok')
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
    exit(0)
except EOFError:
    exit(0)
