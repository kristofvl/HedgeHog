#!/usr/bin/env python2.7

########################################################################
#
# Filename: download_HHG.py 							Authors: KristofVL
#
# Descript: Process downloaded npz files into a web calendar view
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

import sys, time
import numpy as np
import os, subprocess, fnmatch
from matplotlib.dates import num2date
import hhg_features.hhg_bstats as hf
import hhg_io.hhg_import as hi
import hhg_io.hhg_html as hh

	
	
	
## resolution at which the plotting occurs:
bins = 1440*2	# for full day view: 30 seconds
zbins = 1440*6 # for zoom view
bdiv = 17    	# for calendar views
zdiv = 32	

## one day canvas width (pixels):
cd_px_draw = 800
cd_px_yaxs = 32
cd_px = cd_px_yaxs + cd_px_draw

## zoomed day canvas width (pixels):
cz_px_draw = 1064
cz_px_yaxs = 32
cz_px = cz_px_yaxs + cz_px_draw

## write a calendar entry
def cal_entry(day_id, dlpath, f, skip):
	def find_in_js(vstr, substr, stop=0):
		entry = fstr.find(substr,stop)+len(substr)
		stop = fstr.find('";',entry)
		return vstr[entry:stop], stop

	tic = time.clock()
	hh.write_cal_entry(day_id, f)
	if skip and (day_id<skip_id):
		try:
			with open(os.path.join(dlpath,str(day_id),'d.js'),"r") as fl:
				fstr = fl.read()
				p_str,st = find_in_js(fstr,'p="',0)
				l_str,st = find_in_js(fstr,'l="',st)
				l = range(0,len(l_str),4*bdiv*30)
				l_str = ''.join([l_str[i:i+2] for i in l])
				x_str,st = find_in_js(fstr,'x="',st)
				y_str,st = find_in_js(fstr,'y="',st)
				z_str,st = find_in_js(fstr,'z="',st)
				xs_str,st = find_in_js(fstr,'xs'+str(day_id)+'="',st)
				ys_str,st = find_in_js(fstr,'ys'+str(day_id)+'="',st)
				zs_str,st = find_in_js(fstr,'zs'+str(day_id)+'="',st)
		except:
			f.write('</a></time>')
			try:
				os.makedirs(os.path.join(dlpath,str(day_id)))
			except:
				pass
			hh.write_day_stub_html(day_id, dlpath)
			print str(num2date(day_id))[0:10]+": d.js not parsed"
			return
	else:
		## open the data and configuration for the day:
		dfile = os.path.join(dlpath,str(day_id),'d.npz')
		try:
			out = np.load(dfile)
			dta = out['dta']
			cnf = str(out['conf'])
		except:
			f.write('</a></time>')
			try:
				os.makedirs(os.path.join(dlpath,str(day_id)))
			except:
				pass
			hh.write_day_stub_html(day_id, dlpath)
			print str(num2date(day_id))[0:10]+": d.npz not parsed"
			return
		## calculate day statistics and plot array (w. 30 seconds bins)
		days_stats = hf.stats_npz(dta, bins)
		day_bin = hf.npz2secbin(dta, 30)
		x_str=''.join(["%02x" %c for c in [x[0] for x in day_bin]])
		y_str=''.join(["%02x" %c for c in [x[1] for x in day_bin]])
		z_str=''.join(["%02x" %c for c in [x[2] for x in day_bin]])
		l_str =''.join(["%02x" %c for c in [x[3] for x in day_bin][::bdiv]])
		xs_str=''.join(["%02x" %c for c in [x[0] for x in day_bin][::bdiv]])
		ys_str=''.join(["%02x" %c for c in [x[1] for x in day_bin][::bdiv]])
		zs_str=''.join(["%02x" %c for c in [x[2] for x in day_bin][::bdiv]])
		probs = hf.night(bins, bdiv, days_stats, [x[3] for x in day_bin])
		nt = hf.night_endpoints(probs)
		p_str =''.join(["%02x" %c for c in map(int,probs.tolist())])
		dta = dta.view(np.recarray)
		dta_sum = sum(dta.d)
		dta_rle = len(dta)
	hh.write_cal_plots(day_id, f, l_str, xs_str, ys_str, zs_str, p_str)
	#####################################################################
	if not skip or (day_id>=skip_id):
		csva = np.array( ( dta.t-int(dta.t[0]), dta.x, dta.y,dta.z  ) ).T
		np.savetxt( os.path.join(dlpath,str(day_id),'d.csv'), csva, 
			fmt="%1.8f,%d,%d,%d")
		hh.write_day_html(day_id, dlpath, cnf, dta_sum, dta_rle, nt,cd_px)
		int_bin = hf.npz2secbin(dta,0.5)
		l_str =''.join(["%02x" %c for c in [x[3] for x in int_bin]])
		x_str =''.join(["%02x" %c for c in [x[0] for x in int_bin]])
		y_str =''.join(["%02x" %c for c in [x[1] for x in int_bin]])
		z_str =''.join(["%02x" %c for c in [x[2] for x in int_bin]])
		try:
			f=open(os.path.join(dlpath,str(day_id),'d.js'),"w")
		except:
			print "Day js file not opened for "+daystr
			return False
		f.write('var p="'+p_str+'";var l="'+l_str+'";var x="'+
					x_str+'";var y="'+y_str+'";var z="'+z_str+'";')
		f.write('var xs'+str(day_id)+'="'+xs_str+'";'+
				  'var ys'+str(day_id)+'="'+ys_str+'";'+
				  'var zs'+str(day_id)+'="'+zs_str+'";')
		f.close()
		## write zoom html:
		hh.write_day_zoom_html(day_id, dlpath, cz_px)
		## write raw plot file:
		#hh.write_raw_day_htmls(day_id, dlpath)
		os.remove(os.path.join(dlpath,str(day_id),'d.csv'));
	#####################################################################
	toc = time.clock()
	print str(num2date(day_id))[0:10]+' took '+str(toc-tic)+' seconds'
	

## main script starts here: ############################################

if len(sys.argv) < 2:
	print 'use: calendar_HHG.py [download_folder] [start day]'
	exit(1)

dlpath = sys.argv[1]
if not os.path.exists(dlpath):
	exit(1)

skip = False
skip_id = sys.maxint
if len(sys.argv) > 2:
	skip_id = int(sys.argv[2])
	skip = True

home = os.environ['HOME']
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/st.css"%home,  dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/Chart.js"%home, dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/ans.js"%home, dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/cal.js"%home, dlpath])
subprocess.call(["cp", "-rf", "%s/HedgeHog/HHG/hhg_web/img"%home,dlpath])

## get all subdirectories with d.npz files:
matches = []
for root, dirnames, filenames in os.walk(dlpath):
	for filename in fnmatch.filter(filenames, 'd.npz'):
		matches.append((root[-6:], os.path.join(root, filename)))
matches = sorted(matches)
first_day_id = int(matches[0][0])
last_day_id  = int(matches[-1][0])
		
## remove previous html files
if not skip:
	for root, dirnames, filenames in os.walk(dlpath):
		for filename in fnmatch.filter(filenames, 'index_*.html'):
			os.remove( os.path.join(root, filename))
		
## assume that we're interested in first month:
month_vw = num2date(first_day_id).month

try:
	f=open(os.path.join(dlpath,'index.html'),"w")
except:
	print 'Cannot write to index file'
	exit(1)
	
f.write(hh.cal_indexheader())

# fill empty days before day of week:
wkday =  num2date(first_day_id).weekday()
for wd in range(wkday):
	cal_entry(first_day_id-wkday+wd, dlpath, f, skip)
	
# fill in days with data:
for day_id in range(first_day_id, last_day_id):
	cal_entry(day_id, dlpath, f, skip)
	
# add remaining days in row:
for rd in range( 7-(last_day_id-first_day_id+wkday)%7):
	cal_entry(last_day_id+rd, dlpath, f, skip)

f.write('</div></div></section></body>')
f.close()

## preview:
subprocess.call(["x-www-browser", "%s/index.html"%dlpath, "--start-maximized"])
