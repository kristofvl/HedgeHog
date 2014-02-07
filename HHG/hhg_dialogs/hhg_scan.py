

########################################################################
#
# Filename: hhg_fopen.py								Author: Kristof VL
#
# Descript: Maintain a dialog to pick a HedgeHog data file 
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#       
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#       
   


import pygtk, gtk
import sys, os, time
import hhg_io.hhg_import as hgi



class Hhg_scan_dlg:
	def __init__(self, size_x=250, size_y=270):
		self.dlg = gtk.Dialog("Scanning", None, 0, None)
		self.dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.dlg.set_default_response(gtk.RESPONSE_CANCEL)
		self.pbar = gtk.ProgressBar()
		self.infotxt = gtk.Label()
		self.infotxt.set_text('Scanning for HedgeHog...')
		self.dlg.vbox.add(self.pbar)
		self.dlg.vbox.add(self.infotxt)
		self.dlg.set_size_request(250, 70)
		self.dlg.show_all()
		self.priter = 0
	def update_prgs(self):
		self.priter += 1
		self.pbar.set_fraction(float(self.priter%170)/170)
		while gtk.events_pending(): gtk.main_iteration()
	def scan_dmesg(self):
		self.infotxt.set_text('Scanning for HedgeHog...')
		self.update_prgs()
		time.sleep(0.1)
		return hgi.hhg_parsedmesg()
	def scan_mount(self):
		self.infotxt.set_text('HedgeHog connected. Mounting...')
		self.update_prgs()
		time.sleep(0.1)
		return hgi.hhg_findmount()
	def scan_files(self, srcdir):
		self.infotxt.set_text('Mounted. Parsing directory...')
		self.update_prgs()
		time.sleep(0.1)
		return os.path.isfile(srcdir+'/config.ure')
	def close(self):
		self.dlg.destroy()


## open a pygtk dialog that takes care of scanning for a new hedgehog
def hhg_scan_dlg():
	dlg = gtk.Dialog("Scanning", None, 0, None)
	dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
	dlg.set_default_response(gtk.RESPONSE_CANCEL)
	pbar = gtk.ProgressBar()
	infotxt = gtk.Label()
	infotxt.set_text('Scanning for HedgeHog...')
	pgrsdlg.vbox.add(pbar)
	pgrsdlg.vbox.add(infotxt)
	pgrsdlg.set_size_request(250, 70)
	pbar.show();infotxt.show();pgrsdlg.vbox.show();pgrsdlg.show()
	dlgres = dlg.run()
	scr = dlg.get_screen()
	dlg.destroy()
	if dlgres == gtk.RESPONSE_CANCEL:
		return False
	else:
		return 
		
		
	
	return filename, scr  # add screen properties (-hacky +efficient!)



