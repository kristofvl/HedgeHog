#!/usr/bin/env python

########################################################################
#
# Filename: import_HHG.py   							Author: Kristof VL
#
# Descript: Import a HedgeHog dataset and convert to npy
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


import sys, time
from numpy import *
import hhg_plot.hhg_plot as hplt
import hhg_dialogs.hhg_fopen as hhg_fopen
import hhg_io.hhg_import as hgi
import matplotlib.dates  as mld
import pygtk, gtk

import pdb

#data descriptor for the hedgehog default data:
desc_hhg = {	'names':   ('t',  'd',  'x',  'y',  'z',  'e1', 'e2'), 
					'formats': ('f8', 'B1', 'B1', 'B1', 'B1', 'u2', 'u2') }

#check where to load from (default is the 1st HedgeHog's data):
filename, scr = hhg_fopen.load('/media/HEDGEHG0123/log000.HHG')

# buffer size: how many blocks (of 512 bytes each) do we read at once?
bufsize = 370	# is about 0.1 seconds on a laptop

#open/parse the data:
if len(sys.argv) == 3:
	filename = sys.argv[1]
	#read the data file
	dta = zeros(10000000,dtype=desc_hhg)
	dta = dta.view(recarray)
	if len(filename)>3:
		if filename[-3:]=='HHG':
			i = 0;
			# opening progress bar:
			pgrsdlg = gtk.Dialog("Importing...", None, 0, None)
			pbar = gtk.ProgressBar()
			infotxt = gtk.Label()
			infotxt.set_text('reading data...')
			pgrsdlg.vbox.add(pbar)
			pgrsdlg.vbox.add(infotxt)
			pgrsdlg.set_size_request(250, 70)
			pbar.show()
			infotxt.show()
			pgrsdlg.vbox.show()
			pgrsdlg.show()
			while True:
				tic = time.clock()
				bdta = hgi.hhg_import_n(filename, i, i+bufsize)
				dta[i*126:i*126+len(bdta)] = bdta
				toc = time.clock()
				if len(dta)>0:
					stats =  ( str(mld.num2date(bdta.t[0]))
							+ ' -- imported '+ str(sum(bdta.d)) 
							+ ' samples or ' + str(len(bdta))
							+ ' rle entries, in ' +str(toc-tic) + ' seconds, ' 
							+ str(126*i) + '-' + str(126*i+len(bdta)))
				else:
					stats = 'Invalid data'
				print stats
				# update progress bar:
				pbar.set_fraction(float(i%7000)/7000)
				infotxt.set_text(str(mld.num2date(bdta.t[0])))
				if len(bdta)<126*bufsize-1:
					break;
				i+=bufsize-1
				while gtk.events_pending(): gtk.main_iteration()
			dta = dta[0:126*i+len(bdta)]
			pgrsdlg.hide()
			pgrsdlg.destroy()
			save(sys.argv[2], dta)
			
else:
	print 'usage: import_HHG.py <input.HHG> <output.npy>'
	exit()



