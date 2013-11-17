#!/usr/bin/python2.7

import sys
import os
import subprocess
from random import randint

home_dir = os.environ['HOME']
target = sys.argv[1]

rnd = randint(4,9999)

print('make sure the device you chose is listed down here')
print('if not exit at once with 0000')

out = subprocess.Popen(['ls', '-l', '/dev/disk/by-label/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
devices, err = out.communicate()
print devices

print rnd

print ('dd is a very dangerous command')
print ('and it could brick you hard disk')
print ('please exit if you are not sure')
print ('to exit enter 0000')

code = raw_input('to continue enter the passcode above: ')

if int(code) == rnd:
	print('code accepted')
	subprocess.call(["sudo", "dd", "if=%s/.hhg/dd_img/dd.img" % home_dir, "of=%s" %target])
else: 	
	sys.exit()
