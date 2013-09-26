#!/usr/bin/python2.7


import sys
from gi.repository import Gtk, GObject
import subprocess
import time, datetime, os
from datetime import timedelta

class timer:
	
	def calcStpTime(self, stpTime):
		stpTime_struc = datetime.datetime.now()+timedelta(days=7)
		stpTime.insert(0,stpTime_struc.year)
		stpTime.insert(1,stpTime_struc.month)
		stpTime.insert(2,stpTime_struc.day)

	def setTime(self, confpath, stpTime):
		sysTime = datetime.datetime.now()

		if (stpTime[0]<sysTime.year) or (stpTime[0]==sysTime.year and stpTime[1]<sysTime.month) or (stpTime[0]==sysTime.year and 
						stpTime[1]==sysTime.month and stpTime[2]<sysTime.day):
			self.calcStpTime(stpTime)

		with open (confpath, "r+w") as confhhg: 
			confhhg.seek(59,0)  # Write System Time
			confhhg.write(chr(sysTime.year-2000))
			confhhg.write(chr(0))
			confhhg.write(chr(sysTime.day))
			confhhg.write(chr(sysTime.month))
			confhhg.write(chr(sysTime.hour))
			confhhg.write(chr(0))
			confhhg.write(chr(sysTime.second))
			confhhg.write(chr(sysTime.minute))
			confhhg.seek(70,0)  # Write Stop Time
            		confhhg.write(chr(stpTime[0]-2000))
            		confhhg.write(chr(0))
            		confhhg.write(chr(stpTime[2]))
            		confhhg.write(chr(stpTime[1])) # Month
            		confhhg.write(chr(sysTime.hour))
            		confhhg.write(chr(0))
           		confhhg.write(chr(sysTime.second))
            		confhhg.write(chr(sysTime.minute))
			confhhg.close()

class start_HHG_dialog:

	def __init__( self ):
		self.timer = timer();	
		self.builder = Gtk.Builder()
		self.builder.add_from_file("/home/hany/HedgeHog/nocdc/HHG/Start.ui")
		self.logger = self.builder.get_object("Logger")
		self.cal = self.builder.get_object("Cal")
		dic = {
			"on_Logger_destroy" : self.Quit,
			"on_ConfirmButton_clicked": self.StartLogging,
			"on_Cal_day_selected": self.CalDayClick,
		}
		self.builder.connect_signals(dic)

		self.logger.show_all()

		self.startpath = sys.argv[1]
		self.confpath = sys.argv[1].replace("start.now","config.ure")
		#print(self.confpath)
		#print(self.startpath)
        	self.stpTime = []
        	self.timer.calcStpTime(self.stpTime)
        	#print(self.stpTime)
		self.cal.clear_marks()
   		self.cal.select_month(self.stpTime[1]-1, self.stpTime[0])	
		self.cal.mark_day(self.stpTime[2])

    	def CalDayClick(self, widget): 
		self.cal.clear_marks()
		self.stpTime = list(self.cal.get_date())
		self.stpTime[1] = self.stpTime[1]+1	
		#print(self.stpTime)
		self.cal.mark_day(self.stpTime[2])

	def StartLogging(self, widget):
		self.timer.setTime(self.confpath, self.stpTime)	
		with open (self.startpath,"r+w") as starthhg:
			starthhg.seek(511,0)  
			starthhg.write("l")
			starthhg.close()
			#subprocess.call(["sync"])
			#subprocess.call(["umount", sys.argv[1]]);
		sys.exit(0)	 

    	def Quit(self, widget):
        	sys.exit(0)

dialog = start_HHG_dialog()
Gtk.main()
