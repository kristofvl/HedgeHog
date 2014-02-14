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

## write html header
def hhg_day_indexheader():
	return ('<!DOCTYPE html><html lang=en><meta charset=utf-8>'+
		'<link rel=stylesheet href="../st.css">'+
		'<head><title>HedgeHog Day View</title>'+
		'<script src="../Chart.js"></script></head>')
def hhg_cal_indexheader():
	return ('<!DOCTYPE html><html lang=en><meta charset=utf-8>'+
		'<link rel=stylesheet href="st.css">'+
		'<head><title>HedgeHog Day View</title>'+
		'<script src="Chart.js"></script></head>')
	
def hhg_conf_html(cnf,smps,rle):
	g_range = pow(2,1+ord(cnf[12])-48)
	bw_lookup = [0.1, 5, 10, 25, 50, 100, 200, 400, 800, 1500]
	md_lookup = ['controller', 'sensor']			
	pw_lookup = ['normal', 'low-power', 'auto-sleep', 'low/auto']
	htstr = ('<div id="inf" style="left:850px;top:90px;height:72px;">'+
		'<b>HedgeHog Configuration</b>\n'+ 
		'HedgeHog_ID: '+str(cnf[0:4])+'\nfirmware:    ' + cnf[35:42] +
		'\nlogging end: 20' +str(ord(cnf[71])) + '-' +
		str(1+ord(cnf[72])).zfill(2) +'-'+ str(ord(cnf[73])).zfill(2) +
		'</div><div id="inf" style="left:850px;top:190px;height:84px;">'+
		'<b>Accelerometer Settings</b>\n' +
		'acc. range: +/- ' + str(g_range) +'g\nsampled at: ' + 
		str(bw_lookup[ord(cnf[13])-48]) + 'Hz (' + 
		str(md_lookup[ord(cnf[14])-48]) + ')\npower mode: ' + 
		str(pw_lookup[ord(cnf[15])-48]) + '\nRLE delta : ' + str(cnf[20])+
		'</div><div id="inf" style="left:850px;top:310px;height:50px;">'+
		'<b>Dataset Properties:</b>\n3d samples : '+str(smps).zfill(9)+
		'\nRLE samples: '+str(rle).zfill(9)+
		'</div>')
	return htstr

## write a calendar entry
def hhg_cal_entry(day_id, month_view, dlpath, f):
	## construct the html page for the calendar:
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
	## open the data and configuration for the day:
	try:
		out = np.load(os.path.join(dlpath,str(day_id),'d.npz'))
		dta = out['dta']
		cnf = str(out['conf'])
	except:
		f.write('</a></time>')
		print "Data not found"
		return
	## open the data and configuration for the day:
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
	f.write('</a><canvas style="top:0px;"'+
		'id="dv_l'+str(day_id)+'" width="160" height="27">'+
		'</canvas><canvas style="top:25px;"'+
		'id="dv_a'+str(day_id)+'" width="160" height="70"></canvas>')
	f.write('\n<script>')
	f.write('var dl_'+str(day_id)+'={labels:'+
		str(['']*(bins/bdiv)).replace(" ","") +
		',datasets:[{fillColor:"rgba(220,220,0,7)",' + 
		'strokeColor : "rgba(220,220,220,1)",data:' + 
		str((day_bin.e1[::bdiv]>>8).tolist()).replace(" ","")+'}]};')
	f.write('var da_'+str(day_id)+'={labels: ' +
		str(['']*(bins/bdiv)).replace(" ","")+
		',datasets:[{strokeColor:"rgba(220,0,0,1)",data:'+
		str((day_bin.x[::bdiv]).tolist()).replace(" ","")+
		'},{strokeColor:"rgba(0,170,0,1)",data:'+
		str((day_bin.y[::bdiv]).tolist()).replace(" ","")+
		'},{strokeColor:"rgba(0,0,220,1)",data:'+
		str((day_bin.z[::bdiv]).tolist()).replace(" ","")+'}]};')
	f.write('var l_'+str(day_id)+'=new Chart(document.getElementById('+
		'"dv_l'+str(day_id)+'").getContext("2d")).Bar(dl_'+str(day_id)+
		',{scaleShowLabels:false,scaleShowGridLines:false,'+
		'scaleFontSize:0,scaleStepWidth:32,animation:false});')
	f.write('var a_'+str(day_id)+'=new Chart(document.getElementById('+
		'"dv_a'+str(day_id)+'").getContext("2d")).Line(da_'+str(day_id)+
		',{scaleShowLabels:false,scaleFontSize:0,'+
		'scaleLineWidth:0,datasetStrokeWidth:0.5,scaleStepWidth:64});')
	f.write('</script></time>')
		
	## construct the html page for the day-view:
	try:
		df=open(os.path.join(dlpath,str(day_id),'index.html'),"w")
	except:
		print "Day directory file not found"
		return
	df.write(hhg_day_indexheader())
	df.write('<body><section id="calendar"><h1>'+daystr+'</h1>')
	df.write('<p>Detailed 24h view for '+daystr+' with HedgeHog'+
		' sensor #'+ cnf[0:4]+
		'. Raw data download: <a href="d.npz">here</a> (npz format, '+
		str(os.path.getsize(os.path.join(dlpath,str(day_id),'d.npz')))+
		' bytes)</p>')
	df.write('<canvas id="day_view_light" width="832" height="120">'+
		'</canvas></br>'+
		'<canvas id="day_view_acc3d" width="832" height="200"></canvas>')
	df.write(hhg_conf_html(cnf,sum(dta.view(np.recarray).d),len(dta)))
	lbl = [' ']*bins;lbl[0]='00';lbl[int(bins/4)]='06';lbl[bins>>1]='12';
	lbl[int(3*bins/4)]='18';lbl[bins-1]='00';
	df.write('<script>var data_light={'+
		'labels:'+str(['']*int(bins/bdiv)).replace(" ","")+
		',datasets:[{fillColor : "rgba(220,220,0,7)",'+
		'strokeColor:"rgba(220,220,220,1)",data:'+
		str((day_bin.e1[::bdiv]>>8).tolist()).replace(" ","")+
		'}]};var data_acc3d = {labels: '+str(lbl).replace(" ","")+
		',datasets:[{strokeColor : "rgba(220,0,0,1)",data: '+
		str((day_bin.x).tolist()).replace(" ","")+'},'+
		'{strokeColor : "rgba(0,170,0,1)",data: '+
		str((day_bin.y).tolist()).replace(" ","")+'},'+
		'{strokeColor : "rgba(0,0,220,1)",data: '+
		str((day_bin.z).tolist()).replace(" ","")+'}]};')
	df.write('var light = new Chart(document.getElementById('+
		'"day_view_light").getContext("2d")).Bar(data_light,'+
		'{scaleStepWidth:32});')		
	df.write('var acc3d = new Chart(document.getElementById('+
		'"day_view_acc3d").getContext("2d")).Line(data_acc3d,'+
		'{scaleSteps:8,scaleStepWidth:32});')
	df.write('</script></section></body></html>')
	df.close()


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

f=open(os.path.join(dlpath,'index.html'),"w")
f.write(hhg_cal_indexheader())
f.write('<body><section id=calendar>')
f.write('<h1>'+calendar.month_name[month_vw]+' '
				 +str(num2date(first_day_id).year)+'</h1>')
for dayname in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
	f.write('<div class="header">'+dayname+'</div>')
f.write('<div id="days"><div id="scrollview">')

# fill empty days before day of week:
wkday =  num2date(first_day_id).weekday()
for wd in range(wkday):
	hhg_cal_entry(first_day_id-wkday+wd, month_vw, dlpath, f)
	
# fill in days with data:
for day_id in range(first_day_id, last_day_id):
	hhg_cal_entry(day_id, month_vw, dlpath, f)
	
# add remaining days in row:
for rd in range( 7-(last_day_id-first_day_id+wkday)%7 ):
	hhg_cal_entry(last_day_id+rd, month_vw, dlpath, f)
	
f.write('</div></div></section></body>')
f.close()

subprocess.call(["firefox", "%s/index.html"%dlpath])
