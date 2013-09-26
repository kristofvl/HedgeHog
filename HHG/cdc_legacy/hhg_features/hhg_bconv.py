

########################################################################
#
# Filename: hhg_bconv.py					Authors: Kristof VL, Eugen Berlin
#
# Descript: Get basic conversions for HedgeHog datasets
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
import time

# unique encoding for different types of features:
HHGFEAT_NONE		= 000	
HHGFEAT_EQUIDIST	= 002	# convert to equidistant array	
		
# convert the original data in an equidistant-sampled array
def hhg_equidist(dta):
	if dta == False:
		return False
	else:
		tic = time.clock()
		rle = array((dta.d,dta.x,dta.y,dta.z,dta.l)).transpose()
		dta_e = rle[:,1:].repeat(rle[:,0],axis=0)
		toc = time.clock()
		stats = ('samples: '+str(len(dta_e))+', time(s): '+str(toc-tic))
		return dta_e, stats
