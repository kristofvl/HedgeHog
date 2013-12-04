#!/usr/bin/python2.7


import sys
from gi.repository import Gtk, GObject
from os import path, access, W_OK  # check: can we write to config file?
import subprocess
import time, datetime, os
from datetime import timedelta

class timer:
    
    def calcStpTime(self, stpTime):
        stpTime_struc = datetime.datetime.now()+timedelta(days=7)
        stpTime.insert(0,stpTime_struc.year)
        stpTime.insert(1,stpTime_struc.month)
        stpTime.insert(2,stpTime_struc.day)

    def setTime(self, conf_file, stpTime):
        sysTime = datetime.datetime.now()

        if (stpTime[0]<sysTime.year) or (stpTime[0]==sysTime.year and stpTime[1]<sysTime.month) or (stpTime[0]==sysTime.year and 
                        stpTime[1]==sysTime.month and stpTime[2]<sysTime.day):
            self.calcStpTime(stpTime)
        with open (conf_file, "r+w") as confhhg: 
            confhhg.seek(60,0)  # Write System Time
            confhhg.write(chr(sysTime.year-2000))
            confhhg.write(chr(0))
            confhhg.write(chr(sysTime.day))
            confhhg.write(chr(sysTime.month))
            confhhg.write(chr(sysTime.hour))
            confhhg.write(chr(0))
            confhhg.write(chr(sysTime.second))
            confhhg.write(chr(sysTime.minute))
            confhhg.seek(71,0)  # Write Stop Time
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
        self.home_dir = os.environ['HOME']
        try:
            self.builder.add_from_file(self.home_dir+"/.hhg/Start.ui")
        except:
            self.builder.add_from_file("Start.ui")
        self.logger = self.builder.get_object("Logger")
        self.cal = self.builder.get_object("Cal")
        dic = {
            "on_Logger_destroy" : self.Quit,
            "on_ConfirmButton_clicked": self.StartLogging,
            "on_Cal_day_selected": self.CalDayClick,
        }
        self.builder.connect_signals(dic)

        self.logger.show_all()

        self.conf_file = config_file
        self.stpTime = []
        self.timer.calcStpTime(self.stpTime)
        self.cal.clear_marks()
        self.cal.select_month(self.stpTime[1]-1, self.stpTime[0])
        self.cal.mark_day(self.stpTime[2])
        self.cal.select_day(self.stpTime[2])

    def CalDayClick(self, widget): 
        self.cal.clear_marks()
        self.stpTime = list(self.cal.get_date())
        self.stpTime[1] = self.stpTime[1]+1 
        self.cal.mark_day(self.stpTime[2])
        self.cal.select_day(self.stpTime[2])

    def StartLogging(self, widget):
        self.timer.setTime(self.conf_file, self.stpTime) 
        with open (self.conf_file,"r+w") as starthhg:
            starthhg.seek(1023,0)  
            starthhg.write("l")
            starthhg.close()
        sys.exit(0)  

    def Quit(self, widget):
        sys.exit(0)

if len(sys.argv) >= 2:
	config_file = sys.argv[1]
	if path.isfile(config_file) and access(config_file, W_OK):
		# great, *now* we can start:
		dialog = start_HHG_dialog()
		Gtk.main()
		sys.exit(0)
	else:
		sys.stderr.write("Error: Can't write to configuration file.")
else:	
	sys.stderr.write("Error: Supply configuration file as argument.")

sys.exit(1)


