

########################################################################
#
# Filename: hhg_bstats.py							Author: Kristof VL
#
# Descript: Get basic mean-variance statistics for HedgeHog datasets
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
from matplotlib.dates import num2date
import hhg_io.hhg_import as hio




# unique encoding for different types of features:
HHGFEAT_BSTATS      = 21	# basic statistics for raw data on 10ms scale
HHGFEAT_TS_BSTATS   = 22	# basic timestamp-based statistics (1s scale)
HHGFEAT_RWTS_BSTATS = 220	#    ... implementation for raw data
HHGFEAT_MVTS_BSTATS = 221	#    ... implementation for mean-var data

					
# get basic statistics on raw data, on a window of n original samples
def hhg_bstats_raw(dta, n):
	if dta == False:
		return False, False, False, False
	else:
		tic = time.clock()
		t  = array(dta.t);		dt = array(dta.d)
		l  = array(dta.l)
		xyz  = zeros( (len(dta),3), dtype='u4' )
		xyz[:,0] = dta.x;		xyz[:,1] = dta.y;		xyz[:,2] = dta.z
		numsamples = sum(dt)
		numfeats = 1+numsamples/n
		mv  = zeros( (numfeats,6), dtype='u4' )
		ts  = zeros( numfeats, dtype='f8' )
		env = zeros( numfeats, dtype='u2' )
		i = j = 0; rf = 0; 
		while j<len(dt):
			ii = 0; # renew counting till n
			while j<len(dt) and ii<n:
				#get timestamp from the approx. the middle of the window
				if ii<n/2:
					ts[i]  = t[j]
					env[i] = l[j]
				acc = xyz[j,:]
				#array([x[j],y[j],z[j]], dtype='u4')
				#calculate multipl. & res. factors
				if rf==0:									# 
					if ii+dt[j]<=n:						#  
						mf = dt[j]; rf = 0; j += 1;	# 
					else: 									# 
						mf = n-ii;  rf = ii+dt[j]-n;  # 
				else: 										# 	
					if rf<=n:								# 
						mf = rf;    rf = 0; j += 1;	# 
					else:										#
						mf = n;	   rf -= n; 			# 
				ii += mf
				mv[i,:] += concatenate([acc, acc**2]) * mf
			i += 1
		mv[:i,3:6] -= (mv[:,0:3]**2)/n
		mv[:i,0:3] /= n
		toc = time.clock()
		stats = ('basis stats: '+str(len(mv))+', time(s): '+str(toc-tic))
		return ts, mv, env, stats

# get basic statistics on raw data, on a window of n seconds
def hhg_bstats_ts(dta, n):
	if dta == False:
		return False, False, False, False
	else:
		if dta.dtype==hio.desc_raw:	
			return hhg_bstats_ts_raw(dta, n)
		elif dta.dtype==hio.desc_mv: 	
			return hhg_bstats_ts_mv(dta, n)
		else:
			return False, False, False, False

# get basic statistics on raw data, on a window of n seconds
def hhg_bstats_ts_raw(dta, n):
	if dta == False:
		return False, False, False, False
	else:
		tic = time.clock()
		t  = array(dta.t)
		l  = array(dta.l)
		xyz  = zeros( (len(dta),3), dtype='u4' )
		xyz[:,0] = dta.x;		xyz[:,1] = dta.y;		xyz[:,2] = dta.z
		numfeats = int(((dta.t[-1]-dta.t[0])*86400.0)/n) 
		mv  = zeros( (numfeats,6), dtype='u4' )
		ts  = zeros( numfeats, dtype='f8' )
		env = zeros( numfeats, dtype='u2' )
		int_size = (n/86400.0) # interval size (86400 seconds in a day)
		i = ii = 0; 
		while ii<len(t):
			start_ii = ii
			start_t  = t[ii]
			while (t[ii] <= (start_t+int_size)):
				ii += 1
				if (ii == len(t)): break
			if ii<len(t) and i<len(ts):
				irange = range(start_ii,ii)
				ts[i] = t[start_ii]
				mv[i] = concatenate( [ mean( xyz[irange], axis=0 ), 
											  std(  xyz[irange], axis=0 ) ] )
				env[i] = l[start_ii]
				i += 1
			else: break
		ts = ts[:i]; mv = mv[:i]; env = env[:i]
		toc = time.clock()
		stats = ('basis stats: '+str(len(mv))+', time(s): '+str(toc-tic))
		return ts, mv, env, stats

# get basic statistics on mean-var data, on a window of n seconds
def hhg_bstats_ts_mv(dta, n):
	if dta == False:
		return False, False, False, False
	else:
		tic = time.clock()
		t  = array(dta.t)
		l  = array(dta.l)
		xyz  = zeros( (len(dta),6), dtype='u4' )
		xyz[:,0] = dta.xm;		xyz[:,1] = dta.ym;		xyz[:,2] = dta.zm
		xyz[:,3] = dta.xv;		xyz[:,4] = dta.yv;		xyz[:,5] = dta.zv
		numfeats = int(((dta.t[-1]-dta.t[0])*86400.0)/n)
		mv  = zeros( (numfeats,6), dtype='u4' )
		ts  = zeros( numfeats, dtype='f8' )
		env = zeros( numfeats, dtype='u2' )
		int_size = (n/86400.0) # interval size (86400 seconds in a day)
		i = ii = 0; 
		while ii<len(t):
			start_ii = ii
			start_t  = t[ii]
			while (t[ii] <= (start_t+int_size)):
				ii += 1
				if (ii == len(t)): break
			if ii<len(t) and i<len(ts):
				irange = range(start_ii,ii)
				ts[i] = t[start_ii]
				mv[i] = mean( xyz[irange], axis=0 )
				env[i] = l[start_ii]
				i += 1
			else: break
		ts = ts[:i]; mv = mv[:i]; env = env[:i]
		toc = time.clock()
		stats = ('basis stats: '+str(len(mv))+', time(s): '+str(toc-tic))
		return ts, mv, env, stats


