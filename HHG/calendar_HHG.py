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
bins = 1440*2	# for full day view: 30 seconds
zbins = 1440*6 # for zoom view
bdiv = 17    	# for calendar views
zdiv = 32		
	
## subplots per day:
subp = [	(0,0.25,'0006'), (0.125,0.375,'0309'), (0.25,0.5,'0612'), 
			(0.375,0.625,'0915'), (0.5,0.75,'1218'), 
			(0.625,0.875,'1521'), (0.75,1,'1800') ]


subh = []
for i in range(24):
	subh.append( (float(i)/24, float(i+1)/24, 
		str(i).zfill(2)+str((i+1)%24).zfill(2) ) )

print subh
	
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
		try:
			os.makedirs(os.path.join(dlpath,str(day_id)))
		except:
			pass
		hh.write_day_stub_html(day_id, dlpath)
		print str(num2date(day_id))[0:10]+": data not found"
		return
	## calculate day statistics and plot array (w. 30 seconds bins)
	days_stats, day_bin = hf.stats_npz(dta, bins)
	probs = hf.night(bins, bdiv, days_stats, day_bin)
	nt = hf.night_endpoints(probs)
	l_str =''.join(["%02x" %c for c in (day_bin.e1[::bdiv]>>8).tolist()])
	x_str =''.join(["%02x" %c for c in (day_bin.x).tolist()])
	y_str =''.join(["%02x" %c for c in (day_bin.y).tolist()])
	z_str =''.join(["%02x" %c for c in (day_bin.z).tolist()])
	xs_str=''.join(["%02x" %c for c in day_bin.x[::bdiv].tolist()])
	ys_str=''.join(["%02x" %c for c in day_bin.y[::bdiv].tolist()])
	zs_str=''.join(["%02x" %c for c in day_bin.z[::bdiv].tolist()])
	p_str =''.join(["%02x" %c for c in map(int,probs.tolist())])
	dta = dta.view(np.recarray)
	dta_sum = sum(dta.d)
	dta_rle = len(dta)
	csva = np.array( ( dta.t-int(dta.t[0]), dta.x, dta.y,dta.z  ) ).T
	np.savetxt( os.path.join(dlpath,str(day_id),'d.csv'), csva, 
		fmt="%1.8f,%d,%d,%d")
	hh.write_cal_plots(day_id, f, l_str, xs_str, ys_str, zs_str, p_str)
	if skip:
		if os.path.exists(os.path.join(dlpath,str(day_id),'index.html')):
			skip = True;
		else:
			skip = False;
	#####################################################################
	if not skip:
		hh.write_day_html(day_id, dlpath, cnf, dta_sum, dta_rle, nt,
							x_str, y_str, z_str, l_str, p_str, cd_px)
		## calculate raw data view for 1 hour with no overlaps:
		for intr in subh:
			dta_sel = [dta[j] for j in range(len(dta)) 
							if ((dta[j][0]>(day_id+intr[0])) and   
								(dta[j][0]<(day_id+intr[1])))]
			dta_sel = np.array(dta_sel).view(np.recarray)
			if dta_sel!=[]:
				int_bin = hf.equidist_npz(dta_sel)
				if len(int_bin)>zbins:
					it_bin = int_bin[0:zbins].view(np.recarray);
					fctr = len(int_bin)/zbins;
					for i in range(0,zbins):
						if i%2==0:
							it_bin.x[i] = max(int_bin.x[i*fctr:(i+1)*fctr])
							it_bin.y[i] = min(int_bin.y[i*fctr:(i+1)*fctr])
							it_bin.z[i] = max(int_bin.z[i*fctr:(i+1)*fctr])
						else:
							it_bin.x[i] = min(int_bin.x[i*fctr:(i+1)*fctr])
							it_bin.y[i] = max(int_bin.y[i*fctr:(i+1)*fctr])
							it_bin.z[i] = min(int_bin.z[i*fctr:(i+1)*fctr])
					
					l_str =''.join(["%02x" %c for c in (
												it_bin.e1[::zdiv]>>8).tolist()])
					x_str =''.join(["%02x" %c for c in (it_bin.x).tolist()])
					y_str =''.join(["%02x" %c for c in (it_bin.y).tolist()])
					z_str =''.join(["%02x" %c for c in (it_bin.z).tolist()])
					hh.write_day_zoom_html(day_id, dlpath, 
						x_str, y_str, z_str, l_str, 
						p_str[int(intr[0]*len(p_str)):int(intr[1]*len(p_str))], 
						intr[2], cz_px)
		## calculate raw data view for 6 hours with 3 hour overlaps:
		for intr in subp:
			dta_sel = [dta[j] for j in range(len(dta)) 
							if ((dta[j][0]>(day_id+intr[0])) and   
								(dta[j][0]<(day_id+intr[1])))]
			dta_sel = np.array(dta_sel).view(np.recarray)
			if dta_sel!=[]:
				int_bin = hf.equidist_npz(dta_sel)
				if len(int_bin)>zbins:
					it_bin = int_bin[0:zbins].view(np.recarray);
					fctr = len(int_bin)/zbins;
					for i in range(0,zbins):
						if i%2==0:
							it_bin.x[i] = max(int_bin.x[i*fctr:(i+1)*fctr])
							it_bin.y[i] = min(int_bin.y[i*fctr:(i+1)*fctr])
							it_bin.z[i] = max(int_bin.z[i*fctr:(i+1)*fctr])
						else:
							it_bin.x[i] = min(int_bin.x[i*fctr:(i+1)*fctr])
							it_bin.y[i] = max(int_bin.y[i*fctr:(i+1)*fctr])
							it_bin.z[i] = min(int_bin.z[i*fctr:(i+1)*fctr])
					
					l_str =''.join(["%02x" %c for c in (
												it_bin.e1[::zdiv]>>8).tolist()])
					x_str =''.join(["%02x" %c for c in (it_bin.x).tolist()])
					y_str =''.join(["%02x" %c for c in (it_bin.y).tolist()])
					z_str =''.join(["%02x" %c for c in (it_bin.z).tolist()])
					hh.write_day_zoom_html(day_id, dlpath, 
						x_str, y_str, z_str, l_str, 
						p_str[int(intr[0]*len(p_str)):int(intr[1]*len(p_str))], 
						intr[2], cz_px)
		## write raw plot file:
		hh.write_raw_day_htmls(day_id, dlpath)
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
if len(sys.argv) > 2:
	skip = True

home = os.environ['HOME']
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/st.css"%home,  dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/Chart.js"%home, dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/hhg_web/ans.js"%home, dlpath])
subprocess.call(["cp", "-rf", "%s/HedgeHog/HHG/hhg_web/img"%home,dlpath])
subprocess.call(["wget", "-q", "-nc", "-P%s"%dlpath,
	"http://dygraphs.com/1.0.1/dygraph-combined.js"])


first_day_id = -1;
try_id = 0;
while (first_day_id==-1):
	try:
		first_day_id = int(sorted(os.walk(dlpath).next()[1])[try_id])
	except ValueError:
		first_day_id = -1; try_id+=1;
		
if len(sys.argv) > 2: first_day_id = int(sys.argv[2]) # allow skip days

last_day_id = -1;
try_id = -1;
while (last_day_id==-1):
	try:
		last_day_id = int(sorted(os.walk(dlpath).next()[1])[try_id])+1
	except ValueError:
		last_day_id = -1; try_id-=1;	
		
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
	cal_entry(first_day_id-wkday+wd, dlpath, f, skip)
	
# fill in days with data:
for day_id in range(first_day_id, last_day_id):
	cal_entry(day_id, dlpath, f, skip)
	
# add remaining days in row:
for rd in range( 7-(last_day_id-first_day_id+wkday)%7):
	cal_entry(last_day_id+rd, dlpath, f, skip)

f.write('</div></div></section>'+
	'<script>$("#scrollview").stop().animate({scrollTop:'+
		'$("#scrollview")[0].scrollHeight},700);</script>'+
		'</body>')
f.close()

## preview:
subprocess.call(["firefox", "%s/index.html"%dlpath])
