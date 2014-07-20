#!/usr/bin/env python2.7

import sys
import os
import subprocess

homeDir = os.environ['HOME']
deviceList = [];

if os.path.exists("/dev/disk/by-label"):
	deviceStr = os.popen("ls /dev/disk/by-label/").read()
else: 
	print ('No SD Card/USB Device found')
	print ('Script aborted')
	sys.exit()
	
if not deviceStr:
	print ('No SD Card/USB Device found')
	print ('Script aborted')
	sys.exit()	 
	
else: 
	indexNL = [i for i, ltr in enumerate(deviceStr) if ltr == '\n']
	deviceList.insert(0,deviceStr[0:indexNL[0]])
	for i in xrange(1,len(indexNL)):
		deviceList.insert(i,deviceStr[indexNL[i-1]+1:indexNL[i]])
	for i in xrange(0,len(deviceList)):
		print (str(i)+ ').' + deviceList[i])

print ('Choose the number of a HedgeHog device from the list above.')
target = raw_input('Make sure the device you are choosing is actually a HedgeHog device:')

if int(target) < len(deviceList):
		subprocess.call(["sudo", "dd", "if=%s/.hhg/dd_img/dd.img" % homeDir, "of=/dev/disk/by-label/%s" %str(deviceList[int(target)])])
else: 	
	print('Chosen device does not exist')
	print('Script aborted')
	sys.exit()
