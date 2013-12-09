#!/usr/bin/env python

########################################################################
#
# Filename: plot_HHG.py   								Author: Kristof VL
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
import hhg_dialogs.hhg_fopen as hhg_fopen
import hhg_io.hhg_import as hgi

import pdb


# buffer size:
bufsize = 500

#open/parse the data:
if len(sys.argv) == 2:
	filename = sys.argv[1]
	#read the data file
	dta = []
	if len(filename)>3:
		if filename[-3:]=='HHG':
			i = 0;
			while True:
				tic = time.clock()
				dta = hgi.hhg_import_n(filename, i, i+bufsize)
				toc = time.clock()
				if len(dta)>0:
					stats =  ('imported '+ str(sum(dta.d)) + ' samples or ' 
							+ str(len(dta))
							+ ' rle entries, in ' +str(toc-tic) + 'seconds')
				else:
					stats = 'Invalid data'
					break
				print stats
				i+=bufsize
else:
	print 'please use an HHG file as argument'
	exit()


