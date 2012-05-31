#!/usr/bin/env python

########################################################################
#
# Filename: comp_HHG.py   								Author: Enzo Torella 
#
# ATTENTION:
# You should always import your data in the right order! 
#
# Descript: Convert the log files, split the data into days and save 
#		    them as a numpy file in the users home folder in 'HHG'.
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
#looking for the home directory of the system
homedir=os.path.expanduser("~")
sys.path.append(os.path.join(homedir, 'HedgeHog/HHG'))
import hhg_io.hhg_import as hgi
sys.path.append('./hhg_tools')
import hhg_split as hhg_tools
import hhg_dialogs.hhg_fopen as hhg_fopen
import numpy as np
import pygtk, gtk
import re
from struct import unpack

#----------------------------------------------------------------------#


#this function opens a dialog in which you can choose the directory to 
#use and returns this directory
def sel_dir():

	try:
		dialog = gtk.FileChooserDialog("Select directory with HHG files...",
		                               None,
		                               gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
		                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
		                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
		    return dialog.get_filename()
		else:
			return []
	finally:
		dialog.destroy()
#------------------------------MAIN------------------------------------#

#the tic counts how long time the programs takes
tic = time.clock()

#the source we've selected
src=sel_dir()

if src==[]:
	print 'No directory specified!'
	sys.exit()
	
outpath = os.path.join(homedir,'HHG')

if not os.path.exists(outpath):
	os.makedirs(outpath)
extension = ".HHG"

#in the list 'lst' we have all the HHG files
lst=[file for file in os.listdir(src) if file.endswith(extension)]
lst.sort()

flst = []
k=0
for file in lst:
	flst.append(os.path.join(src,lst[k]))
	k = k+1

#in the cycle while we can read the first 4 bytes of the first log file,
#that is the timestamp and convert it into floating point, so we can do 
#the same with the second one, and compare them; if the first timestamp
#is minor than the second one, we import all two timestamps, otherwise 
# just the first one and so on...  
i=0
jj=[]	
while i<len(flst):
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
			
			break
		bl=unpack("%sB"%len(bl),bl)
		tme2=hgi.hhg_convtime(bl[0],bl[1],bl[2],bl[3])
		
	#here we append all log files into a list	
	if tme1<tme2:
		if os.path.isfile(os.path.join(src, lst[i])):
			jj.append(lst[i])
		else:
			jj.append(lst[i])
			jj.append(lst[i+1])
		i+=1
		
		continue
	else:
		jj.append(lst[i])
		
		break
			
#open/parse the data:
#we slide the list and join all the log files inside into one file
joindta=[]
for file in jj:
	dta = hgi.hhg_import(os.path.join(src,file))
	print dta.dtype
	if joindta==[]:
		joindta = dta
		
	else:
		joindta = np.concatenate((joindta, dta))

#start splitting up the data
hhg_tools.splithhg(joindta)

toc = time.clock()

stats = ('imported: ' + str(i) + ' files, ' + str(len(joindta))
				 + ' entries, format=raw' + ', time(s): ' + str(toc-tic))

print stats
#----------------------------------------------------------------------#

