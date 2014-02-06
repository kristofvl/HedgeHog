#!/usr/bin/env python2.7

import os
import time
import datetime
import subprocess


def getDMESG():
	usbLog = os.popen("dmesg -T | tail -n 30 | grep HedgeHog").read()
	return usbLog

def compareStatus(currentLogStatus):
	logStatus = getDMESG()
	if logStatus:
		dateString = logStatus[4:24]
		dateString = dateString[:4] + dateString[5:]
		#print dateString
		dateStruct = datetime.datetime.strptime(dateString, "%b %d %H:%M:%S %Y")
		#print dateStruct
		timeDelta = datetime.datetime.now() - dateStruct
		#print timeDelta.seconds 
		if (timeDelta.seconds < 1): 
			return 1
		else:
			return 0
	else:
		return 0

