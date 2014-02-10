#!/usr/bin/env python2.7

########################################################################
#
# Filename: download_HHG.py 							Authors: KristofVL
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
########################################################################

import sys, time, calendar
import os, subprocess
from matplotlib.dates import num2date



## write html header
def hhg_cal_indexheader(f):
	f.write('<!DOCTYPE html><html lang=en><meta charset=utf-8>')
	f.write('<link rel=stylesheet href=st.css>')
	f.write('<meta property=og:title content="HTML5 HedgeHog Calendar">')
	
## write a calendar entry
def hhg_cal_entry(day_id, month_view, dlpath):
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	f.write('<time datetime="'+ daystr + '"')
	if num2date(day_id).weekday()>4:
		f.write('class="weekend"')
	elif month_view != num2date(day_id).month:
		f.write(' class="notmonth"')
	f.write('><a href="./'+ str(day_id) +'/index.html">' 
				+ str(num2date(day_id).day) )
	f.write( '<div class="crop"><img src="./' + str(day_id) + '/p.png' +
				'"></div></a></time>\n')
	try:
		df=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
		hhg_cal_indexheader(df)
		df.write('<body><h1>'+daystr+'</h1>')
		df.write('<p><a href="d.npz">Download the raw data</a>')
		df.write(' in npz format (numerical python)</p> <center>')
		df.write('<iframe src="p.pdf" width="1000px" height="700px">')
		df.write('</iframe></center></body>')
		df.close()
	except:
		print "Date not found"
	


if len(sys.argv) < 2:
	print 'use: calendar_HHG.py [download_folder]'
	exit(1)

dlpath = sys.argv[1]
if not os.path.exists(dlpath):
	exit(1)

home = os.environ['HOME']
subprocess.call(["cp", "%s/HedgeHog/HHG/st.css"%home, dlpath])
first_day_id = int(sorted(os.walk(dlpath).next()[1])[0])
last_day_id = int(sorted(os.walk(dlpath).next()[1])[-1])+1
 # assume that we're interested in first month:
month_vw = num2date(first_day_id).month

f=open(os.path.join(dlpath,'index.html'),"w")
hhg_cal_indexheader(f)
f.write('<body><section id=calendar>')
f.write('<h1>'+calendar.month_name[month_vw]+' '
				 +str(num2date(first_day_id).year)+'</h1>')
for dayname in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
	f.write('<div class="header">'+dayname+'</div>')
f.write('<div id="days"><div id="scrollview">')

# fill empty days before day of week:
wkday =  num2date(first_day_id).weekday()
for wd in range(wkday):
	hhg_cal_entry(first_day_id-wkday+wd, month_vw, dlpath)
	
# fill in days with data:
for day_id in range(first_day_id, last_day_id):
	hhg_cal_entry(day_id, month_vw, dlpath)
	
# add remaining days in row:
for rd in range( 7-(last_day_id-first_day_id+wkday)%7 ):
	hhg_cal_entry(last_day_id+rd, month_vw, dlpath)
	
f.write('</div></div></section></body>')
f.close()

subprocess.call(["firefox", "%s/index.html"%dlpath])
