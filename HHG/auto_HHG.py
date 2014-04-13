#!/usr/bin/env python2.7

import sys
import gtk, gobject, pygtk
from os import path, access, W_OK  # check: can we write to config file?
import time, datetime
from datetime import timedelta
import re
import sys, calendar, os
import numpy as np
from struct import unpack
import glob, subprocess, shutil
from matplotlib.dates import num2date
import hhg_plot.hhg_plot as hplt
import hhg_io.hhg_import as hgi
import hhg_dialogs.hhg_scan as hgd

class hhg_connect_download_dlg:
	def __init__(self, size_x=250, size_y=100):
		self.dlg = gtk.Dialog("Please wait", None, 0, None)
		self.dlg.set_urgency_hint(True)
		self.dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.dlg.set_default_response(gtk.RESPONSE_CANCEL)
		self.dlg.connect("response",self.close)
		self.pbar = gtk.ProgressBar()
		self.infotxt = gtk.Label()
		self.infotxt.set_text('Connect first HedgeHog...')
		self.dlg.vbox.add(self.pbar)
		self.dlg.vbox.add(self.infotxt)
		self.dlg.set_size_request(size_x, size_y)
		self.quitnow = False
		self.dlg.show_all()
		self.dlg.set_keep_above(True)
	def on_cancel(self):
		gtk.main_quit()
	def update_prgs(self):
		self.priter += 1
		self.pbar.set_fraction(float(self.priter%70)/70)
		while gtk.events_pending(): gtk.main_iteration()
	def scan_dmesg(self):
		self.infotxt.set_text('Connect first HedgeHog...')
		ret = hgi.hhg_parsedmesg()
		while not ret and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_parsedmesg()
			time.sleep(0.1)
	def scan_mount(self):
		self.infotxt.set_text('First HedgeHog connected. Mounting...')
		ret = hgi.hhg_findmount()
		while ret=='' and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_findmount()
			time.sleep(0.1)
		return ret
	def scan_files(self, srcdir):
		self.infotxt.set_text('Mounted. Parsing directory...')
		ret = os.path.isfile(srcdir+'/config.URE')
		while not ret and not self.quitnow:
			self.update_prgs()
			ret = os.path.isfile(srcdir+'/config.URE')
			time.sleep(0.1)
	def close(self, dta=[], msg=[]):
		self.quitnow = True;
		self.dlg.destroy()
	def run(self):
		self.priter = 0
		if not hgi.hhg_findmount():
			self.scan_dmesg()
		first_srcdir = self.scan_mount()
		self.scan_files(first_srcdir)
		first_id = hgi.hhg_findname()
		self.close()
		return [first_srcdir, first_id]

class hhg_disconnect_download_dlg:
	def __init__(self, size_x=250, size_y=125):
		self.counter = datetime.datetime.now()
		self.dlg = gtk.Dialog("Please wait", None, 0, None)
		self.dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.dlg.set_default_response(gtk.RESPONSE_CANCEL)
		self.dlg.connect("response",self.close)
		self.pbar = gtk.ProgressBar()
		self.infotxt1 = gtk.Label()
		self.infotxt2 = gtk.Label()
		self.dlg.vbox.add(self.pbar)
		self.dlg.vbox.add(self.infotxt1)
		self.dlg.vbox.add(self.infotxt2)
		self.dlg.set_size_request(size_x, size_y)
		self.quitnow = False
		self.dlg.show_all()
	def on_cancel(self):
		gtk.main_quit()
	def update_prgs(self):
		self.priter += 1
		self.pbar.set_fraction(float(self.priter%70)/70)
		while gtk.events_pending(): gtk.main_iteration()
	def scan_dmesg(self):
		self.infotxt1.set_text('Download successful')
		self.infotxt2.set_text('Disconnect first Hedgehog...')
		ret = True
		while ret and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_parsedmesg()
			time.sleep(0.1)
	def close(self, dta=[], msg=[]):
		self.quitnow = True;
		self.dlg.destroy()
	def run(self):
		self.priter = 0
		self.scan_dmesg()
		self.close()

class hhg_connect_start_dlg:
	def __init__(self, size_x=250, size_y=100):
		self.dlg = gtk.Dialog("Please wait", None, 0, None)
		self.dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.dlg.set_default_response(gtk.RESPONSE_CANCEL)
		self.dlg.connect("response",self.close)
		self.pbar = gtk.ProgressBar()
		self.infotxt = gtk.Label()
		self.dlg.vbox.add(self.pbar)
		self.dlg.vbox.add(self.infotxt)
		self.dlg.set_size_request(size_x, size_y)
		self.quitnow = False
		self.dlg.show_all()
	def on_cancel(self):
		gtk.main_quit()
	def update_prgs(self):
		self.priter += 1
		self.pbar.set_fraction(float(self.priter%70)/70)
		while gtk.events_pending(): gtk.main_iteration()
	def scan_dmesg(self):
		self.infotxt.set_text('Connect second HedgeHog...')
		ret = hgi.hhg_parsedmesg()
		while not ret and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_parsedmesg()
			time.sleep(0.1)
	def scan_mount(self):
		self.infotxt.set_text('Second HedgeHog connected. Mounting...')
		ret = hgi.hhg_findmount()
		while ret=='' and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_findmount()
			time.sleep(0.1)
		return ret
	def scan_files(self, srcdir):
		self.infotxt.set_text('Mounted. Parsing directory...')
		ret = os.path.isfile(srcdir+'/config.URE')
		while not ret and not self.quitnow:
			self.update_prgs()
			ret = os.path.isfile(srcdir+'/config.URE')
			time.sleep(0.1)
	def close(self, dta=[], msg=[]):
		self.quitnow = True;
		self.dlg.destroy()
	def run(self):
		self.priter = 0
		if not hgi.hhg_findmount():
			self.scan_dmesg()
		second_srcdir = self.scan_mount()
		self.scan_files(second_srcdir)
		second_id = hgi.hhg_findname()
		self.close()
		return [second_srcdir, second_id]
					
class hhg_disconnect_start_dlg:
	def __init__(self, size_x=250, size_y=125):
		self.counter = datetime.datetime.now()
		self.dlg = gtk.Dialog("Please wait", None, 0, None)
		self.dlg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self.dlg.set_default_response(gtk.RESPONSE_CANCEL)
		self.dlg.connect("response",self.close)
		self.pbar = gtk.ProgressBar()
		self.infotxt1 = gtk.Label()
		self.infotxt2 = gtk.Label()
		self.dlg.vbox.add(self.pbar)
		self.dlg.vbox.add(self.infotxt1)
		self.dlg.vbox.add(self.infotxt2)
		self.dlg.set_size_request(size_x, size_y)
		self.quitnow = False
		self.dlg.show_all()
	def on_cancel(self):
		gtk.main_quit()
	def update_prgs(self):
		self.priter += 1
		self.pbar.set_fraction(float(self.priter%70)/70)
		while gtk.events_pending(): gtk.main_iteration()
	def scan_dmesg(self):
		self.infotxt1.set_text('HedgeHog is logging for 7 days')
		self.infotxt2.set_text('Disconnect second HedgeHog...')
		ret = True
		while ret and not self.quitnow:
			self.update_prgs()
			ret = hgi.hhg_parsedmesg()
			time.sleep(0.1)
	def close(self, dta=[], msg=[]):
		self.quitnow = True;
		self.dlg.destroy()
	def run(self):
		self.priter = 0
		self.scan_dmesg()
		self.close()
		
		

while True:
	## buffer size: how many blocks (of 512 bytes each) do we read at once?
	bufsize = 192	# takes about 0.5 seconds on a laptop

	## look for the home directory of the system 
	homedir=os.path.expanduser("~")

	## look for an attached HedgeHog:
	hhgdwl = hhg_connect_download_dlg()
	[first_srcdir, first_id] = hhgdwl.run()

	## prepare the output structures:
	dta = np.recarray(0, dtype=hgi.desc_hhg)
	dlpath = os.path.join(homedir,'hhg_logs')
	if not os.path.exists(dlpath):
		os.makedirs(dlpath)
		
	## read configuration file:
	filen = first_srcdir+'/config.URE'
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
	flst = sorted(glob.glob(first_srcdir + '/log*.HHG'))
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
			break
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

	if tme1:
		## read the HHG data file(s) and show progress plot to inform user
		file_iter = 0
		old_day = 0
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
				bdta_l = len(bdta)
				bdta_s = sum(bdta.d)
				dta_s += bdta_s
				if len(bdta)>0:
					stats =  ( str(num2date(bdta.t[0]))[0:22]
							+ ': read '+ str(bdta_s).zfill(7) 
							+ ' samples in ' + str(bdta_l).zfill(7)
							+ ' rle entries, in ' +str(toc-tic)+' seconds, ' 
							+ str(len(dta)).zfill(10) + ' ' 
							+ str(dta_s).zfill(10) )
				else:
					stats = ''
				print stats
				## update plot: ###########################################
				new_day = int(bdta.t[-1])
				if old_day!=new_day:
					old_day = new_day
					## first plot the remains of the last day and save: ###
					tt = len([x for x in bdta.t if x<int(bdta.t[-1])])
					dta = np.append(dta, bdta[:tt]).view(hgi.desc_hhg,np.recarray)
					if tt>0:
						fig.update_plot(dta[::itr], stats)
					if len(dta)>0:
						daypath = hgi.hhg_store(dlpath, int(dta.t[0]), dta, conf)
						if daypath=='':
							print 'warning: could not write to '+	dlpath
					dta  = bdta[tt:].view(hgi.desc_hhg, np.recarray)
				else:
					dta  = np.append(dta, bdta).view(hgi.desc_hhg, np.recarray)
				#fig.update_plot(dta[::itr], stats)
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

	## unmounting first hedgehog
	subprocess.call(["sync"])
	subprocess.call(["umount", first_srcdir])
	
	## waiting 20 seconds for user to disconnect
	hhgdlwait = hhg_disconnect_download_dlg()
	hhgdlwait.run()
	
	## waiting for user to attach new hedgehog
	hhgcnt = hhg_connect_start_dlg()
	[second_srcdir, second_id] = hhgcnt.run()
	second_config_file = second_srcdir+'/config.URE'
	
	### write stp time to new hedgehog
	stpTime = []
	sysTime = datetime.datetime.now()
	stpTime_struc = datetime.datetime.now()+timedelta(days=7)
	stpTime.insert(0,stpTime_struc.year)
	stpTime.insert(1,stpTime_struc.month)
	stpTime.insert(2,stpTime_struc.day)
	with open (second_config_file, "r+w") as confhhg: 
		confhhg.seek(60,0)  # Write System Time
		confhhg.write(chr(sysTime.year-2000))
		confhhg.write(chr(0))
		confhhg.write(chr(sysTime.day))
		confhhg.write(chr(sysTime.month))
		confhhg.write(chr(sysTime.hour))
		confhhg.write(chr(0))
		confhhg.write(chr(sysTime.second))
		confhhg.write(chr(sysTime.minute))
		confhhg.seek(71,0)  # Write Stop Time
		confhhg.write(chr(stpTime[0]-2000))
		confhhg.write(chr(0))
		confhhg.write(chr(stpTime[2]))
		confhhg.write(chr(stpTime[1])) # Month
		confhhg.write(chr(sysTime.hour))
		confhhg.write(chr(0))
		confhhg.write(chr(sysTime.second))
		confhhg.write(chr(sysTime.minute))
		confhhg.close()
		
	## start logging 	
	with open (second_config_file,"r+w") as starthhg:
		starthhg.seek(1023,0)  
		#starthhg.write("l")
		starthhg.close()
	
	## unmount second hedgehog	
	subprocess.call(["sync"])
	subprocess.call(["umount", second_srcdir])

	## waiting 20 seconds for user to disconnect
	hhgstwait = hhg_disconnect_start_dlg()
	hhgstwait.run()
	
