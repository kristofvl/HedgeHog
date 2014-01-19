#!/usr/bin/env python2.7

########################################################################
#
# Filename: download_HHG.py 							Author: Enzo Torella 
#
#
# Descript: Download from the Hedgehog, convert the log files, split 
# 			the data into days and save them as a numpy file in the 
#			users home folder in 'HHG'. The log files are being stored
#			in 'HHG/raw'.
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
#######################################################################

import sys, time
import os
import hhg_io.hhg_import as hgi
import hhg_io.hhg_split as hhg_split
import hhg_dialogs.hhg_fopen as hhg_fopen
import numpy as np
import pygtk, gtk
import re
from struct import unpack
import glob
import subprocess 
import shutil
from numpy import *
from matplotlib.dates import num2date
import sqlite3
import pdb

#------------------------------------------------------------------------------#

#looking for the home directory of the system 
homedir=os.path.expanduser("~")

src = glob.glob('/media/essuser/HEDG*')[0]
print 'HedgeHog Device found at ' + src

outpath = os.path.join(homedir,'Logs')

if not os.path.exists(outpath):
	os.makedirs(outpath)

extension = ".HHG"

flst = sorted(glob.glob(src + '/log*.HHG'))
#print flst

#find relevant files to be copied
rlvlst = []
rlvlst.insert(0,0)
i=0

# opening progress bar:
pgrsdlg = gtk.Dialog("Scanning...", None, 0, None)
pbar = gtk.ProgressBar()
infotxt = gtk.Label()
infotxt.set_text('scanning data...')
pgrsdlg.vbox.add(pbar)
pgrsdlg.vbox.add(infotxt)
pgrsdlg.set_size_request(250, 70)
pgrsdlg.show_all()
while gtk.events_pending(): gtk.main_iteration()

while i<len(flst):

	f=open(flst[i],"rb")
	bs=f.read(4)
	f.close()
	bs=unpack("%sB"%len(bs),bs)
	tme1 = hgi.hhg_convtime(bs[0],bs[1],bs[2],bs[3])
	
	if i+1 >= len(flst):
		break 

	else:
		g=open(flst[i+1],"rb")
		bl=g.read(4)
		g.close()

		if len(bl)==0:
			break

		bl=unpack("%sB"%len(bl),bl)
		tme2=hgi.hhg_convtime(bl[0],bl[1],bl[2],bl[3])
		
		if tme1<tme2:
			rlvlst.insert(i+1,i+1)
			i+=1
		else:
			break
	## update progress bar:
	time.sleep(1)
	pbar.set_fraction(float(i%len(flst))/len(flst))
	while gtk.events_pending(): gtk.main_iteration()

pbar.set_fraction(1)
while gtk.events_pending(): gtk.main_iteration()

time.sleep(2)

print 'Relevant Log files ' + str(flst[0:len(rlvlst)])
pgrsdlg.hide()
pgrsdlg.destroy()

loglst = flst[0:len(rlvlst)]
# print loglst

#------------------------------------------------------------------------------#

outext = 'npy'
outname = 'HEDHG'

#data descriptor for the hedgehog default data:
desc_hhg = {	'names':   ('t',  'd',  'x',  'y',  'z',  'e1', 'e2'), 
					'formats': ('f8', 'B1', 'B1', 'B1', 'B1', 'u2', 'u2') }

# buffer size: how many blocks (of 512 bytes each) do we read at once?
bufsize = 370	# takes about 0.5 seconds on a laptop

## output to a numpy file or db? prepare the output structure:
if outext=='.db':
	conn = sqlite3.connect(outname+outext)
	cur = conn.cursor()
	# if not there yet: create new db table
	cur.execute("""SELECT name FROM sqlite_master 
						WHERE type='table' AND name='hhg'""")
	res = cur.fetchone()
	if res==None:
		cur.execute("""CREATE TABLE hhg (time real, time_d integer,
							acc_x integer, acc_y integer, acc_z integer, 
							env1 integer, env2 integer)""")
if outext=='npy':
	dta = zeros(10000000,dtype=desc_hhg)
	dta = dta.view(recarray)
	
# opening progress bar:
pgrsdlg = gtk.Dialog("Importing...", None, 0, None)
pbar1 = gtk.ProgressBar()
pbar2 = gtk.ProgressBar()
infotxt1 = gtk.Label()
infotxt1.set_text('file progress...')
infotxt2 = gtk.Label()
infotxt2.set_text('reading data...')
pgrsdlg.vbox.add(pbar1)
pgrsdlg.vbox.add(infotxt1)
pgrsdlg.vbox.add(pbar2)
pgrsdlg.vbox.add(infotxt2)
pgrsdlg.set_size_request(250, 140)
pgrsdlg.show_all()
while gtk.events_pending(): gtk.main_iteration()

time.sleep(2)

## read the HHG data file(s)
dta_i = 0;
file_iter = 0

while len(loglst) >= file_iter+1:

	pbar1.set_fraction(float(file_iter%len(loglst))/len(loglst))
	while gtk.events_pending(): gtk.main_iteration()

	filename = loglst[file_iter]
	file_iter+=1
	print filename
	i = 0;
	if len(filename)>3:
		if filename[-3:]=='HHG':
			while True:
				tic = time.clock()
				bdta = hgi.hhg_import_n(filename, i, i+bufsize)
				## update output:
				if   outext=='.db': # insert multiple records in db:
					cur.executemany("INSERT INTO hhg VALUES (?,?,?,?,?,?,?)", 
											bdta.tolist())
					conn.commit()
				elif outext=='npy': # update npy output recarray: 
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
				## update progress bar:
				pbar2.set_fraction(float(i%7000)/7000)
				infotxt2.set_text(str(num2date(bdta.t[0])))
				while gtk.events_pending(): gtk.main_iteration()
				## stop for current file if we didn't fill the full buffer:
				if len(bdta)<126*bufsize-1:
					dta_i = dta_i + len(bdta)
					pbar2.set_fraction(1)
					while gtk.events_pending(): gtk.main_iteration()
					break;
				else:
					i+=bufsize-1
					dta_i+=len(bdta)

pbar1.set_fraction(1)
while gtk.events_pending(): gtk.main_iteration()
time.sleep(2)
## get rid of the progress dialog and finish:
pgrsdlg.destroy()

## finalize output:
if   outext=='npy':
	dta = dta[0:dta_i]
	save(outname, dta)
elif outext=='.db':
	conn.commit()
	cur.close()

#------------------------------------------------------------------------------#
