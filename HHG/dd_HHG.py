#!/usr/bin/env python2.7

import sys
import os
import subprocess
from random import randint
from termcolor import colored

homeDir = os.environ['HOME']
rnd = randint(4,9999)

print('Your input should be like /dev/DEVICE')
print('Choose a HedgeHog device from the list:')

out = subprocess.Popen(['ls', '-l', '/dev/disk/by-label/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
devices, err = out.communicate()
devices = devices[:-1]
devices = devices[8:]
print colored(devices,'green')

target = raw_input('Enter your device path:')

print colored('Your passcode is: ' + str(rnd), 'red')

print ('dd is a very dangerous tool and could brick your MBR')
print ('Please exit if you are not sure')
print ('Press Enter to exit')

code = raw_input('To continue enter the passcode above: ')

if code.isdigit():
	if int(code) == rnd:
		print('Code accepted')
		subprocess.call(["sudo", "dd", "if=%s/.hhg/dd_img/dd.img" % homeDir, "of=%s" %target])
else: 	
	print('Script aborted')
	sys.exit()
