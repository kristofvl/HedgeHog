#!/usr/bin/python2.7


import sys
from gi.repository import Gtk, GObject
import glob
import subprocess
import os

class configure:

	def readSettings(self, idEntry, rleCombo, rangeCombo, powCombo, freqCombo, modeCombo):
		confhhg_path = config_file 
		with open (confhhg_path,"r") as confhhg:
			confhhg.seek(0,0)
			idChar = confhhg.read(4)
			idEntry.set_text(idChar)
			confhhg.seek(12,0)
			rangetmp = confhhg.read(1)
			freqtmp = confhhg.read(1)
			modetmp = confhhg.read(1)
			powtmp = confhhg.read(1)
			if (rangetmp.isdigit()):
				rangeCombo.set_active(int(rangetmp))
			if (freqtmp.isdigit()):
				freqCombo.set_active(int(freqtmp))
			if (modetmp.isdigit()):
				modeCombo.set_active(int(modetmp))
			if (powtmp.isdigit()):
				powCombo.set_active(int(powtmp))
			confhhg.seek(20,0)
			rletmp = confhhg.read(1)
			if (rletmp.isdigit()):
				rleCombo.set_active(int(rletmp))
			confhhg.close()

	def writeSettings(self, idEntry, rleCombo, rangeCombo, powCombo, freqCombo, modeCombo):
		confhhg_path = config_file 
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
			confhhg.write(str(modeCombo.get_active()))
			confhhg.write(str(powCombo.get_active()))
			confhhg.seek(20,0) # Write RLE Delta
			confhhg.write(str(rleCombo.get_active()))
			confhhg.close()
		sys.exit()

	def formatCard(self):
		confhhg_path = config_file 
		with open (confhhg_path,"r+w") as confhhg:
			confhhg.seek(1023,0)  
			confhhg.write("f")
			confhhg.close()
		sys.exit()


class conf_HHG_dialog:
          	
	def __init__( self ):
		self.confer = configure()
		self.builder = Gtk.Builder()
		self.homeDir = os.environ['HOME']
		try:
				self.builder.add_from_file(self.homeDir+"/.hhg/Conf.ui")
		except:
				self.builder.add_from_file("Conf.ui")
		self.window = self.builder.get_object("HedgeHog")
		self.window.set_title("HedgeHog Configuration")
		self.window.show_all()
	
		self.idEntry = self.builder.get_object("IDEntry")
		self.rangeCombo = self.builder.get_object("RangeCombo")
		self.powCombo = self.builder.get_object("PowCombo")
		self.freqCombo = self.builder.get_object("FreqCombo")
		self.rleCombo = self.builder.get_object("RLECombo")
		self.modeCombo = self.builder.get_object("ModeCombo")

		self.stpTime = []
		self.ranges = ["-2 to +2 g","-4 to +4 g","-8 to +8 g","-16 to +16 g"]    
		self.freqs =  ["0.1Hz","5Hz","10Hz","25Hz","50Hz","100Hz","0.2kHz","0.4kHz",
			"0.8kHz","1.5kHz"]
		self.pows = ["normal","low-power","auto-sleep","low / auto"]
		self.mods = ["sampling by PIC", "sampling by sensor, raw sampling"]
		self.deltas = ["0","1","2","3","4","5","6","7"]

		dic = { "on_HedgeHog_destroy": self.Quit,
				"on_SyncButton_clicked": self.SyncButtonClick,
				"on_FormatButton_clicked": self.FormatButtonClick}
		self.builder.connect_signals(dic)

		for rang in self.ranges:
			self.rangeCombo.append_text(rang)

		for freq in self.freqs:
			self.freqCombo.append_text(freq)	
		
		for power in self.pows:
			self.powCombo.append_text(power)		
				
		for delta in self.deltas:
			self.rleCombo.append_text(delta)
			
		for mod in self.mods:
			self.modeCombo.append_text(mod)

		self.confer.readSettings(self.idEntry, self.rleCombo, self.rangeCombo, self.powCombo, self.freqCombo, self.modeCombo)					   		

	def Quit(self, widget):
		sys.exit(0)
	
	def SyncButtonClick(self, widget):
		self.confer.writeSettings(self.idEntry, self.rleCombo, self.rangeCombo, self.powCombo, self.freqCombo, self.modeCombo)
    		    		
	def FormatButtonClick(self, widget):
		self.confer.formatCard()
	
if len(sys.argv) >= 2:
	config_file = sys.argv[1]
else:	
	sys.stderr.write("Error: Execute this script with a configuration file as argument.")
	sys.exit(1)

hhg_dialog = conf_HHG_dialog()
Gtk.main()


