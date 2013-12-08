#!/usr/bin/env python

import os
import time


def getDMESG():
	commLog = os.popen("dmesg | tail -n 1").read()
	return commLog
	#print commLog
	
def compareStatus(currentLogStatus):
	logStatus = getDMESG()
	if (logStatus!=currentLogStatus):
		currentLogStatus = logStatus
		os.system("notify-send \"" + currentLogStatus + "\"")
	#time.sleep(0.5)
	return currentLogStatus

def main():
	currentLogStatus = getDMESG()
	while (1):
		currentLogStatus=compareStatus(currentLogStatus)
        
if __name__ == "__main__":
	main()
