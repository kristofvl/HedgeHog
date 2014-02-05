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
import os
from matplotlib.dates import num2date

#open/parse the data:
if len(sys.argv) < 2:
	print 'use: calendar_HHG.py [download_folder]'
	exit(1)

dlpath = sys.argv[1]
if not os.path.exists(dlpath):
	exit(1)	

## update calendar view:
f=open(os.path.join(dlpath,'index.html'),"w")
f.write('<!DOCTYPE html><html lang=en><meta charset=utf-8>')
f.write('<link rel=stylesheet href=st.css>')
f.write('<meta name=author content="KristofVL">')
f.write('<meta property=og:title content="HTML5 HedgeHog Calendar">')
f.write('<body><section id=calendar>')
# fill empty days before day of week: 
first_day_id = int(sorted(os.walk(dlpath).next()[1])[0])
for wd in range(num2date(first_day_id).weekday()):
	f.write('<time datetime=""><a href=#">' 
					+ str(num2date(first_day_id-wd-1).day) )
	f.write( '<div class="crop"></div></a></time>\n')

#f.write('<h1>'+calendar.month_name[(num2date(day_id).month)]+' '
#				 +str(num2date(day_id).year)+'</h1>')
for day_id_str in sorted(os.walk(dlpath).next()[1]):	
	day_id = int(day_id_str)
	daystr = str(num2date(day_id).year) + ' '  
	daystr += str(num2date(day_id).month) + '-' 
	daystr += str(num2date(day_id).day)
	f.write('<time datetime="'+ daystr + '"><a href="./' + 
				day_id_str + '/p.pdf">' + str(num2date(day_id).day) )
	f.write( '<div class="crop"><img src="./' + day_id_str + '/p.png' +
				'"></div></a></time>\n')
f.write('</section></body>')
f.close()
