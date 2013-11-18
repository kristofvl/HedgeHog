#!/usr/bin/python2.7

import sys
import os
import subprocess
from random import randint

home_dir = os.environ['HOME']

rnd = randint(4,9999)

print('choose a HedgeHog device from the list')
print('your input should be like /dev/sdd')

out = subprocess.Popen(['ls', '-l', '/dev/disk/by-label/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
devices, err = out.communicate()
print devices

target = raw_input('device name: ')

print rnd

print ('dd is a very dangerous command')
print ('and could brick your MBR')
print ('please exit if you are not sure')
print ('to exit enter 0000')

code = raw_input('to continue enter the passcode above: ')

if int(code) == rnd:
	print('code accepted')
	subprocess.call(["sudo", "dd", "if=%s/.hhg/dd_img/dd.img" % home_dir, "of=%s" %target])
else: 	
	sys.exit()
