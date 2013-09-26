

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
import sys, os
import hhg_io.hhg_import as hgi





#open a HedgeHog file via a pygtk dialog
def load(def_hhg_file='/media/HEDGEHOG/log000.HHG'):
	#check first whether a filename was passed through the command line:
	try:
		no_argument = False
		open(sys.argv[1])
		filename = sys.argv[1]
	except IndexError as e:
		no_argument = True
	except IOError as e:
		no_argument = True
		print 'File given as argument does not open.'
	#otherwise pick data file(s) in GUI, merge multiple files, load data:
	if no_argument:
		filenames, scr = hhg_fopen(def_hhg_file)
		filename = hgi.hhg_merge_HHGs(filenames, 
								os.path.join(os.getenv("HOME"),'temp.HHG') )
	else:
		scr = hhg_getscr()
	# return selected file plus screen stats	
	return filename, scr	

#open a HedgeHog file via a pygtk dialog
def hhg_fopen(default_file=''):
	# check if the default file exists 
	try:
		open(default_file)
		# if it exists -> ask for confirmation to use it
		dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, 
									gtk.BUTTONS_NONE, 'Open '+default_file+' ?')
		dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		dlg.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_OK)
		dlg.set_default_response(gtk.RESPONSE_OK)
		dlgres = dlg.run()
		scr = dlg.get_screen()
		dlg.destroy()
		if dlgres == gtk.RESPONSE_OK:
			filename = [default_file]
		else:
			filename = []
			raise IOError('')
	except IOError as e:
 	# if the default does not exist or cancelled: file open dialog:
		dlg = gtk.FileChooserDialog(title = "Open..", 
						action = gtk.FILE_CHOOSER_ACTION_OPEN,
						buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
									  gtk.STOCK_OPEN, gtk.RESPONSE_OK)  )
		dlg.set_default_response(gtk.RESPONSE_OK)
		dlg.set_select_multiple(True)
		filter_HHG = gtk.FileFilter()
		filter_HHG.set_name("HHG")
		filter_HHG.add_mime_type("hedgehog/hhg")
		filter_HHG.add_pattern("*.HHG")
		dlg.add_filter(filter_HHG)
		filter_npy = gtk.FileFilter()
		filter_npy.set_name("npy")
		filter_npy.add_mime_type("hedgehog/npy")
		filter_npy.add_pattern("*.npy")
		dlg.add_filter(filter_npy)
		dlgres = dlg.run()
		if dlgres == gtk.RESPONSE_OK:
			filename = dlg.get_filenames() # .. or use the selected file(s)
		else:
			filename = []
		scr = dlg.get_screen()
		dlg.destroy()
	return filename, scr  # add screen properties (-hacky +efficient!)


#hacky function that asks gtk for the screen size
def hhg_getscr():
	dlg = gtk.Dialog(None)
	scr = dlg.get_screen()
	dlg.destroy()
	return scr

