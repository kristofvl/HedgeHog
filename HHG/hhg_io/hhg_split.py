#######################################################################
#																	  
# (c) Enzo Torella for ESS											  
# www.ess.tu-darmstadt.de											  
#																	  
# hhg_split.py											          
# 
# Descript: Splits the numpy file into several numpy files of days.
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
#######################################################################

import numpy as np
import os
import shutil
from matplotlib.dates import num2date
import re
import pygtk, gtk

homedir=os.path.expanduser("~")
dst=os.path.join(homedir,'HHG')

#-----------------------------------------------------------------------

#'splithhg calls the function splitting fot the input files
def splithhg(joindta, joinfta):
	# open progress bar:
	pgrsdlg = gtk.Dialog("Splitting...", None, 0, None)
	pbar = gtk.ProgressBar()
	pgrsdlg.vbox.add(pbar)
	pgrsdlg.set_size_request(250, 50)
	pbar.show()
	pgrsdlg.vbox.show()
	pgrsdlg.show()
	while gtk.events_pending(): gtk.main_iteration()

	#in directory HHG the main program controls if there's some 
	#directories reporting the date. If directories exists, the main 
	#programm returns the last day, else it reports nday(number day)
	# as 1,that is the first day
	
	dirlst=[d for d in os.listdir(dst) if d.isdigit()]
	dirlst.sort()
	
	if not dirlst==[]:
		lastdir=dirlst[-1]
		outper=os.path.join(dst, lastdir)
	
		n_arr= str(os.listdir(outper))
		print n_arr
		jj=re.findall('\d+', n_arr)
		nday= int(jj[0])
	else:
		nday = 1
	
	posi1 = find_pos(joindta)
	posi2 = find_pos(joinfta)

	if len(posi2) < len(posi1):
		posi2.append(len(joinfta))
	
	splitting(joindta,posi1,nday, posi2, joinfta)
	pgrsdlg.hide()
	pgrsdlg.destroy()
	while gtk.events_pending(): gtk.main_iteration()
	
	return True

#-----------------------------------------------------------------------
#this function takes as input a npy file, takes the first element, that
#is the floating point and converts it into an integer which indicates 
#the day, then it sums it with one and put into a list the position 
#where the day before is, and so on, it continues until it slides the 
#whole numpy array. It returns a list containing the positions of the 
#days
def find_pos(fil):	
	lst=[]
	n=int(fil[0][0])+1
	c=1
	while True:
		t=np.where(fil['t']<n)
		
		if len(t[0])==len(fil):
			return lst
		lst.append(len(t[0]))
		n += 1

#-----------------------------------------------------------------------
#this function takes as input a 'npy file', creates a directory referred
# to the day included in the file. If this directory existed before, 
#it returns the existing directory and boo as true, else returns the new
# directory and boo as false 	
def creadir(fle):
	boo = False
	outdir=os.path.join(homedir,'HHG')
	fdir=''
	if not os.path.exists(outdir):
		os.makedirs(outdir)
	if len(fle) == 0:
		return fdir, boo
	else:
		pel=fle[0]
		rs = pel[0]
		hh=num2date(rs)
		b = '%02d' % hh.month
		a=str(hh.year)
		c='%02d' % hh.day
		stringa=a+b+c
		fdir=os.path.join(dst,stringa)
	if not os.path.exists(fdir):
		os.makedirs(fdir)
	else:
		boo = True
	return fdir, boo

#-----------------------------------------------------------------------
#the function splits joindta and joinfta into days, always as numpy files
def splitting(joindta, pos1, d, pos2, joinfta):
	j=0
	xx=0
	k=0
	for i in pos1:
		ind=pos2[k]
		
		outpath, boo = creadir(joindta[j:i-1])
	
		if (boo):
			#day dataset
			fst=(os.path.join(outpath,'day%03d.npy' % d))
			outday=np.load(fst)
			joinday=np.concatenate((outday, joindta[j:i-1]))
			np.save(os.path.join(outpath,'day%03d' % d),joinday)
			#preview dataset
			sst=(os.path.join(outpath,'prev%03d.npy' % d))
			outprev=np.load(sst)
			prev=np.concatenate((outprev,joinfta[xx:ind-1]))
			np.save(os.path.join(outpath, 'prev%03d' % d), prev)
		else:
			np.save(os.path.join(outpath,'day%03d' % d), joindta[j:i-1])
			np.save(os.path.join(outpath, 'prev%03d' % d),joinfta[xx:ind-1]) 
		
		xx=ind
		j=i
		k+=1
	outpath, boo = creadir(joindta[j:])
	d+=1
	np.save(os.path.join(outpath, 'day%03d' % d), joindta[j:])
	np.save(os.path.join(outpath, 'prev%03d' % d), joinfta[xx:])
	
#-----------------------------------------------------------------------
