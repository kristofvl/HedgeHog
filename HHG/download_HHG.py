#!/usr/bin/env python

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
#import wx ==> what is this for?? is not standard 
import os
#looking for the home directory of the system 
homedir=os.path.expanduser("~")
sys.path.append(os.path.join(homedir, 'HedgeHog/HHG'))
import hhg_io.hhg_import as hgi
sys.path.append('./hhg_tools')
import hhg_io.hhg_split as hhg_split
import hhg_dialogs.hhg_fopen as hhg_fopen
import shutil
import numpy as np
import pygtk, gtk
import re
import pygtk, gtk
from struct import unpack

#-------------------------------------

#here I define a class which  creates a new directory containing 
#all the log-files
def check_raw(npath):
	raw=os.path.join(npath, 'raw')

	if not os.path.exists(raw):
		os.makedirs(raw)

	list_raw=os.listdir(raw)
	list_raw.sort()
	if list_raw == []:
		first_dir=os.path.join(raw, '001')
	else:
		n = int(list_raw[-1]) + 1
		first_dir = os.path.join(raw, '%03d' % n) 
	
	os.makedirs(first_dir)
	return first_dir

#------------------------------MAIN------------------------------------#

#the tic counts how long time the programs takes
tic = time.clock()
src='/media/HEDGEHOG'

outpath = os.path.join(homedir,'HHG')

if not os.path.exists(outpath):
	os.makedirs(outpath)

extension = ".HHG"

#we have the list of the HHG files only
lst=[file for file in os.listdir(src) if file.endswith(extension)]
lst.sort()

#create the directory where to put the log files
opath = check_raw(outpath)

# open dialog:
pgrsdlg = gtk.Dialog("Downloading...", None, 0, None)
pbar = gtk.ProgressBar()
pgrsdlg.vbox.add(pbar)
pgrsdlg.set_size_request(250, 50)
pbar.show()
pgrsdlg.vbox.show()
pgrsdlg.show()
while gtk.events_pending(): gtk.main_iteration()

flst = []
k=0
for file in lst:
	flst.append(os.path.join(src,lst[k]))
	k = k+1

#first of all, in the cycle while, the main program takes the first 
#4 bytes of each log files and converts it to floating point referred to
#the timestamp. In this way we can compare the first 2 files; if the 
#timestamp of the first log file is minor than the second's we copy the
#first log files into HHG folder and we continue to compare 
#the second one and the third one and so on, else we copy only
#the log file with higher timestamp
i=0
	
while i<len(flst):
	pbar.pulse()
	while gtk.events_pending(): gtk.main_iteration()

	f=open(flst[i],"rb")
	bs=f.read(4)
	bs=unpack("%sB"%len(bs),bs)
	tme1 = hgi.hhg_convtime(bs[0],bs[1],bs[2],bs[3])
	
	if i+1 > len(flst):
		break 
	else:
	
		g=open(flst[i+1],"rb")
		bl=g.read(4)
		
		if len(bl)==0:
			shutil.copyfile(flst[i], os.path.join(opath,lst[i]))
			break
		bl=unpack("%sB"%len(bl),bl)
		tme2=hgi.hhg_convtime(bl[0],bl[1],bl[2],bl[3])
		
		if tme1<tme2:
			if os.path.isfile(os.path.join(opath, lst[i])):
				shutil.copyfile(flst[i+1], os.path.join(opath,lst[i+1]))
			else:
				shutil.copyfile(flst[i], os.path.join(opath,lst[i]))
				shutil.copyfile(flst[i+1], os.path.join(opath,lst[i+1]))
				i+=1
			continue
		else:
			shutil.copyfile(flst[i], os.path.join(opath,lst[i]))
			break
	pbar.pulse()
	while gtk.events_pending(): gtk.main_iteration()

pgrsdlg.hide()
pgrsdlg.destroy()
while gtk.events_pending(): gtk.main_iteration()	

#open/parse the data:
list_of_files = [file for file in os.listdir(opath) if file.endswith(extension)]
list_of_files.sort()

joindta=[]
#we slide the list and join all the log files inside into one file
for file in list_of_files:
	dta = hgi.hhg_import(os.path.join(opath,file))
	if joindta==[]:
		joindta = dta
		
	else:
		joindta = np.concatenate((joindta, dta))

#start splitting up the data
hhg_split.splithhg(joindta)

toc = time.clock()

stats = ('imported: ' + str(i) + ' files, ' + str(len(joindta))
				 + ' entries, format=raw' + ', time(s): ' + str(toc-tic))

print stats
#--------------------------------------------------------------------------------------------------------------

