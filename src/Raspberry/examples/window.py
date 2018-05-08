#!/usr/bin/python3

import sys
import time
import pyhouse  #importuje ovládací API


    
#inicializace 
a = pyhouse.Device(1)    #modul s adresou 1

#doporučené volání pro synchronizaci čítačů paketů řídící jednotky a univerzálního modulu
if(not a.reset()):
    print("Connection between devices cannot be established")
    exit(1)
    

#správně by mělo volání funkce sendCmd vypadat takto, protože může vyvolat výjímku při špatně zadaných parametrech
#zde je neexistující zařízení
try:
    if(not a.sendCmd('window7', 'open')):
        print("Cannot send CMD")
except Exception as e:
    print(e.args[0])  #vypíše, co bylo špatně
    
#otevření okna
if(not a.sendCmd('window', 'open')):
    print("Cannot send CMD")
    
#a zavření
if(not a.sendCmd('window', 'close')):
    print("Cannot send CMD")


