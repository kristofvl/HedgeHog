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
from calendar import TimeEncoding, month_name





## write html headers:
def hhg_htmlhead(title, csspath, jspath):
	return ('<!DOCTYPE html><html lang=en><meta charset=utf-8>'+
		'<link rel=stylesheet href="'+csspath+'">'+
		'<head><title>'+title+'</title>'+
		'<script src="'+jspath+'"></script>')
def hhg_day_indexheader(daystr, day_id):
	return (hhg_htmlhead('HedgeHog Day View','../st.css','../Chart.js')+
		'</head><body><section id="calendar" style="width:1100px;">'+
		'<h1><a href="../'+str(day_id-1)+
		'/index.html"><span class="a-left"></span></a>'+daystr+
		'<a href="../'+str(day_id+1)+
		'/index.html"><span class="a-right"></span></a>'+
		'<a style="text-align=right;" href="../index.html">'+
		'<span class="a-up"></span></a></h1>')
def hhg_cal_indexheader(mnth):
	hdr = ''
	for dayname in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
		hdr += ('<div class="header">'+dayname+'</div>')
	return (hhg_htmlhead('HedgeHog Calendar View','st.css','Chart.js')+
		'<script src="http://code.jquery.com/jquery-1.11.0.min.js">'+
		'</script><script>$(document).ready(function(){'+
		'$("time").mouseover(function(){'+
		'$("h1").html($(this).attr("datetime"))});});</script></head>'+
		'<body><section id=calendar><h1>'+mnth+'</h1>'+hdr+
		'<div id="days"><div id="scrollview">')

## generate html for chart canvas:
def hhg_canvas_html(varname, style, w, h):
	return ('<canvas style="'+style+
		'" id="'+varname+'" width="'+w+'" height="'+h+'"></canvas>')
		
## generate html for light dataset variable:
def hhg_ldata_html(varname, labels, fcolor, scolor, data):
	return ('var '+varname+'={l:'+labels+',ds:[{fc:"'+
		fcolor+'",'+'sc:"'+scolor+'",d:'+data+'}]};')

## generate html for night/light dataset variable:
def hhg_ndata_html(varname, labels, fcl, scl, datal, fcn, scn, datan ):
	return ('var '+varname+'={l:'+labels+
		',ds:[{fc:"'+fcl+'",sc:"'+scl+'",d:' + datal +'},'+
		'{fc:"'+fcn+'",'+'sc:"'+scn+'",d:' + datan +'}]};')

## generate html for acc3d dataset variable:
def hhg_adata_html(varname, labels, scx,datax, scy,datay, scz,dataz):
	return ('var '+varname+'={l:'+labels+
		',ds:[{sc:"'+scx+'",d:'+datax+'},'+
		'{sc:"'+scy+'",d:'+datay+'},{sc:"'+scz+'",d:'+dataz+'}]};')

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


## write a calendar entry
def hhg_cal_entry(day_id, dlpath, f):
	## helper function to get month name:
	def get_month_name(month_no, locale):
		with TimeEncoding(locale) as encoding:
			s = month_name[month_no]
			if encoding is not None:
				s = s.decode(encoding)
			return s
	## construct the html page for the calendar:
	daystr = str(num2date(day_id).year)+'-'
	daystr += str(num2date(day_id).month).zfill(2)
	daystr += '-' + str(num2date(day_id).day).zfill(2)
	f.write('<time datetime="'+
		get_month_name(num2date(day_id).month, "en_US.UTF-8")+
		' '+str(num2date(day_id).year)+ '"')
	if num2date(day_id).weekday()>4:
		f.write('class="weekend"')
	f.write('><a href="./'+ str(day_id) +'/index.html">'
				+ str(num2date(day_id).day) )
	## open the data and configuration for the day:
	dfile = os.path.join(dlpath,str(day_id),'d.npz')
	bins = 1440*2
	bdiv = 17
	try:
		out = np.load(dfile)
		dta = out['dta']
		cnf = str(out['conf'])
	except:
		f.write('</a></time>')
		print "Data not found for "+daystr
		return
	tic = time.clock()
	days_stats, day_bin = hf.stats_npz(dta, bins)
	probs = ( 128 	* hf.night_acc(days_stats, bdiv, 2.0)
						* hf.night_lgt((day_bin.e1>>8).tolist(), bdiv, 4.0)
						)
	probs_str = str( map(int,probs.tolist()) ).replace(" ","")
	toc = time.clock()
	print daystr+' took '+str(toc-tic)+' seconds'
	
	## construct the html for the calendar view's plots:
	f.write('</a>')
	f.write(hhg_canvas_html('dvn'+str(day_id),
		'position:absolute;left:0px;top:14px;', '160', '30'))
	f.write(hhg_canvas_html('dva'+str(day_id),
		'position:absolute;left:0px;top:42px;','160', '63'))
	f.write('\n<script>')
	f.write( hhg_ndata_html('dn'+str(day_id), str([]), '#dd0', '#ddd', 
					str((day_bin.e1[::bdiv]>>8).tolist()).replace(" ",""),
					'#000', '#ddd', probs_str ))
	f.write( hhg_adata_html('da'+str(day_id),str([]),
				'#d00',str((day_bin.x[::bdiv]).tolist()).replace(" ",""),
				'#0a0',str((day_bin.y[::bdiv]).tolist()).replace(" ",""),
				'#00d',str((day_bin.z[::bdiv]).tolist()).replace(" ","") ) )
	f.write(
		hhg_chart_html('n'+str(day_id), 'dvn'+str(day_id), 'Bar', 
							'dn'+str(day_id), '') )
	f.write(
		hhg_chart_html('a'+str(day_id), 'dva'+str(day_id), 'Line', 
							'da'+str(day_id), '') )
	f.write('</script></time>')
		
	## construct the html page for the day-view:
	lbl = [' ']*bins;lbl[0]='00';lbl[int(bins/4)]='06';lbl[bins>>1]='12';
	lbl[int(3*bins/4)]='18';lbl[bins-1]='00';
	try:
		df=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
	except:
		print "Day directory file not found for "+daystr
		return
	df.write(hhg_day_indexheader(daystr, day_id))
	df.write('<hr>')
	
	df.write(hhg_conf_html(cnf,sum(dta.view(np.recarray).d),len(dta)))
	df.write( '<div id="inf" style="left:865px;top:379px;height:70px;">'+
		'<b>Sleep Estimation</b>\ntotal sleep: 00.00 Hours\n'+
		'start: 23:00,'+daystr+'\n' + 
		'stop:  23:00,'+daystr+'\n' +'</div>')
	df.write('<div class="icn-sun"></div>')
	df.write( hhg_canvas_html('day_view_light', 'position:relative;', 
			'832', '120') )
	df.write('</br><div class="icn-act"></div>')
	df.write( hhg_canvas_html('day_view_acc3d', 'position:relative;',
			'832', '200') )
	df.write('</br><div class="icn-slp"></div>')
	df.write( hhg_canvas_html('night_view_prb', 'position:relative;', 
			'832', '100') )
	df.write('<script>')
	df.write( hhg_ldata_html('d_light', str([]),'#dd0', '#ddd', 
					str((day_bin.e1[::bdiv]>>8).tolist()).replace(" ","")) )
	df.write( hhg_adata_html('d_acc3d', str(lbl).replace(" ",""),
					'#d00', str((day_bin.x).tolist()).replace(" ",""),
					'#0c0', str((day_bin.y).tolist()).replace(" ",""),
					'#00d', str((day_bin.z).tolist()).replace(" ","")) )
	df.write( hhg_ldata_html('d_night',str([]),'#111','#ddd', probs_str))
	df.write( hhg_chart_html('light', 'day_view_light', 'Bar', 
								'd_light', 'scaleShowLabels:true,'+
								'scaleFontSize:12,scaleShowGridLines:true,'+
								'animation:true,scaleStepWidth:32') )
	df.write( hhg_chart_html('acc3d', 'day_view_acc3d', 'Line', 
								'd_acc3d', 'scaleSteps:8,scaleShowLabels:true,'+
								'scaleFontSize:12,scaleLineWidth:1,'+
								'datasetStrokeWidth:0.5,scaleStepWidth:32'))
	df.write( hhg_chart_html('night', 'night_view_prb', 'Bar', 
								'd_night', 'scaleShowLabels:true,'+
							'scaleFontSize:12,scaleShowGridLines:true,'+
							'animation:true,scaleStepWidth:32') )
	df.write('</script>')
	df.write('<hr><p style="font-size:small;">Detailed 24h view for '+
		daystr+' with <a href="http://www.ess.tu-darmstadt.de/hedgehog">'+
		'HedgeHog sensor</a> #'+ cnf[0:4]+
		'. Raw data download: <a href="d.npz">here</a> (npz format, '+
		str(os.path.getsize(os.path.join(dlpath,str(day_id),'d.npz')))+
		' bytes)</p>')
	df.write('</section></body></html>')
	df.close()



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
