

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
   


import pygtk, gtk, gobject
import sys, os, time
import hhg_io.hhg_import as hgi



class Hhg_scan_dlg:
	def __init__(self, size_x=250, size_y=100):
		self.dlg = gtk.Dialog("Please wait", None, 0, None)
		self.dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.dlg.set_default_response(gtk.RESPONSE_CANCEL)
		self.dlg.connect("response",self.close)
		self.pbar = gtk.ProgressBar()
		self.infotxt = gtk.Label()
		self.infotxt.set_text('Scanning for HedgeHog...')
		self.dlg.vbox.add(self.pbar)
		self.dlg.vbox.add(self.infotxt)
		self.dlg.set_size_request(size_x, size_y)
		self.quitnow = False
		self.dlg.show_all()
	def on_cancel(self):
		gtk.main_quit()
	def update_prgs(self):
		self.priter += 1
		self.pbar.set_fraction(float(self.priter%70)/70)
		while gtk.events_pending(): gtk.main_iteration()
	def scan_dmesg(self):
		self.infotxt.set_text('Scanning for HedgeHog...')
		ret = hgi.hhg_parsedmesg()
		while not ret and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_parsedmesg()
			time.sleep(0.1)
	def scan_mount(self):
		self.infotxt.set_text('HedgeHog connected. Mounting...')
		ret = hgi.hhg_findmount()
		while ret=='' and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_findmount()
			time.sleep(0.1)
		return ret
	def scan_files(self, srcdir):
		self.infotxt.set_text('Mounted. Parsing directory...')
		ret = os.path.isfile(srcdir+'/config.URE')
		while not ret and not self.quitnow:
			self.update_prgs()
			ret = os.path.isfile(srcdir+'/config.URE')
			time.sleep(0.1)
	def close(self, dta=[], msg=[]):
		self.quitnow = True;
		self.dlg.destroy()
	def run(self):
		self.priter = 0
		if not hgi.hhg_findmount():
			self.scan_dmesg()
		srcdir = self.scan_mount()
		self.scan_files(srcdir)
		self.close()
		return srcdir


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



