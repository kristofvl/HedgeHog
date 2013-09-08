#!/usr/bin/python2.7

import sys
import subprocess

if 'conf' in sys.argv[1]:
	subprocess.call(["/home/hany/bin/conf_HHG.py", sys.argv[1]])
if 'start' in sys.argv[1]:
	subprocess.call(["/home/hany/bin/start_HHG.py", sys.argv[1]])
