

########################################################################
#
# Filename: hhg_html.py								Author: Kristof VL
#
# Descript: Data conversion routines for html-bliss
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
import json
from json import encoder
from matplotlib.dates import date2num, num2date
from datetime import datetime
from struct import unpack
from calendar import TimeEncoding, month_name
import csv

## change this to alter names of calendar entities:
locale_str = "en_US.UTF-8"

## write html headers:
def htmlhead(title, csspath, jspath):
	return ('<!DOCTYPE html><html lang=en><meta charset=utf-8>'+
		'<link rel=stylesheet href="'+csspath+'">'+
		'<head><title>'+title+'</title>'+
		'<script src="'+jspath+'"></script>')

def zoom_indexheader():
	return (htmlhead('HedgeHog Zoom View','../st.css','../ans_array.js')+
		'<script src="d.js"></script><script src="../ans.js"></script>'+
		'<script src="../Chart.js"></script></head>'+
		'<body><section id="calendar" style="width:1100px;">'+
		'<h1><a href="javascript:goLeft();"><span class="a-left">'+
		'</span></a><script>'+
		'document.write(toDate(dayid)+", "+toTime(strtt)+"-"+'+
		'toTime(stopt))</script><a href="javascript:goRight();">'+
		'<span class="a-right"></span></a>'+
		'<a style="text-align:right;" href="javascript:goUp();">'+
		'<span class="a-up"></span></a></h1>')
def cal_indexheader(year,d0,d1):
	hdr = ''
	for dayname in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
		hdr += ('<div class="header">'+dayname+'</div>')
	return (htmlhead('HedgeHog Calendar View','st.css','cal.js')+
		'<script src="Chart.js"></script></head>'+
		'<body onload="init_cal()"><section id="calendar">'+
		'<script>addMonthBrowser('+str(year)+');</script>'+
		'<a href="#" onmousedown="browseMonth()" '+
		'style="text-decoration:none;"><h1 id="t"></h1></a>'+
		hdr+'<div id="days"><div id="scrollview" '+
		'onscroll="onScroll(this)">'+
		'<script>fillDays('+str(d0)+','+str(d1)+');</script>')

## generate html for chart canvas:
def canvas_html(varname, style, w, h):
	return ('<canvas style="'+style+'" id="'+varname+
				'" width="'+w+'" height="'+h+'"></canvas>')
		
## generate html for light dataset variable:
def ldata_html(varname, labels, fcolor, scolor, data):
	return ('var '+varname+'={l:'+labels+',ds:[{fc:"'+
		fcolor+'",'+'sc:"'+scolor+'",d:"'+data+'"}]};')

## generate html for night/light dataset variable:
def ndata_html(varname, labels, fcl, scl, datal, fcn, scn, datan ):
	return ('var '+varname+'={l:'+labels+
		',ds:[{fc:"'+fcl+'",sc:"'+scl+'",d:"' + datal +'"},'+
		'{fc:"'+fcn+'",'+'sc:"'+scn+'",d:"' + datan +'"}]};')

## generate html for acc3d dataset variable:
def adata_html(varname, labels, scx,dx, scy,dy, scz,dz):
	return ('var '+varname+'={l:'+labels+
			',ds:[{sc:"'+scx+'",d:"'+dx+'"},'+
			'{sc:"'+scy+'",d:"'+dy+
			'"},{sc:"'+scz+'",d:"'+dz+'"}]};')

## generate html for chart variable:
def chart_html(varname, idname, charttype, dataname, options):
	return ('var '+varname+' = new Chart(document.getElementById('+
		'"'+idname+'").getContext("2d")).'+charttype+'('+dataname+','+
		'{'+options+'});')
		
## return html string to draw the configuration info boxes
def conf_html(cnf,smps,rle):
	g_range = pow(2,1+ord(cnf[12])-48)
	bw_lookup = [0.1, 5, 10, 25, 50, 100, 200, 400, 800, 1500]
	md_lookup = ['controller', 'sensor']
	pw_lookup = ['normal', 'low-power', 'auto-sleep', 'low/auto']
	div_preambl = '<div id="inf" style="left:'
	left_offset = '865px'
	return (div_preambl+left_offset+';top:62px;height:70px;">'+
		'<b>HedgeHog Configuration</b>\n'+ 
		'HedgeHog_ID: '+str(cnf[0:4])+'\nfirmware:    ' + cnf[35:42] +
		'\nlogging end: 20' +str(ord(cnf[71])) + '-' +
		str(1+ord(cnf[72])).zfill(2) +'-'+ str(ord(cnf[73])).zfill(2) +
		'</div>'+div_preambl+left_offset+
		';top:169px;height:84px;"><b>Accelerometer Settings</b>\n' +
		'acc. range: +/- ' + str(g_range) +'g\nsampled at: ' + 
		str(bw_lookup[ord(cnf[13])-48]) + 'Hz (' + 
		str(md_lookup[ord(cnf[14])-48]) + ')\npower mode: ' + 
		str(pw_lookup[ord(cnf[15])-48]) + '\nRLE delta : ' + str(cnf[20])+
		'</div>'+div_preambl+left_offset+';top:292px;height:48px;">'+
		'<b>Dataset Properties</b>\n3d samples : '+str(smps).zfill(9)+
		'\nRLE samples: '+str(rle).zfill(9)+'</div>')

## helper function to get month name:
def get_month_name(month_no, locale):
	with TimeEncoding(locale) as encoding:
		s = month_name[month_no]
		if encoding is not None:
			s = s.decode(encoding)
		return s
		
def write_day_stub_html(day_id, dlpath):
	## construct html file
	try:
		f=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
	except:
		print "Day directory file not found for "+str(day_id)
		return False
	## construct the html page for the day-view:
	f.write(zoom_indexheader())
	f.write('<hr>')
	f.write('<p>no data found for this day</p>')
	f.write('</section></body></html>')
	f.close()
	## construct js file
	try:
		f=open(os.path.join(dlpath,str(day_id),'ds.js'),"w")
	except:
		print "Day directory file not found for "+str(day_id)
		return False
	## construct the js for the day-view:
	f.write('ps'+str(day_id)+'="0";ls'+str(day_id)+'="0";')
	f.write('xs'+str(day_id)+'="0";ys'+str(day_id)+'="0";')
	f.write('zs'+str(day_id)+'="0";')
	f.close()
	return True
	
def write_day_html(day_id, dlpath, cnf, dta_sum, dta_rle, nt, cd_px):
	ntimes = [' ', ' ', '']
	ntimes[0] = str(num2date(day_id+nt[0]))[:16]
	ntimes[1] = str(num2date(day_id+nt[1]))[:16]
	ntimes[2] = str(num2date(day_id+nt[1]-nt[0]))[11:16]
	canw=str(cd_px)
	## construct html file
	try:
		f=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
	except:
		print "Day directory file not found for "+str(day_id)
		return False
	## construct the html page for the day-view:
	f.write(zoom_indexheader()+'<hr>')
	f.write(conf_html(cnf,dta_sum, dta_rle))
	f.write( '<div id="inf" style="left:865px;top:379px;height:70px;">'+
		'<b>Largest Sleep Segment</b>\ntotal duration: '+ntimes[2]+'\n'+
		'start: '+ntimes[0]+'\n' +'stop:  '+ntimes[1]+'\n' +'</div>')
	f.write('<div class="icn-slp"></div>')
	f.write( 
		canvas_html('night_view_prb','position:relative;',canw,'100') +
		'</br><div class="icn-sun"></div>'+
		canvas_html('day_view_light','position:relative;',canw,'120') +
		'</br><div class="icn-act"></div>'+
		canvas_html('day_view_acc3d','position:relative;',canw,'200') +
		'</br>'+
		canvas_html('dvans','position:relative;',canw,'100')
		 )
	f.write('<script>'+
		'drawAll(x,y,z,l,p, strtt,stopt, skipenv, skipxyz, 7);</script>')
	f.write('<hr><p style="font-size:small;">24h view '+
		'with <a href="http://kristofvl.github.io/HedgeHog">'+
		'HedgeHog sensor</a> #'+ cnf[0:4]+'.<br/>'+
		'<a href="d.npz"><img src="../img/zoom.png" style="'+
		'vertical-align:middle;"></img>Raw data for this day (npz, '+
		str(os.path.getsize(os.path.join(dlpath,str(day_id),'d.npz')))+
		' bytes)</a></p>')
	f.write('<p style="font-size:small;color:#fff;left:'+
		str(15+800.0*nt[0]+400.0*(nt[1]-nt[0]))+'px;top:102px;'+
		'height:70px;position:absolute;">'+ntimes[2]+'</p>')
	f.write('<p style="font-size:small;color:#666;left:'+
		str(15+800.0*nt[0])+'px;top:122px;'+
		'height:70px;position:absolute;">'+ntimes[0][11:]+'</p>')
	f.write('<p style="font-size:small;color:#666;left:'+
		str(15+800.0*nt[1])+'px;top:122px;'+
		'height:70px;position:absolute;">'+ntimes[1][11:]+'</p>')
	f.write('</section></body></html>')
	f.close()
	return True


def write_day_zoom_html(day_id, dlpath, cz_px):
	canw = str(cz_px)
	## construct html file
	try:
		f=open(os.path.join(dlpath,str(day_id),'index_zoom.html'),"w")
	except:
		print "Day directory file not found for "+str(dayid)
		return False
	## construct the html page for the day-view:
	f.write(zoom_indexheader())
	f.write('<hr>')
	f.write( 
		'<div class="icn-slp"></div>'+
		canvas_html('night_view_prb','position:relative;',canw,'100') +
		'</br><div class="icn-sun"></div>'+
		canvas_html('day_view_light','position:relative;',canw,'120') +
		'</br><div class="icn-act"></div>'+
		canvas_html('day_view_acc3d','position:relative;',canw,'200') +
		'</br>'+
		canvas_html('dvans','position:relative;',canw,'100')
		 )
	f.write('<script>'+
		'drawAll(x,y,z,l,p, strtt,stopt, skipenv, skipxyz, 7);</script>')
	f.write('<hr><p style="font-size:small;">24h view '+
		'with a <a href="http://kristofvl.github.io/HedgeHog">'+
		'HedgeHog sensor</a> <br/></p>')
	f.write('</section></body></html>')
	f.close()
	return True
