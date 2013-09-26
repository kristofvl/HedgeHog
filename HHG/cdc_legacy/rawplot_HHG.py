#!/usr/bin/env python

########################################################################
#
# Filename: rawplot_HHG.py   								Author: Kristof VL
#
# Descript: Import, save and plot HedheHog datasets as raw data arrays
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



import numpy # for saving the equidistant data to ascii
import hhg_io.hhg_import as hgi
import hhg_features.hhg_bconv as hft
import hhg_plot.hhg_plot as hhg_plt
import hhg_dialogs.hhg_fopen as hhg_fopen



#check where to load from ():
filename, scr = hhg_fopen.load('/media/HEDGEHOG/log000.HHG')

#load data:
dta, stats = hgi.hhg_open_data(filename)
print stats

#convert to 
dta_e, stats = hft.hhg_equidist(dta)
print stats

#create plot:
fig = hhg_plt.Hhg_raw_plot(scr.get_width()/80,10,80)
fig.plot(1, 4, dta.t, numpy.array((dta.x, dta.y, dta.z)).T)
fig.plot(2, 4, dta.t, numpy.array((dta.l)).T>>8, 'ambient light')
fig.plot(3, 4, dta.t, ((numpy.array((dta.l)).T&0xFF)/2)-30, 'temperature')
fig.equidist_plot(4, 4, range(0,len(dta_e)), dta_e[:,:3])
fig.draw_top_text( (('user: anonymous'),(stats )) )
fig.show()

#save to ascii file:
numpy.savetxt('output.txt', dta_e, delimiter=',', fmt='%d')

