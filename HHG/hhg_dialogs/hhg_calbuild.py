

########################################################################
#
# Filename: hhg_calbuild.py								Author: Kristof VL
#
# Descript: Maintain a dialog to inform user about calendar building
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



class Hhg_calbuild_dlg:
	def __init__(self, size_x=250, size_y=100):
		self.priter = 0
		self.maxiter= 7;
		self.dlg = gtk.Dialog("Please wait", None, 0, None)
		self.dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.dlg.set_default_response(gtk.RESPONSE_CANCEL)
		self.dlg.connect("response",self.close)
		self.pbar = gtk.ProgressBar()
		self.infotxt = gtk.Label()
		self.infotxt.set_text('Building Calendar...')
		self.dlg.vbox.add(self.pbar)
		self.dlg.vbox.add(self.infotxt)
		self.dlg.set_size_request(size_x, size_y)
		self.quitnow = False
		self.dlg.show_all()
		while gtk.events_pending(): gtk.main_iteration()
	def on_cancel(self):
		gtk.main_quit()
	def update_prgs(self,str):
		self.infotxt.set_text(str)
		self.priter += 1
		self.pbar.set_fraction(float(self.priter%self.maxiter)/self.maxiter)
		while gtk.events_pending(): gtk.main_iteration()
	def set_it(self,val):
		self.maxiter = val;
	def close(self, dta=[], msg=[]):
		self.quitnow = True;
		self.dlg.destroy()
		while gtk.events_pending(): gtk.main_iteration()


