

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



import numpy as np
import time
from matplotlib.dates import num2date
import hhg_io.hhg_import as hi


## bin-wise collect the dta stats for calendar plotting
## return mean, std, min, max for x, y, and z axes
def stats_npz(dta, bins):
	day_bin = np.zeros(bins,dtype=hi.desc_hhg).view(np.recarray)
	day_bin_stats = np.zeros( (bins,12) )-[0,0,0,1,1,1,0,0,0,0,0,0]
	cur_idx = 0; cur_bin = []
	for x in dta:
		idx = int((x[0]-int(dta[0][0]))*bins)
		if cur_idx == idx: 
			cur_bin.append([x[2],x[3],x[4]])
		else:
			if cur_bin != []:
				day_bin_stats[cur_idx,:] = np.concatenate([
						np.mean(cur_bin, axis=0), np.std(cur_bin, axis=0),
						np.min(cur_bin, axis=0),  np.max(cur_bin, axis=0)])
				day_bin[cur_idx] = x
				for k in range(0,3):
					day_bin[cur_idx][2+k] = day_bin_stats[cur_idx,
															(6+(cur_idx&1)*3)+k]
				cur_bin = []
			cur_idx = idx
	## fill in any holes with previous data:
	for cur_idx in range(1,bins):
		if day_bin_stats[cur_idx,0:6].all()==0:
			day_bin_stats[cur_idx][0:3]=day_bin_stats[cur_idx-1][0:3]
			day_bin_stats[cur_idx][6:]=day_bin_stats[cur_idx-1][6:]
		if day_bin[cur_idx][0]==0:
			day_bin[cur_idx] = day_bin[cur_idx-1]
			for k in range(0,3):
				day_bin[cur_idx][2+k] = day_bin_stats[cur_idx-1,k]
	return day_bin_stats, day_bin
	
## return acc-threshold probabilities for sleep detection:
def night_acc(stats, bdiv, pct):
	sum_std = np.sum(stats[:,3:6],1)
	max_std = np.max(sum_std)*(pct/100) # put treshold at % of maximum 
	all_probs = ( (max_std-sum_std)/max_std * 
					 ((stats[:,3]!=-1)*(sum_std <= max_std)) )
	probs = np.zeros(int(len(all_probs)/bdiv))
	for i in range(0,len(all_probs)/bdiv):
		probs[i] = np.mean(all_probs[i*bdiv:(i+1)*bdiv])
	return probs
	
## return light-threshold probabilities for sleep detection:
def night_lgt(bins, bdiv, pct):
	thresh = np.max(bins)*(pct/100) # put treshold at pct% of maximum 
	all_probs = (bins <= thresh) * (thresh-bins)/thresh
	probs = np.zeros(int(len(all_probs)/bdiv))
	for i in range(0,len(all_probs)/bdiv):
		probs[i] = np.max(all_probs[i*bdiv:(i+1)*bdiv])
	return probs
	
	
	
	
	
	
	
	
	

					
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
		if dta.dtype==hi.desc_raw:	
			return hhg_bstats_ts_raw(dta, n)
		elif dta.dtype==hi.desc_mv: 	
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
		xyz  = np.zeros( (len(dta),3), dtype='u4' )
		xyz[:,0] = dta.x;		xyz[:,1] = dta.y;		xyz[:,2] = dta.z
		numfeats = int(((dta.t[-1]-dta.t[0])*86400.0)/n) 
		mv  = np.zeros( (numfeats,6), dtype='u4' )
		ts  = np.zeros( numfeats, dtype='f8' )
		env = np.zeros( numfeats, dtype='u2' )
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
				mv[i] = np.concatenate( [ np.mean( xyz[irange], axis=0 ), 
											  np.std(  xyz[irange], axis=0 ) ] )
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
		xyz  = np.zeros( (len(dta),6), dtype='u4' )
		xyz[:,0] = dta.xm;		xyz[:,1] = dta.ym;		xyz[:,2] = dta.zm
		xyz[:,3] = dta.xv;		xyz[:,4] = dta.yv;		xyz[:,5] = dta.zv
		numfeats = int(((dta.t[-1]-dta.t[0])*86400.0)/n)
		mv  = np.zeros( (numfeats,6), dtype='u4' )
		ts  = np.zeros( numfeats, dtype='f8' )
		env = np.zeros( numfeats, dtype='u2' )
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
				mv[i] = np.mean( xyz[irange], axis=0 )
				env[i] = l[start_ii]
				i += 1
			else: break
		ts = ts[:i]; mv = mv[:i]; env = env[:i]
		toc = time.clock()
		stats = ('basis stats: '+str(len(mv))+', time(s): '+str(toc-tic))
		return ts, mv, env, stats


