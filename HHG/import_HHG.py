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


import sys, time, os, math
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
	print 'use: import_HHG.py [out.<npy|npz|db>] [in0.HHG] <in1.HHG ..>'
	exit(1)

## output to a numpy file or db? prepare the output structure:
outfile  = sys.argv[1]
try:
	ext = outfile[-3:]
except:
	exit(1)
else:
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
	
## read the HHG data file(s)
dta_i = 0
firstplot=0
file_iter = 1
dta_ = np.recarray(0, dtype=desc_hhg)
old_day = 0
## plotting init:
fig = hplt.Hhg_load_plot(10,8,80)
## loop over input files:
while len(sys.argv) > file_iter+1:
	file_iter+=1
	filename = sys.argv[file_iter]
	i = 0; # buffer counter
	dta_s = 0
	if len(filename)>3:
		if filename[-3:]=='HHG':
			# read configuration if we're reading from a hedgehog:
			if len(filename)>=10:
				if filename[-10:-5]=='log00':
					filen = filename[:-10]+'config.URE'
					# check if the conf file exists:
					if os.path.isfile(filen):	
						# read config as a string:
						with open(filen, "rb") as f:
							conf = f.read(512)	# read first 512 bytes
			if file_iter==2:
				bdta = hgi.hhg_import_n(filename, 0, 1)
				fig.plot(bdta, filename, conf)
			while True:
				############################################################
				tic = time.clock()
				bdta = hgi.hhg_import_n(filename, i, i+bufsize)
				## update output: #########################################
				if   ext=='.db': # insert multiple records in db:
					cur.executemany(
						"INSERT INTO hhg VALUES (?,?,?,?,?,?,?)",
						bdta.tolist())
					conn.commit()
				elif ext=='npy' or ext=='npz': # update npy output: 
					dta[dta_i:dta_i+len(bdta)] = bdta
				toc = time.clock()
				## report:
				bdta_l = len(bdta)
				bdta_s = sum(bdta.d)
				dta_s += bdta_s
				if len(bdta)>0:
					stats =  ( str(num2date(bdta.t[0]))[0:22]
							+ ': read '+ str(bdta_s).zfill(7) 
							+ ' samples in ' + str(bdta_l).zfill(7)
							+ ' rle entries, in ' +str(toc-tic)+' seconds, ' 
							+ str(dta_i+bdta_l).zfill(10) + ' ' 
							+ str(dta_s).zfill(10) )
				else:
					stats = ''
				print stats
				## update plot: ###########################################
				itr = 50 # TODO: make this dependent on configuration
				bdta_ = bdta[::itr]
				bdta_.e1 >>= 8 # ambient light
				new_day = int(bdta_.t[-1])
				if old_day!=new_day:
					old_day = new_day
					## first plot the remains of the last day: ############
					bdta_tt = [x for x in bdta_.t if x<int(bdta_.t[-1])]
					tt = len(bdta_tt)
					dta_ = np.append(dta_, 
										 bdta_[:tt]).view(desc_hhg, np.recarray)
					if tt>0:
						fig.update_plot(dta_, stats)
					dta_  = bdta_[tt:]
				else:
					dta_ = np.append(dta_, 
											bdta_).view(desc_hhg, np.recarray)
				fig.update_plot(dta_, stats)
				## stop for current file if buffer not filled ############
				if len(bdta)<126*bufsize-1:
					dta_i = dta_i + len(bdta)
					break; ## done, get out this infinite loop
				else:
					i+=bufsize-1
					dta_i+=len(bdta)
				############################################################


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
