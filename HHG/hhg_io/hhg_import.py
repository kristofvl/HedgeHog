

########################################################################
#
# Filename: hhg_import.py								Author: Kristof VL
#
# Descript: Data import routines for HedgeHog sensor data (+progressbar)
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



import sys, os, glob, shutil, time
import numpy as np
from matplotlib.dates import date2num, num2date
from datetime import datetime
from struct import unpack
import pygtk, gtk
import subprocess

import pdb


SDRLESIZE = 126 #  sd buffer size in RLE samples:
SDBUFSIZE = 512 #  sd buffer size in bytes

## data descriptor for the hedgehog default data:
desc_hhg = {	'names':   ('t',  'd',  'x',  'y',  'z',  'e1', 'e2'), 
					'formats': ('f8', 'B1', 'B1', 'B1', 'B1', 'u2', 'u2') }	


## finds the first path where a hedgehog has been spotted
def hhg_findmount():
	try:
		lsblk = os.popen("lsblk -n -o MOUNTPOINT | grep HEDGE").read()
		if lsblk != '':
			return lsblk[0:-1]
		else:
			return ''
	except:
		return ''
		
## checks dmesg output for recent occurences of a hedgehog popping up
def hhg_parsedmesg():
	usbList = subprocess.check_output("lsusb", shell=True)
	if 'HedgeHog' in usbList: 
		return True
	else:
		return False
#	log = os.popen("dmesg -T | tail -n 30 | grep HedgeHog").read()
#	if log:
#		datestr = log[4:24]
#		datestr = datestr[:4] + datestr[5:]
#		logtime = datetime.strptime(datestr, "%b %d %H:%M:%S %Y")
#		td = datetime.now() - logtime
#		if (td.seconds < 5):
#			return True
#		else:
#			return False
#	else:
#		return False
		
## converts 4 bytes into a matplotlib timestamp
def hhg_convtime(b1,b2,b3,b4):
	try:
		dt	= datetime(	2000+((b4 & 0xFC) >> 2),					# year
						((b4 & 0x03)<<2) + ((b3 & 0xC0)>>6),		# month
						(b3 & 0x3E)>>1,									# day
						((b3 & 0x01)<<4) + ((b2 & 0xF0)>>4),		# hour
						((b2 & 0x0F)<<2) + ((b1 & 0xC0)>>6),		# minute
						(b1 & 0x3F) ) 										# seconds
		return date2num(dt)
	except ValueError:
		return False

## read the binary HHG file and convert it (datenum d x y z e1 e2)
## from page 'strt' till (and not including) page 'stop' 
def hhg_import_n(filen, strt, stop):
	pg_i = 0
	ii = 0
	tme_delta=0
	rle_samples = abs(stop-strt)*SDRLESIZE
	# check if file exists, if not exit now:
	if not os.path.isfile(filen):	return []
	# start parsing file:
	with open(filen, "rb") as f:
		f.seek(abs(strt)*SDBUFSIZE) # offset to 'strt'
		bs = f.read(8)	# read first 8 bytes
		bs = unpack('%sB'%len(bs),bs)
		dta = np.recarray((rle_samples,),dtype=desc_hhg)
		if len(bs) == 8: # parse for time and light/temp data
			tme = hhg_convtime(bs[0],bs[1],bs[2],bs[3])
			env1 = bs[5]*256+bs[4]
			env2 = bs[7]*256+bs[6]
			bs = f.read(512)
			bs = unpack('%sB'%len(bs),bs)
		invalid_data = False
		while (len(bs)==512) and ii<rle_samples and not invalid_data:
			tme_next = hhg_convtime(bs[504],bs[505],bs[506],bs[507])
			if ( (tme_next-tme) >= 0):  # time is okay:
				num_samples = sum(bs[0:504:4])
				if num_samples > 0:
					tme_delta = (tme_next - tme) / num_samples
				else:
					invalid_data = True
					break
				for j in range(0,126):
					dta[ii] = np.array((tme, bs[j*4], bs[1+(j*4)], 
											bs[2+(j*4)], bs[3+(j*4)], env1, env2), 
											dtype=desc_hhg)
					tme += bs[j*4]*tme_delta
					ii += 1
				tme = tme_next
				bs = f.read(512)
				if len(bs) == 512:
					bs = unpack('%sB'%512,bs)
					env1 = bs[509]*256+bs[508]
					env2 = bs[511]*256+bs[510]
			else: # if time doesn't look okay:
				if tme_delta>0: # we can read one more page (the last one):
					for j in range(0,126):
						dta[ii] = np.array((tme, bs[j*4], bs[1+(j*4)], 
												bs[2+(j*4)], bs[3+(j*4)], 
												env1, env2), dtype=desc_hhg)
						tme += bs[j*4]*tme_delta
						ii += 1
				invalid_data = True
				break
	# close file and return the read values:	
	f.close()
	if ii:
		return dta[:ii-1]
	else:
		return []
		
		
def hhg_store(path, daystamp, dta, conf):
	try:
		outpath = os.path.join(path,str(daystamp))
		if not os.path.exists(outpath):
			os.makedirs(outpath)
		np.savez(os.path.join(outpath,'d.npz'), dta=dta, conf=conf)		
		return outpath
	except:
		return ''
		
		
		
		
		
		
		
		
		
		
	
#### Everything below will be abandoned soon -- avoid using it!






# maximum file buffer
FBUFSIZE = 15000000

#ID that is found at the start of an mv_sampling page:
MV_IDBLOCK = (175,170,170,250,175,170,170,170)

#data descriptor for the raw data:
desc_raw = {	'names':   ('t',  'd',  'x',  'y',  'z',  'l'), 
					'formats': ('f8', 'B1', 'B1', 'B1', 'B1', 'u2') }
#data descriptor for mean-variance data:
desc_mv  = {	'names': (  't', 'xm','xv','ym','yv','zm','zv','l'), 
					'formats': ('f8','B1','B1','B1','B1','B1','B1','u2') }
	

## to be scrapped:
## read the binary HHG file and convert it into raw data (datenum x y z)
def hhg_import(filen):
	pg_i = 0
	ii = 0
	# check if file exists, if not exit now:
	if not os.path.isfile(filen):	return []
	# open dialog:
	pgrsdlg = gtk.Dialog("Importing...", None, 0, None)
	pbar = gtk.ProgressBar()
	pgrsdlg.vbox.add(pbar)
	pgrsdlg.set_size_request(250, 50)
	pbar.show()
	pgrsdlg.vbox.show()
	pgrsdlg.show()
	while gtk.events_pending(): gtk.main_iteration()
	# start parsing file:
	with open(filen, "rb") as f:
		bs = f.read(8)
		bs = unpack('%sB'%len(bs),bs)
		# is our data of type mean_variance or raw?
		if bs == MV_IDBLOCK:
			dta = np.recarray((FBUFSIZE,),dtype=desc_mv) # init mv dta
			bs = f.read(512)
			bs = unpack('%sB'%len(bs),bs)
			while len(bs)==512:
				if bs[-8:] == MV_IDBLOCK:
					# update progress bar:
					if (pg_i%10)==0:
						pbar.set_fraction(float(pg_i%3200)/3200)
						while gtk.events_pending(): gtk.main_iteration()
					# read:
					for j in range(0,42):
						tme = hhg_convtime(	bs[(j*12)],bs[1+(j*12)],
													bs[2+(j*12)],bs[3+(j*12)])
						if tme != False:
							dta[ii] = np.array( (tme,	
														bs[4+(j*12)],bs[5+(j*12)],
														bs[6+(j*12)],bs[7+(j*12)],
														bs[8+(j*12)],bs[9+(j*12)],
														bs[11]*256+bs[10] ), 
														dtype=desc_mv)
							ii+=1;
					pg_i+=1;
					bs = f.read(512)
					bs = unpack('%sB'%len(bs),bs)
				else:
					bs = (1,) # force us out of this loop!
		else: # else we assume raw data:
			fta = np.recarray((FBUFSIZE,),dtype=desc_raw) # init raw dta
			dta = np.recarray((FBUFSIZE,),dtype=desc_raw) # init raw dta
			if  len(bs) > 6:
				tme = hhg_convtime(bs[0],bs[1],bs[2],bs[3])
				lgt = bs[5]*256+bs[4]
				bs = f.read(512)
				bs = unpack('%sB'%len(bs),bs)
			invalid_data = False
			mm = 0;
			tmetmp = tme
			tmetmp += 1./1440
			fta[mm] = np.array( (tme, bs[4], 
									bs[1+(4)], bs[2+(4)],
									bs[3+(4)],lgt), dtype=desc_raw)	
			while (len(bs)==512) and not invalid_data:
				# update progress bar:
				if (pg_i%10)==0:
					pbar.set_fraction(float(pg_i%3200)/3200)
					while gtk.events_pending(): gtk.main_iteration()
				# read:
				tme_next = hhg_convtime(bs[504],bs[505],bs[506],bs[507])
				if (abs(tme_next-tme) < 0.005) and tme_next>0:  # time okay:
					num_samples = sum(bs[0:504:4])
					if num_samples > 0:
						tme_delta = (tme_next - tme) / num_samples
					else:
						invalid_data = True
						break
					for j in range(0,126):
						dta[ii] = np.array( (tme, bs[j*4], 
													bs[1+(j*4)], bs[2+(j*4)],
													bs[3+(j*4)],lgt), dtype=desc_raw)
						ii+=1
						tme += bs[j*4]*tme_delta
						if tme >= tmetmp:
							mm += 1
							#tmarr[mm] = tme
							tmetmp = tme
							tmetmp += 1./1440
							fta[mm] = np.array( (tme, bs[j*4], 
													bs[1+(j*4)], bs[2+(j*4)],
													bs[3+(j*4)],lgt), dtype=desc_raw)
					pg_i+=1
					tme = tme_next
					bs = f.read(512)
					if len(bs) == 512:
						bs = unpack('%sB'%512,bs)
						lgt = bs[509]*256+bs[508]
				else: # if time doesn't look okay:
					invalid_data = True
					break
	# close file and return the read values:
	f.close()
	pgrsdlg.hide()
	pgrsdlg.destroy()
	while gtk.events_pending(): gtk.main_iteration()
	if ii:
		return dta[:ii-1]#, fta[:mm-1]
	else:
		return []


#merge multilpe HHG files into one big one 'destination'
def hhg_merge_HHGs(files, destination):
	filename = ''
	if len(files)>1:
		fout = file(destination, 'wb')
		for n in files:
			fin = file(n, 'rb')
			shutil.copyfileobj(fin, fout, 65536)
			fin.close()
		fout.close()
		filename = destination
	elif len(files)==1:
		filename = files[0]
	return filename


#read the data file
def hhg_open_data(filename):
	dta = []
	tic = time.clock()
	if filename=='':
		return [], 'no data'
	if len(filename)>3:
		if filename[-3:]=='HHG':
			dta = hhg_import(filename)
		elif filename[-3:]=='npy':
			try:
				# import from an already-converted npy dataset:
				dta = np.load(filename)
				if len(dta[0])==6: 	# raw data files have 6 columns
					dta = dta.view(desc_raw, np.recarray)
				elif len(dta[0])==7: 	# hhg data files have 7 columns
					dta = dta.view(desc_hhg, np.recarray)
				elif len(dta[0])==8:
					dta = dta.view(desc_mv, np.recarray)
			except:
				dta = []
	toc = time.clock()
	dtstr = 'unknown'
	if len(dta)>0:
		nums = str(0); dtstr = 'unknown'; 
		if   dta.dtype==desc_raw: dtstr = 'raw'; nums = str(sum(dta.d))
		elif dta.dtype==desc_mv:  dtstr = 'mean-var'; nums = str(len(dta))
		elif dta.dtype==desc_hhg:  dtstr = 'hhg'; nums = str(len(dta))
		stats =  ('import: '+ nums + ' samples, ' + str(len(dta))
				 + ' entries, format=' + dtstr+ ', time(s): ' +str(toc-tic))
	else:   stats = 'no / invalid data!'
	return dta, stats
	
