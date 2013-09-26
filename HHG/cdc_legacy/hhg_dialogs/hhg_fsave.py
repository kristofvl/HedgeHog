

########################################################################
#
# Filename: hhg_fsave.py								Author: Kristof VL
#
# Descript: Maintain a dialog to pick a data file to save to
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
   


import gtk







#open a HedgeHog file via a pygtk dialog
def hhg_fsave(default_file=''):
	dlg = gtk.FileChooserDialog(title="Save as..", 
								action = gtk.FILE_CHOOSER_ACTION_SAVE,
								buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
											 gtk.STOCK_SAVE, gtk.RESPONSE_OK) )
	dlg.set_default_response(gtk.RESPONSE_OK)
	filter_npy = gtk.FileFilter()
	filter_npy.set_name("npy")
	filter_npy.add_mime_type("hedgehog/npy")
	filter_npy.add_pattern("*.npy")
	dlg.add_filter(filter_npy)

	filter_csv = gtk.FileFilter()
	filter_csv.set_name("csv")
	filter_csv.add_mime_type("hedgehog/csv")
	filter_csv.add_pattern("*.csv")
	dlg.add_filter(filter_csv)

	dlgres = dlg.run()
	if dlgres == gtk.RESPONSE_OK:
		filename = dlg.get_filename()
		filter = dlg.get_filter().get_name()
	else:
		filename = ''
	dlg.destroy()
	return filename,filter
