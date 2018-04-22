#!/usr/bin/python3

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pyhouse

#slovník zařízení pro jejich přidávání, odebírání a ovládání
devices = {}

try:
    while True:
        line = input('\nType a command: ')
        words = line.split()
        try:
            if (words[0] == 'add'):
                if (not words[2].isdecimal()):
                    print('Address is not a number: ' + words[2])
                    continue
                if (words[1] in devices):
                    print('Device already added: ' + words[1])
                    continue
                dev = pyhouse.Device(int(words[2]))

                devices[words[1]] = dev
                print(words[1] + ' added')
                
            elif (words[0] == 'del'):
                if(words[1] not in devices):
                    print('Device does not exists: ' + words[1])
                    continue
                del devices[words[1]]
                print(words[1] + ' removed')
                
            elif(words[0] == 'call'):
                if (words[1] not in devices):
                    print('Device does not exists: ' + words[1])
                    continue
                    
                dev = devices[words[1]]    
                if (words[2] == 'addCmd'):
                    dev.addCmd(words[3])
                elif (words[2] == 'delCmd'):
                    dev.delCmd(words[3])
                elif (words[2] == 'showCmd'):
                    dev.showCmd()
                elif (words[2] == 'reset'):
                    dev.reset()
                else:
                    print('Unknown method: ' + words[2])
                    continue
                    
            elif (words[0] == 'send'):
                if (words[1] not in devices):
                    print('Device not found: ' + words[1])
                    continue
                dev = devices[words[1]]
                if(len(words) == 4):
                    dev.sendCmd(words[2], words[3])
                elif (len(worlds) == 5):
                    dev.sendCmd(word[2], word[3], word[4])                
                else:
                    print('Invalid count of parameters')
            else:
                print('Unknow command: ' + words[0])
        except IndexError:
            print('Incomplete command')

except KeyboardInterrupt:
    exit(0)
except EOFError:
    exit(0)
