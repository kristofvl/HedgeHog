#!/usr/bin/env python2.7

import sys
import os
import subprocess
from random import randint

homeDir = os.environ['HOME']
deviceList = [];

if os.path.exists("/dev/disk/by-label"):
	deviceStr = os.popen("ls /dev/disk/by-label/ | grep HEDGE").read()
else: 
	print ('No HdegeHog device found')
	print ('Script aborted')
	sys.exit()
	
if not deviceStr:
	print ('No HedgeHog device found')
	print ('Script aborted')
	sys.exit()	 
else: 
	indexNL = [i for i, ltr in enumerate(deviceStr) if ltr == '\n']
	i = 0
	for ind in indexNL:
		deviceList.insert(i,deviceStr[ind-11:ind])
		print (str(i)+ ').' + deviceStr[ind-11:ind])
		i = i+1

target = raw_input('Choose the number of a HedgeHog device from the list above:')

if int(target) < len(deviceList):
		subprocess.call(["sudo", "dd", "if=%s/.hhg/dd_img/dd.img" % homeDir, "of=/dev/disk/by-label/%s" %str(deviceList[int(target)])])
else: 	
	print('Chosen device does not exist')
	print('Script aborted')
	sys.exit()
