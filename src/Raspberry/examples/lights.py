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
#zde nebyla zadaná funkce
try:
    if(not a.sendCmd('light1')):
        print("Cannot send CMD")
except Exception as e:
    print(e.args[0])  #vypíše, co bylo špatně

#zapnutí světla na poslední nastavenou hodnotu stmívání před vypnutím, nebo na hodnotu 255, pokud je zapnuto poprvé
if(not a.sendCmd('light1', 'on')):
        print("Cannot send CMD")    
#čekání na zapnutí
time.sleep(15)

#vypnutí světla
if(not a.sendCmd('light1', 'off')):
    print("Cannot send CMD")

#čekání na vypnutí
time.sleep(15)

#pokud je světlo vypnuté funkce dim nastaví hodnotu stmívání při příštím spuštění
if(not a.sendCmd('light1', 'dim', 10)):
    print("Cannot send CMD")
    
#zapnutí světla - to bude nyní nastaveno na hodnotu stmívání 10
if(not a.sendCmd('light1', 'on')):
    print("Cannot send CMD")    

time.sleep(5)

#světlo se za 10 s vypne a 5 s po vypnutí znovu zapne
if(not a.sendCmd('light1', 'timeoff', 10)):
    print("Cannot send CMD")
if(not a.sendCmd('light1', 'timeon', 15)):
    print("Cannot send CMD")
 
 #vypnutí světla   
if(not a.sendCmd('light1', 'off')):
    print("Cannot send CMD")


#světlo se automaticky zapne, pokud se v místnosti setmí
if(not a.sendCmd('light1', 'autoon')):
    print("Cannot send CMD")

#takto se ruší naplánované časové vypnutí/zapnutí a automatické zapnutí podle intenzity osvětlení
if(not a.sendCmd('light1', 'cancel')):
    print("Cannot send CMD")

