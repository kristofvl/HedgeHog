#!/usr/bin/env python2.7

import os
import time
import subprocess


def getDMESG():
	usbLog = os.popen("dmesg | tail -n 1").read()
	return usbLog

def getMount():
	mountLog = os.popen("mount").read()
	return mountLog
	
def compareStatus(currentLogStatus):
	logStatus = getDMESG()
	if 'Attached' in logStatus and logStatus != currentLogStatus:
		currentLogStatus = logStatus
		subprocess.call(["notify-send", "HedgeHog Device Found"])
		subprocess.call(["notify-send", "Device is being mounted"])
		while True:
			mountStatus = getMount()
			if 'HEDG' in mountStatus:
				break
		subprocess.call(["./download_HHG.py"])
	return currentLogStatus

def main():
	currentLogStatus = getDMESG()
	while (1):
		currentLogStatus = compareStatus(currentLogStatus)
		time.sleep(1)
        
if __name__ == "__main__":
	main()
