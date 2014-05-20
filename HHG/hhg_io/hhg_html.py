

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

def zoom_indexheader(daystr, ts, day_id):
	if ts!=(0,1):
		hspan = float(ts[1]-ts[0])*24
		if round(hspan)==6:
			shft = 3.0
		elif round(hspan)==1:
			shft = 0.5
		prevh = (dayfrac2str((ts[0]*24-shft)/24)[:2]+dayfrac2str((ts[0]*24-shft)/24)[3:]+
					dayfrac2str((ts[1]*24-shft)/24)[:2]+dayfrac2str((ts[1]*24-shft)/24)[3:])
		nexth = (dayfrac2str((ts[0]*24+shft)/24)[:2]+dayfrac2str((ts[0]*24+shft)/24)[3:]+
					dayfrac2str((ts[1]*24+shft)/24)[:2]+dayfrac2str((ts[1]*24+shft)/24)[3:])
		if (prevh=="21000300"): prevh = "18000000"
		if (prevh=="00300030"): prevh = "23000000"
		if (nexth=="21000300"): nexth = "00000600"
		if (nexth=="23300030"): nexth = "00000100"
		prevh = "_"+prevh; nexth = "_"+nexth
	else:
		prevh = ""; nexth = "";
	prevd =  str(day_id-int(ts[0]==0))
	nextd =  str(day_id+int(ts[1]==1))
	return (htmlhead('HedgeHog Zoom View','../st.css','../ans_array.js')+
		'<script>var strtt='+ '{:.20f}'.format(ts[0]) +
		';var stopt='+ '{:.20f}'.format(ts[1]) +';'+
		'var dayid='+str(day_id)+';</script><script src="d.js"></script>'+
		'<script src="../Chart.js"></script>'+
		'<script src="../ans.js"></script></head>'+
		'<body><section id="calendar" style="width:1100px;">'+
		'<h1><a href="../'+prevd+'/index'+prevh+
		'.html"><span class="a-left"></span></a>'+daystr+', <script>'+
		'document.write(toTime(strtt)+"-"+toTime(stopt))</script>'+
		'<a href="../'+nextd+'/index'+nexth+
		'.html"><span class="a-right"></span></a>'+
		'<a style="text-align:right;" href="./index.html">'+
		'<span class="a-up"></span></a></h1>')
def rawday_indexheader(daystr, day_id):
	return (htmlhead('HedgeHog Day View (Raw)','../st.css',
			'../dygraph-combined.js')+
		'</head><body><section id="calendar" style="width:1100px;">'+
		'<h1><a href="../'+str(day_id-1)+
		'/index_raw.html"><span class="a-left"></span></a>'+daystr+
		'<a href="../'+str(day_id+1)+
		'/index_raw.html"><span class="a-right"></span></a>'+
		'<a style="text-align:right;" href="../index.html">'+
		'<span class="a-up"></span></a></h1>')
def cal_indexheader(mnth):
	hdr = ''
	for dayname in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
		hdr += ('<div class="header">'+dayname+'</div>')
	return (htmlhead('HedgeHog Calendar View','st.css','Chart.js')+
		'<script src="https://code.jquery.com/jquery-1.11.0.min.js">'+
		'</script><script>$(document).ready(function(){'+
		'$("time").mouseover(function(){'+
		'$("h1").html($(this).attr("datetime"))});});</script></head>'+
		'<body><section id=calendar><h1>'+mnth+'</h1>'+hdr+
		'<div id="days"><div id="scrollview">')

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

## convert a day fraction to a string (e.g., 0.5 -> "12:00")
def dayfrac2str(frac):
	return (str(int(frac*24)%24).zfill(2)+":"+
		str( int(round(60*(frac*24-int(frac*24))))%60 ).zfill(2) );

## write a calendar entry
def write_cal_entry(day_id, f):
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	## construct the html time section for the calendar:
	f.write('<time datetime="'+
		get_month_name(num2date(day_id).month, locale_str)+
		' '+str(num2date(day_id).year)+ '"')
	if num2date(day_id).weekday()>4:
		f.write('class="weekend"')
	f.write('><a href="./'+ str(day_id) +'/index.html">'
				+ str(num2date(day_id).day) )
	f.write('</a>')
	
	
def write_cal_plots(day_id, f, l_str, x_str, y_str, z_str, p_str ):
	## construct the html for the plots:
	f.write( canvas_html('dvn'+str(day_id),
		'position:absolute;left:0px;top:14px;', '160', '30'))
	f.write( canvas_html('dva'+str(day_id),
		'position:absolute;left:0px;top:42px;','160', '63'))
	f.write('\n<script>')
	f.write( ndata_html('dn'+str(day_id), str([]), '#dd0', '#ddd', l_str,
					'#000', '#ddd', p_str ))
	f.write( adata_html('da'+str(day_id), str([]),
				'#d00',x_str, '#0a0',y_str, '#00d',z_str ) )
	f.write( chart_html('n'+str(day_id), 'dvn'+str(day_id), 'Bar', 
							'dn'+str(day_id), '') )
	f.write( chart_html('a'+str(day_id), 'dva'+str(day_id), 'Line', 
							'da'+str(day_id), '') )
	f.write('</script></time>')
	
def write_day_stub_html(day_id, dlpath):
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	## construct html file
	try:
		f=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
	except:
		print "Day directory file not found for "+daystr
		return False
	## construct the html page for the day-view:
	f.write(zoom_indexheader(daystr, (0,1), day_id))
	f.write('<hr>')
	f.write('<p>no data found for this day</p>')
	f.write('</section></body></html>')
	f.close()
	return True
	
def write_day_html(day_id, dlpath, cnf, dta_sum, dta_rle, nt,
			x_str, y_str, z_str, l_str, p_str, cd_px):
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	ntimes = [' ', ' ', '']
	ntimes[0] = str(num2date(day_id+nt[0]))[:16]
	ntimes[1] = str(num2date(day_id+nt[1]))[:16]
	ntimes[2] = str(num2date(day_id+nt[1]-nt[0]))[11:16]
	canw=str(cd_px)
	## construct html file
	try:
		f=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
	except:
		print "Day directory file not found for "+daystr
		return False
	## construct the html page for the day-view:
	f.write(zoom_indexheader(daystr, (0,1), day_id)+'<hr>')
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
	f.write('<hr><p style="font-size:small;">24h view for '+
		daystr+' with <a href="http://www.ess.tu-darmstadt.de/hedgehog">'+
		'HedgeHog sensor</a> #'+ cnf[0:4]+'.<br/>'+
		'<a href="index_raw.html"><img src="../img/zoom.png" style="'+
		'vertical-align:middle;"></img>Raw data view for full npz file ('+
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


def write_day_zoom_html(day_id, dlpath, 
								x_str, y_str, z_str, l_str, p_str, ts, cz_px):
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	canw = str(cz_px)
	dlen = int(len(x_str)/2)
	tstr = (dayfrac2str(ts[0])[:2]+dayfrac2str(ts[0])[3:]+
				dayfrac2str(ts[1])[:2]+dayfrac2str(ts[1])[3:])
	## construct html file
	try:
		f=open(os.path.join(dlpath,str(day_id),'index_'+tstr+'.html'),"w")
	except:
		print "Day directory file not found for "+daystr
		return False
	## construct the html page for the day-view:
	f.write(zoom_indexheader(daystr, ts, day_id))
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
	f.write('<hr><p style="font-size:small;">24h view for '+
		daystr+' with a <a href="http://www.ess.tu-darmstadt.de/hedgehog">'+
		'HedgeHog sensor</a> <br/></p>')
	f.write('</section></body></html>')
	f.close()
	return True

def write_raw_day_htmls(day_id, dlpath):
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	## construct html file
	try:
		f=open(os.path.join(dlpath,str(day_id),'index_raw.html'),"w")
	except:
		print "Day directory file not found for "+daystr
		return False
	## construct the html page for the day-view:
	f.write(rawday_indexheader(daystr, day_id))
	f.write('<hr><div id="graphdiv" style="width:100%; height:300px;">'+
		'</div><script type="text/javascript">')
	f.write('dta = [')
	## load csv file and put in a js array:
	with open(os.path.join(dlpath,str(day_id),'d.csv'),"rb") as csvfile:
		dta = csv.reader(csvfile, delimiter=',')
		for row in dta:
			f.write('['+str(float(row[0]))+','+str((row[1]))+','+
					str((row[2]))+','+str((row[3]))+'],')
	f.write('];')
	f.write(
		'g3 = new Dygraph(document.getElementById("graphdiv"),'+
		'dta,{colors:["#d00","#0c0","#00d"],'+
		'labels:["time","X","Y","Z"],'+
		'strokeWidth:0.7,xAxisHeight:11,xAxisLabelWidth:80,'+
		'yAxisLabelWidth:30,axisLabelFontSize:10,'+
		'axes:{x:{valueFormatter: function(f){return new Date('+
		'f*86400000+(new Date().getTimezoneOffset()*60000)).'+
		'strftime("%H:%M:%S");},'+
		'axisLabelFormatter:function(f){return new Date('+
		'f*86400000+(new Date().getTimezoneOffset()*60000)).'+
		'strftime("%H:%M:%S");}}}});</script>')
	f.write('</section></body></html>')
	f.close()
	return True
