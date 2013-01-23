#!/usr/bin/env python

########################################################################
#
# Filename: plot_HHG.py   								Author: Kristof VL
#
# Descript: Import and plot a HedgeHog dataset
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



from numpy import *
import hhg_plot.hhg_plot as hplt
import hhg_dialogs.hhg_fopen as hhg_fopen
import hhg_io.hhg_import as hgi
from hhg_features.hhg_nght_stats import *

import pdb

#check where to load from (default is the 1st HedgeHog's data):
filename, scr = hhg_fopen.load('/media/HEDGEHOG/log000.HHG')

#open/parse the data:
dta, stats = hgi.hhg_open_data(filename)
print stats

if dta == []:
	exit()

#do night detection and prepare long-term plot, if enough data:
if len(dta)>5000:
	tme_ngt,acc_ngt,lgt_ngt,min_ngt,res_ngt, stats = hhg_nght_stats(dta)
	print stats

	#data should be loaded and analyzed, let's plot it:
	if (dta != False):
		fig = hplt.Hhg_nights_plot(scr.get_width()/80,8,80)
		if fig != False:
			nf = array((acc_ngt, lgt_ngt+100, min_ngt+200)).T
			nums = 0
			if dta.dtype == hgi.desc_raw:
				xyz = array((dta.x, dta.y, dta.z)).T
				nums = str(sum(dta.d))
			elif dta.dtype == hgi.desc_mv:
				xyz = array((dta.xm,dta.ym,dta.zm,dta.xv,dta.yv,dta.zv)).T
			fig.plot(dta.t,xyz,dta.l, tme_ngt,nf, (res_ngt*4)-20, nums)

#otherwise prepare a raw plot:
else:
	fig = hplt.Hhg_raw_plot(scr.get_width()/80,8,80)
	fig.plot(1, 3, dta.t, array((dta.x,dta.y,dta.z)).T,'3D acceleration')
	fig.plot(2, 3, dta.t, array((dta.l)).T>>8, 'ambient light')
	fig.plot(3, 3, dta.t, (array((dta.l)).T&0xFF)/2-30, 'temperature')
	fig.draw_top_text( (('user: anonymous'),(stats )) )
	fig.show()

# if selected, write data to binary file (so it can be used later):
if fig.save_dta_file:
	print 'saving data to ' + fig.save_dta_file
	if (fig.save_dta_file.endswith(".csv") or fig.save_dta_type=='csv'):
		from matplotlib.mlab import rec2csv
		rec2csv(dta,fig.save_dta_file)
	else:
		save(fig.save_dta_file, dta)

