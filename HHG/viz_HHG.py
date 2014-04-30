#!/usr/bin/env python2.7

########################################################################
#
# Filename: viz_HHG.py   							Author: Kristof VL
#
# Descript: Vizualize a HedgeHog dataset ( database or npy )
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
import numpy as np
import hhg_plot.hhg_plot as hplt
import matplotlib.dates  as mld
import pygtk, gtk
import sqlite3
import pdb

#data descriptor for the hedgehog default data:
desc_hhg = {	'names':   ('t',  'd',  'x',  'y',  'z',  'e1', 'e2'), 
					'formats': ('f8', 'B1', 'B1', 'B1', 'B1', 'u2', 'u2') }


try:
	filename = sys.argv[1]
	ext = filename[-3:]
	ext = ext.lower()
except:
	print 'usage: viz_HHG.py <data.npy|data.db>'
	exit()
	
if ext=='npy': # simple loading of numpy file:
	dta = np.load(filename)
elif ext=='npz':
	out = np.load(filename)
	dta = out['dta']
	cnf = out['conf']
elif ext=='.db':
	## to retrieve the db data in an array:
	conn = sqlite3.connect(filename)
	cursor = conn.cursor()
	test = cursor.execute('SELECT * FROM hhg')
	dta = test.fetchall()
	dta = np.array(dta,dtype=desc_hhg)
else:
	print 'file has wrong extension'
	exit(1)
	
dta = dta.view(desc_hhg, np.recarray)
		
## actual plotting here:
fig = hplt.Hhg_raw_plot(10,8,80)
fig.plot(1, 3, dta.t, np.array((dta.x,dta.y,dta.z)).T,'3D acceleration')
fig.plot(2, 3, dta.t, np.array((dta.e1)).T>>8, 'ambient light')
fig.plot(3, 3, dta.t, (np.array((dta.e1)).T&0xFF)/2-30, 'temperature')
fig.show()

