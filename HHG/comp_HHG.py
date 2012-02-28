#!/usr/bin/env python

########################################################################
#
# Filename: comp_HHG.py   								Author: Kristof VL
#
# Descript: Import and and compare features for multiple datasets
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
  


import numpy
import hhg_io.hhg_import as hgi
import hhg_features.hhg_bstats as hft
import matplotlib.pyplot as plt
import matplotlib.dates as mld
import hhg_plot.hhg_plot as hhg_plt


########################################################################
#       Change the table below to compare datasets and features        #
########################################################################
#list of files to compare, and which features and params to use:       #
#filen = '../sampledata/test/log000.HHG'
file1 = '../subject_a.npy'
file2 = '../subject_k.npy'
files = (	(file1, hft.HHGFEAT_TS_BSTATS, (10,0)),
				(file1, hft.HHGFEAT_TS_BSTATS, (100,0)),
				(file2, hft.HHGFEAT_TS_BSTATS, (10,0)),
				(file2, hft.HHGFEAT_TS_BSTATS, (100,0))
			)
########################################################################

#create plotting object:
fig = hhg_plt.Hhg_comp_plot(14,10,80)
	
#for each file above:
it = 0
for f in files:

	#load data:
	dta, stats = hgi.hhg_open_data(f[0])
	print stats

	#calculate basic stats anew (put to False to avoid re=calculating):
	if True:
		if f[1]==hft.HHGFEAT_BSTATS:
			ts, dta_mv, env, stats = hft.hhg_bstats_raw(dta, f[2][0])
		elif f[1]==hft.HHGFEAT_RWTS_BSTATS:
			ts, dta_mv, env, stats = hft.hhg_bstats_ts_raw(dta, f[2][0])
		elif f[1]==hft.HHGFEAT_MVTS_BSTATS:
			ts, dta_mv, env, stats = hft.hhg_bstats_ts_mv(dta, f[2][0])
		elif f[1]==hft.HHGFEAT_TS_BSTATS:
			ts, dta_mv, env, stats = hft.hhg_bstats_ts(dta, f[2][0])
		else: print 'Error: unknown feature id'
		print stats
		numpy.save(f[0][:-4]+'_ts'+'.npy', ts)
		numpy.save(f[0][:-4]+'_mv'+'.npy', dta_mv)
		numpy.save(f[0][:-4]+'_env'+'.npy', env)
	else: # load previouslz calculated features
		ts = numpy.load(f[0][:-4]+'_ts'+'.npy')
		dta_mv = numpy.load(f[0][:-4]+'_mv'+'.npy')
		env = numpy.load(f[0][:-4]+'_env'+'.npy')
	
	#sum up variances to get a 1D timeseries
	sumv = numpy.sum(dta_mv[:,3:6], axis=1)
		
	#plot results:
	fig.plot(it, len(files)*2, ts, dta_mv[:,0:3], sumv)

	it+=2 # update the subplot iterator

fig.show()
