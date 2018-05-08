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
#zde je parametr příliš velký
try:
    if(not a.sendCmd('socket4', 'timeon', 725360)):
        print("Cannot send CMD")
except Exception as e:
    print(e.args[0])  #vypíše, co bylo špatně


    
#zapnutí zásuvky 2 a 4
if(not a.sendCmd('socket2', 'on')):
    print("Cannot send CMD")

if(not a.sendCmd('socket4', 'on')):
    print("Cannot send CMD")
    

#vypnutí zásuvky 4
if(not a.sendCmd('socket4', 'off')):
    print("Cannot send CMD")
    
  
#zásuvka 3 se automaticky zapne za 10 s
if(not a.sendCmd('socket3', 'timeon', 10)):
    print("Cannot send CMD")
    
#vlastně nezapne, funkce cancel ruší naplánované zapnutí a vypnutí
if(not a.sendCmd('socket3', 'cancel')):
    print("Cannot send CMD")

#zásuvka 2 se zapne za 650 s
if(not a.sendCmd('socket2', 'autoon', 650)):
    print("Cannot send CMD")
  
     