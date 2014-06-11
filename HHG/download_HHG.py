#!/usr/bin/env python2.7

########################################################################
#
# Filename: download_HHG.py 		Authors: Enzo Torella, HanyA, KristofVL
#
# Descript: Download from the Hedgehog as npz files. 
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
########################################################################

import sys, time, calendar, os
import numpy as np
import pygtk, gtk
import re
from struct import unpack
import glob, subprocess, shutil
from matplotlib.dates import num2date
import hhg_plot.hhg_plot as hplt
import hhg_io.hhg_import as hgi
import hhg_dialogs.hhg_scan as hgd

## buffer size: how many blocks (of 512 bytes each) do we read at once?
bufsize = 192	# takes about 0.5 seconds on a laptop

## look for the home directory of the system 
homedir=os.path.expanduser("~")

## look for an attached HedgeHog:
if len(sys.argv) < 2:
	srcdir = hgd.Hhg_scan_dlg().run()
else:
	srcdir = sys.argv[1]

## prepare the output structures:
dta = np.recarray(0, dtype=hgi.desc_hhg)
dlpath = os.path.join(homedir,'hhg_logs')
if not os.path.exists(dlpath):
	os.makedirs(dlpath)
	
## read configuration file:
filen = srcdir+'/config.URE'
# check if the conf file exists:
if os.path.isfile(filen):	
	# read config as a string:
	with open(filen, "rb") as f:
		conf = f.read(512)	# read first 512 bytes
else:
	exit(1)
dlpath = os.path.join(dlpath,conf[:4])
if not os.path.exists(dlpath):
	os.makedirs(dlpath)
itr = 50 # TODO: make this dependent on configuration

## find relevant files to be copied
flst = sorted(glob.glob(srcdir + '/log*.HHG'))
rlvlst = []
rlvlst.insert(0,0)
i=0
while i<len(flst):
	f=open(flst[i],"rb")
	bs=f.read(4)
	f.close()
	bs=unpack("%sB"%len(bs),bs)
	tme1 = hgi.hhg_convtime(bs[0],bs[1],bs[2],bs[3])
	if not tme1:
		print ('No data found on HedgeHog')
		sys.exit() 
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
print 'Relevant Log files ' + str(flst[0:len(rlvlst)])
loglst = flst[0:len(rlvlst)]


## read the HHG data file(s) and show progress plot to inform user
file_iter = 0
old_day = 0
first_dayid = -1
## plotting init:
fig = hplt.Hhg_load_plot(10,8,80)
## loop over input files:
while len(loglst) > file_iter:
	filename = loglst[file_iter]
	i = 0; # buffer counter
	dta_s = 0
	if file_iter==0:
		# init plot with first buffer:
		bdta = hgi.hhg_import_n(filename, 0, 1)
		fig.plot(bdta, filename, conf)
	while True:
		############################################################
		tic = time.clock()
		bdta = hgi.hhg_import_n(filename, i, i+bufsize)
		toc = time.clock()
		## report:
		if len(bdta)>0:
			bdta_l = len(bdta)
			bdta_s = sum(bdta.d)
			if first_dayid < 0:
				first_dayid = int(bdta.t[0])
			dta_s += bdta_s
			stats =  ( str(num2date(bdta.t[0]))[0:22]
					+ ': read '+ str(bdta_s).zfill(7) 
					+ ' samples in ' + str(bdta_l).zfill(7)
					+ ' rle entries, in ' +str(toc-tic)+' seconds, ' 
					+ str(len(dta)).zfill(10) + ' ' 
					+ str(dta_s).zfill(10) )
		else:
			stats = ''
			break 
		print stats
		## update plot: ###########################################
		new_day = int(bdta.t[-1])
		if old_day!=new_day:
			old_day = new_day
			## first plot the remains of the last day and save: ###
			tt = len([x for x in bdta.t if x<int(bdta.t[-1])])
			dta =np.append(dta,bdta[:tt]).view(hgi.desc_hhg,np.recarray)
			if tt>0:
				fig.update_plot(dta[::itr], stats)
			if len(dta)>0:
				daypath =hgi.hhg_store(dlpath, int(dta.t[0]), dta, conf)
				if daypath=='':
					print 'warning: could not write to '+	dlpath
			dta  = bdta[tt:].view(hgi.desc_hhg, np.recarray)
		else:
			dta  = np.append(dta, bdta).view(hgi.desc_hhg, np.recarray)
		fig.update_plot(dta[::itr], stats)
		## stop for current file if buffer not filled ############
		if len(bdta)<126*bufsize-1:
			break; ## done, get out this infinite loop
		else:
			i+=bufsize-1
		############################################################
	file_iter+=1

## finalize output:
daypath = hgi.hhg_store(dlpath, int(dta.t[0]), dta, conf)
if daypath=='':
	print 'warning: could not write to '+	dlpath
fig.update_plot(dta[::itr], stats)

## update calendar:
subprocess.call(
	[ os.path.join(os.path.dirname(os.path.realpath(__file__)),
					"calendar_HHG.py"), 
	  dlpath, str(first_dayid)] )



