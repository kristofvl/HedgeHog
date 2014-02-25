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
import os, subprocess
from matplotlib.dates import num2date
import hhg_features.hhg_bstats as hf
import hhg_io.hhg_import as hi
import hhg_io.hhg_html as hh

	
	
	
## resolution at which the plotting occurs:
bins = 1440*2	# for full day view
bdiv = 17    	# for calendar views
	

## write a calendar entry
def cal_entry(day_id, dlpath, f):
	tic = time.clock()
	hh.write_cal_entry(day_id, f)
	## open the data and configuration for the day:
	dfile = os.path.join(dlpath,str(day_id),'d.npz')
	try:
		out = np.load(dfile)
		dta = out['dta']
		cnf = str(out['conf'])
	except:
		f.write('</a></time>')
		print str(num2date(day_id))[0:10]+": data not found"
		return
	days_stats, day_bin = hf.stats_npz(dta, bins)
	probs = ( 128 	* hf.night_acc(days_stats, bdiv, 2.0)
						* hf.night_lgt((day_bin.e1>>8).tolist(), bdiv, 4.0)
						)
	lbl = [' ']*bins; lbl[0]='00'; lbl[int(bins/4)]='06';
	lbl[bins>>1]='12'; lbl[int(3*bins/4)]='18'; lbl[bins-1]='00';
	lbl_str = str(lbl).replace(" ","")
	l_str =''.join(["%02x" %c for c in (day_bin.e1[::bdiv]>>8).tolist()])
	x_str =''.join(["%02x" %c for c in (day_bin.x).tolist()])
	y_str =''.join(["%02x" %c for c in (day_bin.y).tolist()])
	z_str =''.join(["%02x" %c for c in (day_bin.z).tolist()])
	xs_str=''.join(["%02x" %c for c in day_bin.x[::bdiv].tolist()])
	ys_str=''.join(["%02x" %c for c in day_bin.y[::bdiv].tolist()])
	zs_str=''.join(["%02x" %c for c in day_bin.z[::bdiv].tolist()])
	p_str =''.join(["%02x" %c for c in map(int,probs.tolist())])
	dta_sum = sum(dta.view(np.recarray).d)
	dta_rle = len(dta)
	hh.write_cal_plots(day_id, f, l_str, xs_str, ys_str, zs_str, p_str)
	hh.write_day_html(day_id, dlpath, cnf, dta_sum, dta_rle, 
							x_str, y_str, z_str, l_str, p_str, lbl_str)
	toc = time.clock()
	print str(num2date(day_id))[0:10]+' took '+str(toc-tic)+' seconds'
	

## main script starts here: ############################################

if len(sys.argv) < 2:
	print 'use: calendar_HHG.py [download_folder] [start day]'
	exit(1)

dlpath = sys.argv[1]
if not os.path.exists(dlpath):
	exit(1)

home = os.environ['HOME']
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/st.css"%home,  dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/Chart.js"%home, dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/sleep.png"%home,dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/sun.png"%home,dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/act.png"%home,dlpath])

first_day_id = int(sorted(os.walk(dlpath).next()[1])[0])
if len(sys.argv) > 2: first_day_id = int(sys.argv[2]) # allow skip days

last_day_id = int(sorted(os.walk(dlpath).next()[1])[-1])+1
 # assume that we're interested in first month:
month_vw = num2date(first_day_id).month

try:
	f=open(os.path.join(dlpath,'index.html'),"w")
except:
	print 'Cannot write to index file'
	exit(1)
	
f.write(hh.cal_indexheader('Month View'))

# fill empty days before day of week:
wkday =  num2date(first_day_id).weekday()
for wd in range(wkday):
	cal_entry(first_day_id-wkday+wd, dlpath, f)
	
# fill in days with data:
for day_id in range(first_day_id, last_day_id):
	cal_entry(day_id, dlpath, f)
	
# add remaining days in row:
for rd in range( 7-(last_day_id-first_day_id+wkday)%7):
	cal_entry(last_day_id+rd, dlpath, f)

f.write('</div></div></section></body>')
f.close()

## preview:
subprocess.call(["firefox", "%s/index.html"%dlpath])
