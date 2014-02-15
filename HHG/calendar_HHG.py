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
import numpy as np
import os, subprocess
from matplotlib.dates import num2date


#data descriptor for the hedgehog default data:
desc_hhg = {	'names':   ('t',  'd',  'x',  'y',  'z',  'e1', 'e2'), 
				'formats': ('f8', 'B1', 'B1', 'B1', 'B1', 'u2', 'u2') }

## write html header:
def hhg_day_indexheader(daystr):
	return ('<!DOCTYPE html><html lang=en><meta charset=utf-8>'+
		'<link rel=stylesheet href="../st.css">'+
		'<head><title>HedgeHog Day View</title>'+
		'<script src="../Chart.js"></script></head>'+
		'<body><section id="calendar" style="width:1050px;">'+
		'<h1>'+daystr+'</h1>')
def hhg_cal_indexheader(mnth):
	hdr = ''
	for dayname in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
		hdr += ('<div class="header">'+dayname+'</div>')
	return ('<!DOCTYPE html><html lang=en><meta charset=utf-8>'+
		'<link rel=stylesheet href="st.css">'+
		'<head><title>HedgeHog Calendar View</title>'+
		'<script src="Chart.js"></script>'+
		'<script src="http://code.jquery.com/jquery-1.11.0.min.js">'+
		'</script><script>$(document).ready(function(){'+
		'$("time").mouseover(function(){'+
		'$("h1").html($(this).attr("datetime"))});});</script></head>'+
		'<body><section id=calendar><h1>'+mnth+'</h1>'+hdr+
		'<div id="days"><div id="scrollview">')

## generate html for chart canvas:
def hhg_canvas_html(varname, style, w, h):
	return ('<canvas style="'+style+'" id="'+varname+
		'" width="'+w+'" height="'+h+'"></canvas>')
		
## generate html for light dataset variable:
def hhg_ldata_html(varname, labels, fcolor, scolor, data):
	return ('var '+varname+'={labels:'+labels+
		',datasets:[{fillColor:"rgba('+fcolor+')",' + 
		'strokeColor : "rgba('+scolor+')",data:' + data +'}]};')

## generate html for acc3d dataset variable:
def hhg_adata_html(varname, labels, scx,datax, scy,datay, scz,dataz):
	return ('var '+varname+'={labels:'+labels+
		',datasets:[{strokeColor:"rgba('+scx+')",data:'+datax+'},'+
		'{strokeColor:"rgba('+scy+')",data:'+datay+'},'+
		'{strokeColor:"rgba('+scz+')",data:'+dataz+'}]};')

## generate html for chart variable:
def hhg_chart_html(varname, idname, charttype, dataname, options):
	return ('var '+varname+' = new Chart(document.getElementById('+
		'"'+idname+'").getContext("2d")).'+charttype+'('+dataname+','+
		'{'+options+'});')
		
## return html string to draw the configuration info boxes
def hhg_conf_html(cnf,smps,rle):
	g_range = pow(2,1+ord(cnf[12])-48)
	bw_lookup = [0.1, 5, 10, 25, 50, 100, 200, 400, 800, 1500]
	md_lookup = ['controller', 'sensor']			
	pw_lookup = ['normal', 'low-power', 'auto-sleep', 'low/auto']
	div_preambl = '<div id="inf" style="left:'
	left_offset = '850px'
	return (div_preambl+left_offset+';top:90px;height:70px;">'+
		'<b>HedgeHog Configuration</b>\n'+ 
		'HedgeHog_ID: '+str(cnf[0:4])+'\nfirmware:    ' + cnf[35:42] +
		'\nlogging end: 20' +str(ord(cnf[71])) + '-' +
		str(1+ord(cnf[72])).zfill(2) +'-'+ str(ord(cnf[73])).zfill(2) +
		'</div>'+div_preambl+left_offset+
		';top:197px;height:84px;"><b>Accelerometer Settings</b>\n' +
		'acc. range: +/- ' + str(g_range) +'g\nsampled at: ' + 
		str(bw_lookup[ord(cnf[13])-48]) + 'Hz (' + 
		str(md_lookup[ord(cnf[14])-48]) + ')\npower mode: ' + 
		str(pw_lookup[ord(cnf[15])-48]) + '\nRLE delta : ' + str(cnf[20])+
		'</div>'+div_preambl+left_offset+';top:320px;height:48px;">'+
		'<b>Dataset Properties</b>\n3d samples : '+str(smps).zfill(9)+
		'\nRLE samples: '+str(rle).zfill(9)+'</div>')

## write a calendar entry
def hhg_cal_entry(day_id, dlpath, f):
	## construct the html page for the calendar:
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	f.write('<time datetime="'+
		calendar.month_name[num2date(day_id).month]+' '+
		str(num2date(day_id).year)+ '"')
	if num2date(day_id).weekday()>4:
		f.write('class="weekend"')
	f.write('><a href="./'+ str(day_id) +'/index.html">'
				+ str(num2date(day_id).day) )
	## open the data and configuration for the day:
	try:
		out = np.load(os.path.join(dlpath,str(day_id),'d.npz'))
		dta = out['dta']
		cnf = str(out['conf'])
	except:
		f.write('</a></time>')
		print "Data not found for "+daystr
		return
	## reduce the data for plotting in bins:
	bins = 14400
	bdiv = 50
	day_bin = np.zeros(bins,dtype=desc_hhg).view(np.recarray)
	for x in dta:
		idx= int((x[0]-int(dta[0][0]))*bins)
		day_bin[idx] = x
	for i in range(1,bins):
		if day_bin[i][0]==0:
			day_bin[i] = day_bin[i-1]
	## construct the html for the calendar view:
	f.write('</a>')
	f.write(hhg_canvas_html('dv_l'+str(day_id),'top:0px;', '160', '27'))
	f.write(hhg_canvas_html('dv_a'+str(day_id),'top:25px;', '160', '70'))
	f.write('\n<script>')
	f.write( hhg_ldata_html('dl_'+str(day_id), 
					str(['']*(bins/bdiv)).replace(" ",""), 
					'220,220,7,1', '220,220,220,1', 
					str((day_bin.e1[::bdiv]>>8).tolist()).replace(" ","")) )
	f.write( hhg_adata_html('da_'+str(day_id),
					str(['']*(bins/bdiv)).replace(" ",""),
					'220,0,0,1', 
					str((day_bin.x[::bdiv]).tolist()).replace(" ",""),
					'0,170,0,1',
					str((day_bin.y[::bdiv]).tolist()).replace(" ",""),
					'0,0,220,1',
					str((day_bin.z[::bdiv]).tolist()).replace(" ","") ) )
	f.write(
		hhg_chart_html('l_'+str(day_id), 'dv_l'+str(day_id), 'Bar', 
							'dl_'+str(day_id), 'scaleShowLabels:false,'+
							'scaleFontSize:0,scaleShowGridLines:false,'+
							'animation:false,scaleStepWidth:32') )
	f.write(
		hhg_chart_html('a_'+str(day_id), 'dv_a'+str(day_id), 'Line', 
							'da_'+str(day_id), 'scaleShowLabels:false,'+
							'scaleFontSize:0,scaleLineWidth:0,'+
							'datasetStrokeWidth:0.5,scaleStepWidth:64') )
	f.write('</script></time>')
		
	## construct the html page for the day-view:
	try:
		df=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
	except:
		print "Day directory file not found for "+daystr
		return
	df.write(hhg_day_indexheader(daystr))
	df.write('<p>Detailed 24h view for '+daystr+' with HedgeHog'+
		' sensor #'+ cnf[0:4]+
		'. Raw data download: <a href="d.npz">here</a> (npz format, '+
		str(os.path.getsize(os.path.join(dlpath,str(day_id),'d.npz')))+
		' bytes)</p>')
	df.write( hhg_canvas_html('day_view_light', '', '832', '120') )
	df.write('</br>')
	df.write( hhg_canvas_html('day_view_acc3d', '', '832', '200') )
	df.write(hhg_conf_html(cnf,sum(dta.view(np.recarray).d),len(dta)))
	lbl = [' ']*bins;lbl[0]='00';lbl[int(bins/4)]='06';lbl[bins>>1]='12';
	lbl[int(3*bins/4)]='18';lbl[bins-1]='00';
	df.write('<script>')
	df.write( hhg_ldata_html('data_light', 
					str(['']*int(bins/bdiv)).replace(" ",""), 
					'220,220,0,7', '220,220,220,1', 
					str((day_bin.e1[::bdiv]>>8).tolist()).replace(" ","")) )
	df.write( hhg_adata_html('data_acc3d', str(lbl).replace(" ",""),
					'220,0,0,1', str((day_bin.x).tolist()).replace(" ",""),
					'0,170,0,1', str((day_bin.y).tolist()).replace(" ",""),
					'0,0,220,1', str((day_bin.z).tolist()).replace(" ","")) )
	df.write( hhg_chart_html('light', 'day_view_light', 'Bar', 
								'data_light', 'scaleStepWidth:32') )
	df.write( hhg_chart_html('acc3d', 'day_view_acc3d', 'Line', 
								'data_acc3d', 'scaleSteps:8,scaleStepWidth:32'))
	df.write('</script></section></body></html>')
	df.close()




## main script starts here: ############################################

if len(sys.argv) < 2:
	print 'use: calendar_HHG.py [download_folder]'
	exit(1)

dlpath = sys.argv[1]
if not os.path.exists(dlpath):
	exit(1)

home = os.environ['HOME']
subprocess.call(["cp", "%s/HedgeHog/HHG/st.css"%home, dlpath])
subprocess.call(["cp", "%s/HedgeHog/HHG/Chart.js"%home, dlpath])

first_day_id = int(sorted(os.walk(dlpath).next()[1])[0])
last_day_id = int(sorted(os.walk(dlpath).next()[1])[-1])+1
 # assume that we're interested in first month:
month_vw = num2date(first_day_id).month

try:
	f=open(os.path.join(dlpath,'index.html'),"w")
except:
	print 'Cannot write to index file'
	exit(1)
	
f.write(hhg_cal_indexheader('January 2014'))

# fill empty days before day of week:
wkday =  num2date(first_day_id).weekday()
for wd in range(wkday):
	hhg_cal_entry(first_day_id-wkday+wd, dlpath, f)
	
# fill in days with data:
for day_id in range(first_day_id, last_day_id):
	hhg_cal_entry(day_id, dlpath, f)
	
# add remaining days in row:
for rd in range( 7-(last_day_id-first_day_id+wkday)%7 ):
	hhg_cal_entry(last_day_id+rd, dlpath, f)

f.write('</div></div></section></body>')
f.close()

## preview:
subprocess.call(["firefox", "%s/index.html"%dlpath])
