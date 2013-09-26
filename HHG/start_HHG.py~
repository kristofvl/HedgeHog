#!/usr/bin/python2.7


import sys
from gi.repository import Gtk, GObject
import subprocess
import time, datetime, os

class start_HHG_dialog:

	def __init__( self ):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("/home/hany/HedgeHog/nocdc/HHG/Start.ui")
		self.popup = self.builder.get_object("EndDialog")
		dic = {"on_GreatButton_clicked": self.Quit, }
		self.builder.connect_signals(dic)
		self.startpath = sys.argv[1]
		self.confpath = sys.argv[1].replace("start.now","config.ure")
		#print(self.confpath)
		#print(self.startpath)
		self.sysTime = datetime.datetime.now()
		with open (self.confpath, "r+w") as confhhg: 
			confhhg.seek(59,0)  # Write System Time
			confhhg.write(chr(self.sysTime.year-2000))
			confhhg.write(chr(0))
			confhhg.write(chr(self.sysTime.day))
			confhhg.write(chr(self.sysTime.month))
			confhhg.write(chr(self.sysTime.hour))
			confhhg.write(chr(0))
			confhhg.write(chr(self.sysTime.second))
			confhhg.write(chr(self.sysTime.minute))
			confhhg.close()
		with open (self.startpath,"r+w") as starthhg:
			starthhg.seek(511,0)  
			starthhg.write("l")
			starthhg.close()
			#subprocess.call(["sync"])
			#subprocess.call(["umount", sys.argv[1]]);

		self.popup.show_all()
	def Quit(self, widget):
      		sys.exit(0)

dialog = start_HHG_dialog()
Gtk.main()
