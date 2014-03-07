#!/usr/bin/env python2.7


import sys
import gtk, gobject
import glob
import subprocess
import os
import hhg_dialogs.hhg_scan as hgd
import string

class configure:

	def readSettings(self, idEntry, rleCombo, rangeCombo, powCombo, freqCombo, modeCombo, version, window):
		confhhg_path = config_file 
		with open (confhhg_path,"r") as confhhg:
			confhhg.seek(0,0)
			idChar = confhhg.read(4)
			if all(ch in string.printable for ch in idChar):
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
			confhhg.seek(35,0)
			version = confhhg.read(7)
		        if all(ch in string.printable for ch in version):
				window.set_title("HedgeHog Configuration " + version)
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
			#confhhg.write(str(modeCombo.get_active()))
			confhhg.write(str(1))
			confhhg.write(str(powCombo.get_active()))
			confhhg.seek(20,0) # Write RLE Delta
			confhhg.write(str(rleCombo.get_active()))
			confhhg.seek(1023,0)
			confhhg.write("c")
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
		self.version = ""
		self.conf = configure()
		self.builder = gtk.Builder()
		self.homeDir = os.environ['HOME']
		try:
				self.builder.add_from_file(self.homeDir+"/.hgg/conf.ui")
		except:
				self.builder.add_from_file("conf.ui")
		self.window = self.builder.get_object("HedgeHog")
		self.window.set_title("HedgeHog Configuration" + self.version)
		self.window.show_all()
	
		self.idEntry = self.builder.get_object("IDEntry")
		self.rangeCombo = self.builder.get_object("RangeCombo")
		self.powCombo = self.builder.get_object("PowerCombo")
		self.freqCombo = self.builder.get_object("FreqCombo")
		self.rleCombo = self.builder.get_object("DeltaCombo")
		self.modeCombo = self.builder.get_object("ModeCombo")

		self.stpTime = []
		self.ranges = ["-2 to +2 g","-4 to +4 g","-8 to +8 g","-16 to +16 g"]    
		self.freqs =  ["0.1Hz","5Hz","10Hz","25Hz","50Hz","100Hz","0.2kHz","0.4kHz",
			"0.8kHz","1.5kHz"]
		self.pows = ["normal","low-power","auto-sleep","low / auto"]
		self.modes = ["sampling by PIC", "sampling by sensor, raw sampling"]
		self.deltas = ["0","1","2","3","4","5","6","7"]

		self.rangeStore = gtk.ListStore(gobject.TYPE_STRING)
		for rang in self.ranges:
			self.rangeStore.append([rang])
		self.rangeCombo.set_model(self.rangeStore)
		cell = gtk.CellRendererText()
		self.rangeCombo.pack_start(cell, True)
		self.rangeCombo.add_attribute(cell,"text",0)
		self.rangeCombo.set_active(1)

		self.powStore = gtk.ListStore(gobject.TYPE_STRING)
		for power in self.pows:
			self.powStore.append([power])
		self.powCombo.set_model(self.powStore)
		self.powCombo.pack_start(cell, True)
		self.powCombo.add_attribute(cell,"text",0)
		self.powCombo.set_active(3)

		self.freqStore = gtk.ListStore(gobject.TYPE_STRING)
		for freq in self.freqs:
			self.freqStore.append([freq])
		self.freqCombo.set_model(self.freqStore)
		self.freqCombo.pack_start(cell, True)
		self.freqCombo.add_attribute(cell,"text",0)
		self.freqCombo.set_active(3)

		self.deltaStore = gtk.ListStore(gobject.TYPE_STRING)
		for delta in self.deltas:
			self.deltaStore.append([delta])
		self.rleCombo.set_model(self.deltaStore)
		self.rleCombo.pack_start(cell, True)
		self.rleCombo.add_attribute(cell,"text",0)
		self.rleCombo.set_active(1)

		self.modeStore = gtk.ListStore(gobject.TYPE_STRING)
		for mode in self.modes:
			self.modeStore.append([mode])
		cell = gtk.CellRendererText()
		self.modeCombo.set_model(self.modeStore)
		self.modeCombo.pack_start(cell, True)
		self.modeCombo.add_attribute(cell,"text",0)
		self.modeCombo.set_active(1)

		dic = { "on_HedgeHog_destroy": self.Quit,
				"on_SyncButton_clicked": self.SyncButtonClick,
				"on_FormatButton_clicked": self.FormatButtonClick}
		self.builder.connect_signals(dic)


		self.conf.readSettings(self.idEntry, self.rleCombo, self.rangeCombo, self.powCombo, self.freqCombo, self.modeCombo, self.version, self.window)					   		

	def Quit(self, widget):
		sys.exit(0)
	
	def SyncButtonClick(self, widget):
		self.conf.writeSettings(self.idEntry, self.rleCombo, self.rangeCombo, self.powCombo, self.freqCombo, self.modeCombo)
    		    		
	def FormatButtonClick(self, widget):
		self.conf.formatCard()
	
if len(sys.argv) >= 2:
	config_file = sys.argv[1]
else: ## look for an attached HedgeHog:
	config_file = hgd.Hhg_scan_dlg().run()+'/config.URE'

hhg_dialog = conf_HHG_dialog()
gtk.main()


