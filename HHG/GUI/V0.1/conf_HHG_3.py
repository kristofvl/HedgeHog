#!/usr/bin/python2.7


import sys
from gi.repository import Gtk, GObject
import glob
import time, datetime, os
import subprocess
from math import exp

class configure:

    def getSysTime(self, sysTimeEntry, sysTime, stpTime):
    	sysTime = datetime.datetime.now()
    	sysTimeEntry.set_text(sysTime.strftime("%Y-%m-%d %H:%M:%S"))
	stpTime.insert(0,sysTime.year)
	stpTime.insert(1,sysTime.month)
	stpTime.insert(2,sysTime.day+7)

    def chooseHHG(self, hhgMenu, idEntry, rangeCombo, powCombo, freqCombo, sampCombo, sysTimeEntry, sysTime, stpTime, lastStartEntry, lastStpEntry):
	confhhg_path = sys.argv[1] 
	print(confhhg_path)	
        with open (confhhg_path,"r") as confhhg:
               confhhg.seek(0,0)
               idChar = confhhg.read(4)
               idEntry.set_text(idChar)
	       confhhg.seek(12,0)
	       rangeCombo.set_active(int(confhhg.read(1)))
	       freqCombo.set_active(int(confhhg.read(1)))
	       sampCombo.set_active(int(confhhg.read(1)))
	       powCombo.set_active(int(confhhg.read(1)))			       			
	       self.getSysTime(sysTimeEntry, sysTime, stpTime) 
	       confhhg.seek(59,0)	
	       lastStartTimeChar = confhhg.read(8)
	       lastStartTimeDec = [ord(lastStartTimeChar[0]),ord(lastStartTimeChar[3]),ord(lastStartTimeChar[2]),
                                ord(lastStartTimeChar[4]),ord(lastStartTimeChar[7]),ord(lastStartTimeChar[6])]
	       lastStartEntry.set_text("20%d-%d-%d %d:%d:%d" % (lastStartTimeDec[0],lastStartTimeDec[1],lastStartTimeDec[2],
							       lastStartTimeDec[3],lastStartTimeDec[4],lastStartTimeDec[5]))
	       confhhg.seek(70,0)	
	       lastStpTimeChar = confhhg.read(8)
	       lastStpTimeDec = [ord(lastStpTimeChar[0]),ord(lastStpTimeChar[3]),ord(lastStpTimeChar[2]),
                                ord(lastStpTimeChar[4]),ord(lastStpTimeChar[7]),ord(lastStpTimeChar[6])]
	       lastStpEntry.set_text("20%d-%d-%d %d:%d:%d" % (lastStpTimeDec[0],lastStpTimeDec[1],lastStpTimeDec[2],
							     lastStpTimeDec[3],lastStpTimeDec[4],lastStpTimeDec[5]))
	       confhhg.close()


    def syncSettings(self, hhgMenu, idEntry, rangeCombo, powCombo, freqCombo, sampCombo, sysTimeEntry, sysTime, stpTime, popup, warning):
	confhhg_path = sys.argv[1]	
	if (stpTime[0]<sysTime.year) or (stpTime[0]==sysTime.year and stpTime[1]<sysTime.month) or (stpTime[0]==sysTime.year and 
						stpTime[1]==sysTime.month and stpTime[2]<sysTime.day):
	      warning.run()
	      return	 
	idChar = idEntry.get_text();
	with open (confhhg_path,"r+w") as confhhg:
		confhhg.seek(0,0)   # Write ID
		confhhg.write(idChar[0])
		confhhg.write(idChar[1])
		confhhg.write(idChar[2])
		confhhg.write(idChar[3])
		confhhg.seek(12,0)  # Write ACC Settings
		confhhg.write(str(rangeCombo.get_active()))
		confhhg.write(str(freqCombo.get_active()))
		confhhg.write(str(sampCombo.get_active()))
		confhhg.write(str(powCombo.get_active()))
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
		confhhg.seek(1023,0)  # Set Flag to 'Log'
		confhhg.write("l")
		confhhg.close()
		subprocess.call(["sudo","umount", confhhg_path]);
		popup.run()

class conf_HHG_dialog:
          	
    def __init__( self ):
	self.confer = configure()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/hany/bin/HHG3.ui")
        self.window = self.builder.get_object("HedgeHog")
	self.popup = self.builder.get_object("EndDialog")	
        self.window.set_title("HedgeHog Configuration")
        self.window.set_size_request(500,300)
	self.warning = self.builder.get_object("Warning")
        self.window.show_all()
	
        self.hhgMenu = self.builder.get_object("HHGMenu")
        self.cal = self.builder.get_object("Cal")
        self.idEntry = self.builder.get_object("IDEntry")
        self.sysTimeEntry = self.builder.get_object("SysTimeEntry")
	self.lastStartEntry = self.builder.get_object("LastStart")
	self.lastStpEntry = self.builder.get_object("LastStop")
	self.rangeCombo = self.builder.get_object("RangeCombo")
	self.powCombo = self.builder.get_object("PowCombo")
	self.freqCombo = self.builder.get_object("FreqCombo")
	self.sampCombo = self.builder.get_object("SampCombo")
	self.stpTime = []
    	self.sysTime = datetime.datetime.now()
        self.devices = []
	self.ranges = ["-2 to +2 g","-4 to +4 g","-8 to +8 g","-16 to +16 g"]    
	self.freqs =  ["0.1Hz","5Hz","10Hz","25Hz","50Hz","100Hz","0.2kHz","0.4kHz",
			"0.8kHz","1.5kHz"]
	self.pows = ["normal","low-power","auto-sleep","low / auto"]
	self.samps = ["none (raw data)", "mean/variance","emSWAB","tap features"]	 

        dic = { 
           "on_HedgeHog_destroy" : self.Quit,
           "on_SysTimeButton_clicked": self.SysTimeButtonClick,
           "on_SyncButton_clicked": self.SyncButtonClick,
           "on_HHGMenu_changed": self.HHGMenuChange,
  	   "on_RefreshDevices_clicked": self.Refresh,
	   "on_GreatButton_clicked": self.Quit,
	   "on_Return_clicked": self.Collapse,	
	   "on_Cal_day_selected_double_click": self.CalDayClick,
	   "on_Cal_day_selected": self.CalDayClick,		  	
        }
        self.builder.connect_signals(dic)
	
        self.devices = sorted(glob.glob('/media/HED*'))
        for device in self.devices:
            self.hhgMenu.append_text(device)

	for rang in self.ranges:
	    self.rangeCombo.append_text(rang)

	for freq in self.freqs:
	    self.freqCombo.append_text(freq)	
		
	for power in self.pows:
	    self.powCombo.append_text(power)		
				
	for samp in self.samps:
	    self.sampCombo.append_text(samp)	

	self.confer.chooseHHG(self.hhgMenu, self.idEntry, self.rangeCombo, self.powCombo, self.freqCombo, self.sampCombo, self.sysTimeEntry, self.sysTime, self.stpTime, 			   					self.lastStartEntry,self.lastStpEntry)					   		
 
    def HHGMenuChange(self, widget):
	self.confer.chooseHHG(self.hhgMenu, self.idEntry, self.rangeCombo, self.powCombo, self.freqCombo, self.sampCombo, self.sysTimeEntry, self.sysTime, self.stpTime, 			   					self.lastStartEntry,self.lastStpEntry)

    def Refresh(self, widget):
	 for device in self.devices:
	     self.hhgMenu.remove(self.devices.index(device))
	 self.devices = sorted(glob.glob('/media/HED*'))
         for device in self.devices:
                  self.hhgMenu.append_text(device)
         self.hhgMenu.set_active(0)	

    def SysTimeButtonClick(self, widget):
	self.confer.getSysTime(self.sysTimeEntry, self.sysTime, self.stpTime)
	
    def CalDayClick(self, widget): 
	self.stpTime = list(self.cal.get_date())
	self.stpTime[1] = self.stpTime[1]+1	


    def SyncButtonClick(self, widget):
   	self.confer.syncSettings(self.hhgMenu, self.idEntry,self.rangeCombo, self.powCombo, self.freqCombo, self.sampCombo, self.sysTimeEntry, self.sysTime, self.stpTime, self.popup, self.warning)
    		    		
    def Quit(self, widget):
        sys.exit(0)
 
    def Collapse(self, widget):
	self.warning.destroy()

	
hhg_dialog = conf_HHG_dialog()
Gtk.main()


