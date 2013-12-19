#!/usr/bin/env python2.7

########################################################################
#
# Filename: import_HHG.py   							Author: Kristof VL
#
# Descript: Import a HedgeHog dataset and import to a db, npy or npz
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


import sys, time, os
import numpy as np
from matplotlib.dates import num2date
import hhg_io.hhg_import as hgi
import hhg_plot.hhg_plot as hplt
import matplotlib.dates  as mld
import pygtk, gtk
import sqlite3
import pdb

#data descriptor for the hedgehog default data:
desc_hhg = {	'names':   ('t',  'd',  'x',  'y',  'z',  'e1', 'e2'), 
					'formats': ('f8', 'B1', 'B1', 'B1', 'B1', 'u2', 'u2') }

# buffer size: how many blocks (of 512 bytes each) do we read at once?
bufsize = 192	# takes about 0.5 seconds on a laptop

#open/parse the data:
if len(sys.argv) < 3:
	print 'usage: import_HHG.py <out.[npy|db]> <in0.HHG> [<in1.HHG> ..]'
	exit(1)
outfile  = sys.argv[1]

## output to a numpy file or db? prepare the output structure:
if len(outfile)>3:
	ext = outfile[-3:]
	ext = ext.lower()
	if   ext=='.db':
		conn = sqlite3.connect(outfile)
		cur  = conn.cursor()
		# if not there yet: create new db table
		cur.execute("""SELECT name FROM sqlite_master 
							WHERE type='table' AND name='hhg'""")
		res = cur.fetchone()
		if res==None:
			cur.execute("""CREATE TABLE hhg (time real, time_d integer,
								acc_x integer, acc_y integer, acc_z integer, 
								env1 integer, env2 integer)""")
	elif ext=='npy':
		dta = np.zeros(10000000,dtype=desc_hhg)
		dta = dta.view(np.recarray)
	elif ext=='npz':
		dta = np.zeros(10000000,dtype=desc_hhg)
		dta = dta.view(np.recarray)
		# configuration string (convertable to struct)
		conf = ''
	else:
		exit(1)
else:
	exit(1)
	
## read the HHG data file(s)
dta_i = 0
firstplot=0
file_iter = 1
dta_t = dta_x = dta_y = dta_z = dta_e1 = dta_e2 = []
## plotting init:
fig = hplt.Hhg_main_plot(10,8,80)
## loop over input files:
while len(sys.argv) > file_iter+1:
	file_iter+=1
	filename = sys.argv[file_iter]
	i = 0;
	if len(filename)>3:
		if filename[-3:]=='HHG':
			# read configuration if we're reading from a hedgehog:
			if len(filename)>=10:
				if filename[-10:-5]=='log00':
					filen = filename[:-10]+'config.ure'
					# check if the conf file exists:
					if os.path.isfile(filen):	
						# read config as a string:
						with open(filen, "rb") as f:
							conf = f.read(512)	# read first 512 bytes
			while True:
				tic = time.clock()
				bdta = hgi.hhg_import_n(filename, i, i+bufsize)
				## update output:
				if   ext=='.db': # insert multiple records in db:
					cur.executemany("INSERT INTO hhg VALUES (?,?,?,?,?,?,?)", 
											bdta.tolist())
					conn.commit()
				elif ext=='npy' or ext=='npz': # update npy output recarray: 
					dta[dta_i:dta_i+len(bdta)] = bdta
				toc = time.clock()
				## report:
				if len(bdta)>0:
					stats =  ( str(num2date(bdta.t[0]))
							+ ' -- imported '+ str(sum(bdta.d))
							+ ' samples or ' + str(len(bdta))
							+ ' rle entries, in ' +str(toc-tic) + ' seconds, ' 
							+ str(dta_i) + '-' + str(dta_i+len(bdta)))
				else:
					stats = ''
				print stats
				## update plot:
				itr = 50 # TODO: make this dependent on configuration
				dta_t = np.append(dta_t, bdta.t[::itr])
				dta_x = np.append(dta_x, bdta.x[::itr])
				dta_y = np.append(dta_y, bdta.y[::itr])
				dta_z = np.append(dta_z, bdta.z[::itr])
				dta_e1 = np.append(dta_e1, bdta.e1[::itr]>>8)
				dta_e2 = np.append(dta_e2, bdta.e2[::itr])
				if firstplot:
					fig.update_plot(dta_t, dta_x, dta_y, dta_z, 
										dta_e1, dta_e2, stats)
				else:
					fig.plot(dta_t, dta_x, dta_y, dta_z, 
								dta_e1, dta_e2, filename, conf)
					firstplot = 1
				## stop for current file if we didn't fill the full buffer:
				if len(bdta)<126*bufsize-1:
					dta_i = dta_i + len(bdta)
					break;
				else:
					i+=bufsize-1
					dta_i+=len(bdta)
		
## finalize output:
if   ext=='npy':
	dta = dta[0:dta_i]
	np.save(outfile, dta)
elif ext=='npz':
	dta = dta[0:dta_i]
	np.savez(outfile, dta=dta, conf=conf)
elif ext=='.db':
	conn.commit()
	cur.close()
