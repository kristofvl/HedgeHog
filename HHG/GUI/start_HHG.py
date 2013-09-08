#!/usr/bin/python2.7


import sys
from gi.repository import Gtk, GObject
import subprocess

class start_HHG_dialog:

	def __init__( self ):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("/home/hany/bin/HHG5.ui")
		self.popup = self.builder.get_object("EndDialog")
		dic = {"on_GreatButton_clicked": self.Quit, }
		self.builder.connect_signals(dic)
		with open (sys.argv[1],"r+w") as starthhg:
			starthhg.seek(511,0)  
			starthhg.write("l")
			starthhg.close()
			#subprocess.call(["sync"])
			#subprocess.call(["umount"]);

		self.popup.show_all()
	def Quit(self, widget):
      		sys.exit(0)

dialog = start_HHG_dialog()
Gtk.main()
