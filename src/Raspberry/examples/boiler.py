#!/usr/bin/python3

import sys
import time
import pyhouse  #importuje ovládací API


    
#inicializace 
a = pyhouse.Device(1)    #modul s adresou 1

#doporučené volání pro synchronizaci čítačů paketů  řídící jednotky a univerzálního modulu
if(not a.reset()):
    print("Connection between devices cannot be established")
    exit(1)

#správně by mělo volání funkce sendCmd vypadat takto, protože může vyvolat výjímku při špatně zadaných parametrech
#zde je špatně zadané jméno funkce
try:
    if(not a.sendCmd('boiler', 'tmp')):
        print("Cannot send CMD")
except Exception as e:
    print(e.args[0])  #vypíše, co bylo špatně
		    
#nastavení teploty na v místnosti na 40°C
if(not a.sendCmd('boiler', 'temp', 40)):
    print('Cannot send cmd')

#zapnutí udržování nastavené teploty
if(not a.sendCmd('boiler', 'on')):
     print('Cannot send cmd')
     
#vypnutí udržování nastavené teploty
if(not a.sendCmd('boiler', 'off')):
     print('Cannot send cmd')
    