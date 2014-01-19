#!/usr/bin/env python2.7

import os
import time
import subprocess


def getDMESG():
	usbLog = os.popen("dmesg | tail -n 20").read()
	return usbLog

def getMount():
	mountLog = os.popen("mount -l").read()
	return mountLog

def compareStatus(currentLogStatus):
	logStatus = getDMESG()
	loop = True
	if 'ESS TUD' in logStatus and logStatus != currentLogStatus:
		currentLogStatus = logStatus
		subprocess.call(["notify-send", "HedgeHog Device Found"])
		while loop:
			mountStatus = getMount()
			if 'HEDGEHG' in mountStatus:
				subprocess.call(["notify-send", "Device mounted"])
				loop = False
		subprocess.call(["./download_HHG.py"])
	return currentLogStatus

def main():
	currentLogStatus = getDMESG()
	while (1):
		currentLogStatus = compareStatus(currentLogStatus)
		time.sleep(1)
        
if __name__ == "__main__":
	main()
