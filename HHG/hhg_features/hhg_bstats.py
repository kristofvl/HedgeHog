

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
			##for ii in range(x[1]):  ## over a day, this is insignificant
			cur_bin.append([x[2],x[3],x[4]])
		else:
			if cur_bin != []:
				day_bin_stats[cur_idx,:] = np.concatenate([
						np.mean(cur_bin, axis=0), np.std(cur_bin, axis=0),
						np.min(cur_bin, axis=0),  np.max(cur_bin, axis=0)])
				day_bin[cur_idx] = x ## the last seen value of the bin
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
	
## return equidistant sampling data from RLE:
def equidist_npz(dta):
	day_bin = np.zeros( sum(dta.d) ,dtype=hi.desc_hhg).view(np.recarray)
	cur_idx = 0
	for x in dta:
		for ii in range(x[1]):
			day_bin[cur_idx] = (x[0], 0, x[2],x[3],x[4], x[5],x[6])
			cur_idx+=1
	return day_bin
	
## return a sub-sampled array from dta, leading to [bins] bins:
def sub_npz(dta, bins):
	return dta[0:-1:len(dta)/bins]
	

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
	off_bins = bins-np.min(bins)
	thresh = np.max(off_bins)*(pct/100) # put treshold at pct% of maximum
	all_probs = (off_bins <= thresh) * (thresh-off_bins)/thresh
	probs = np.zeros(int(len(all_probs)/bdiv))
	for i in range(0,len(all_probs)/bdiv):
		probs[i] = np.max(all_probs[i*bdiv:(i+1)*bdiv])
	return probs
	
# convert minute-of-day to nighttime probabilities
def night_time(bins):
	p_ngt = [ 951, 951, 952, 952, 953, 953, 954, 954, 955, 955, 956, 956, 957, 957, 958, 958, 959, 959, 960, 960, 
			961, 961, 962, 962, 963, 963, 964, 964, 964, 965, 965, 966, 966, 966, 967, 967, 968, 968, 968, 969, 
			969, 970, 970, 970, 971, 971, 971, 972, 972, 972, 973, 973, 973, 974, 974, 974, 975, 975, 975, 976, 
			976, 976, 977, 977, 977, 977, 978, 978, 978, 979, 979, 979, 979, 980, 980, 980, 980, 981, 981, 981, 
			981, 982, 982, 982, 982, 983, 983, 983, 983, 983, 984, 984, 984, 984, 985, 985, 985, 985, 985, 986, 
			986, 986, 986, 986, 986, 987, 987, 987, 987, 987, 988, 988, 988, 988, 988, 988, 988, 989, 989, 989, 
			989, 989, 989, 990, 990, 990, 990, 990, 990, 990, 990, 991, 991, 991, 991, 991, 991, 991, 991, 992, 
			992, 992, 992, 992, 992, 992, 992, 992, 993, 993, 993, 993, 993, 993, 993, 993, 993, 993, 994, 994, 
			994, 994, 994, 994, 994, 994, 994, 994, 994, 994, 995, 995, 995, 995, 995, 995, 995, 995, 995, 995, 
			995, 995, 995, 995, 996, 996, 996, 996, 996, 996, 996, 996, 996, 996, 996, 996, 996, 996, 996, 996, 
			996, 996, 996, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 997, 
			997, 997, 997, 997, 997, 997, 997, 998, 998, 998, 998, 998, 998, 998, 998, 998, 998, 998, 998, 994, 
			994, 993, 993, 993, 993, 993, 993, 993, 993, 993, 993, 992, 992, 992, 992, 992, 992, 992, 992, 992, 
			991, 991, 991, 991, 991, 991, 991, 991, 990, 990, 990, 990, 990, 990, 990, 990, 989, 989, 989, 989, 
			989, 989, 988, 988, 988, 988, 988, 988, 988, 987, 987, 987, 987, 987, 986, 986, 986, 986, 986, 986, 
			985, 985, 985, 985, 985, 984, 984, 984, 984, 983, 983, 983, 983, 983, 982, 982, 982, 982, 981, 981, 
			981, 981, 980, 980, 980, 980, 979, 979, 979, 979, 978, 978, 978, 977, 977, 977, 977, 976, 976, 976, 
			975, 975, 975, 974, 974, 974, 973, 973, 973, 972, 972, 972, 971, 971, 971, 970, 970, 970, 969, 969, 
			968, 968, 968, 967, 967, 966, 966, 966, 965, 965, 964, 964, 964, 963, 963, 962, 962, 961, 961, 960, 
			960, 959, 959, 958, 958, 957, 957, 956, 956, 955, 955, 954, 954, 953, 953, 952, 952, 951, 951, 950, 
			949, 949, 948, 948, 947, 946, 946, 945, 945, 944, 943, 943, 942, 941, 941, 940, 939, 939, 938, 937, 
			937, 936, 935, 935, 934, 933, 932, 932, 931, 930, 929, 929, 928, 927, 926, 925, 925, 924, 923, 922, 
			921, 921, 920, 919, 918, 917, 916, 915, 914, 914, 913, 912, 911, 910, 909, 908, 907, 906, 905, 904, 
			903, 902, 901, 900, 899, 898, 897, 896, 895, 894, 893, 892, 891, 890, 889, 888, 887, 885, 884, 883, 
			882, 881, 880, 879, 877, 876, 875, 874, 873, 871, 870, 869, 868, 866, 865, 864, 863, 861, 860, 859, 
			857, 856, 855, 853, 852, 851, 849, 848, 846, 845, 844, 842, 841, 839, 838, 836, 835, 833, 832, 830, 
			829, 827, 826, 824, 823, 821, 820, 818, 817, 815, 813, 812, 810, 809, 807, 805, 804, 802, 800, 798, 
			797, 795, 793, 792, 790, 788, 786, 785, 783, 781, 779, 777, 776, 774, 772, 770, 768, 766, 764, 763, 
			761, 759, 757, 755, 753, 751, 749, 747, 745, 743, 741, 739, 737, 735, 733, 731, 729, 727, 725, 723, 
			721, 718, 716, 714, 712, 710, 708, 706, 703, 701, 699, 697, 695, 692, 690, 688, 686, 684, 681, 679, 
			677, 674, 672, 670, 667, 665, 663, 660, 658, 656, 653, 651, 649, 646, 644, 641, 639, 637, 634, 632, 
			629, 627, 624, 622, 619, 617, 614, 612, 609, 607, 604, 602, 599, 597, 594, 591, 589, 586, 584, 581, 
			578, 576, 573, 571, 568, 565, 563, 560, 557, 555, 552, 549, 547, 544, 541, 539, 536, 533, 530, 528, 
			525, 522, 519, 517, 514, 511, 508, 506, 503, 500, 497, 495, 492, 489, 486, 483, 481, 478, 475, 472, 
			469, 467, 464, 461, 458, 455, 452, 450, 447, 444, 441, 438, 435, 433, 430, 427, 424, 421, 418, 415, 
			413, 410, 407, 404, 401, 398, 395, 393, 390, 387, 384, 381, 378, 375, 373, 370, 367, 364, 361, 358, 
			355, 353, 350, 347, 344, 341, 338, 336, 333, 330, 327, 324, 321, 319, 316, 313, 310, 307, 305, 302, 
			299, 296, 293, 291, 288, 285, 282, 280, 277, 274, 271, 269, 266, 263, 261, 258, 255, 252, 250, 247, 
			244, 242, 239, 236, 234, 231, 229, 226, 223, 221, 218, 216, 213, 210, 208, 205, 203, 200, 198, 195, 
			193, 190, 188, 185, 183, 180, 178, 176, 173, 171, 168, 166, 164, 161, 159, 157, 154, 152, 150, 147, 
			145, 143, 141, 138, 136, 134, 132, 130, 127, 125, 123, 121, 119, 117, 115, 113, 111, 109, 107, 105, 
			103, 101, 99, 97, 95, 93, 91, 89, 87, 86, 84, 82, 80, 78, 77, 75, 73, 71, 70, 68, 
			66, 65, 63, 62, 60, 59, 57, 55, 54, 52, 51, 50, 48, 47, 45, 44, 43, 41, 40, 39, 
			37, 36, 35, 34, 33, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 
			16, 15, 15, 14, 13, 12, 12, 11, 10, 9, 9, 8, 8, 7, 6, 6, 5, 5, 4, 4, 
			4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
			0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 
			4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 10, 11, 12, 12, 13, 14, 15, 15, 16, 17, 
			18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 39, 
			40, 41, 43, 44, 45, 47, 48, 50, 51, 52, 54, 55, 57, 59, 60, 62, 63, 65, 66, 68, 
			70, 71, 73, 75, 77, 78, 80, 82, 84, 86, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 
			107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 130, 132, 134, 136, 138, 141, 143, 145, 147, 
			150, 152, 154, 157, 159, 161, 164, 166, 168, 171, 173, 176, 178, 180, 183, 185, 188, 190, 193, 195, 
			198, 200, 203, 205, 208, 210, 213, 216, 218, 221, 223, 226, 229, 231, 234, 236, 239, 242, 244, 247, 
			250, 252, 255, 258, 261, 263, 266, 269, 271, 274, 277, 280, 282, 285, 288, 291, 293, 296, 299, 302, 
			305, 307, 310, 313, 316, 319, 321, 324, 327, 330, 333, 336, 338, 341, 344, 347, 350, 353, 355, 358, 
			361, 364, 367, 370, 373, 375, 378, 381, 384, 387, 390, 393, 395, 398, 401, 404, 407, 410, 413, 415, 
			418, 421, 424, 427, 430, 433, 435, 438, 441, 444, 447, 450, 452, 455, 458, 461, 464, 467, 469, 472, 
			475, 478, 481, 483, 486, 489, 492, 495, 497, 500, 503, 506, 508, 511, 514, 517, 519, 522, 525, 528, 
			530, 533, 536, 539, 541, 544, 547, 549, 552, 555, 557, 560, 563, 565, 568, 571, 573, 576, 578, 581, 
			584, 586, 589, 591, 594, 597, 599, 602, 604, 607, 609, 612, 614, 617, 619, 622, 624, 627, 629, 632, 
			634, 637, 639, 641, 644, 646, 649, 651, 653, 656, 658, 660, 663, 665, 667, 670, 672, 674, 677, 679, 
			681, 684, 686, 688, 690, 692, 695, 697, 699, 701, 703, 706, 708, 710, 712, 714, 716, 718, 721, 723, 
			725, 727, 729, 731, 733, 735, 737, 739, 741, 743, 745, 747, 749, 751, 753, 755, 757, 759, 761, 763, 
			764, 766, 768, 770, 772, 774, 776, 777, 779, 781, 783, 785, 786, 788, 790, 792, 793, 795, 797, 798, 
			800, 802, 804, 805, 807, 809, 810, 812, 813, 815, 817, 818, 820, 821, 823, 824, 826, 827, 829, 830, 
			832, 833, 835, 836, 838, 839, 841, 842, 844, 845, 846, 848, 849, 851, 852, 853, 855, 856, 857, 859, 
			860, 861, 863, 864, 865, 866, 868, 869, 870, 871, 873, 874, 875, 876, 877, 879, 880, 881, 882, 883, 
			884, 885, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 
			905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 914, 915, 916, 917, 918, 919, 920, 921, 921, 922, 
			923, 924, 925, 925, 926, 927, 928, 929, 929, 930, 931, 932, 932, 933, 934, 935, 935, 936, 937, 937, 
			938, 939, 939, 940, 941, 941, 942, 943, 943, 944, 945, 945, 946, 946, 947, 948, 948, 949, 949, 950]
	return np.interp([x*(1440.0/bins) for x in range(0,int(bins))], range(0,1440) , p_ngt)/1000.0
	
## return sleep detection total probabilities:
def night(bins, bdiv, days_stats, day_bin):
	p = ( 128 	* night_acc(days_stats, bdiv, 2.0)
						* night_lgt((day_bin.e1>>8).tolist(), bdiv, 4.0)
						* night_time( bins/bdiv )
						)
	p = p*(p>(np.max(p)/3))
	w_l = 5
	s = np.r_[p[w_l-1:0:-1], p, p[-1:-w_l:-1] ]
	w = np.ones(w_l,'d') # moving average window
	r = np.convolve(w/w.sum(), s, mode='valid')
	return r*(r>(np.max(r)/4))

## return sleep endpoints over the day:						
def night_endpoints(p):
	## look for biggest blob:
	blob_size = max_blob_size = 0
	blob_start = max_blob_start = max_blob_stop = 0
	plen = len(p)
	p = np.concatenate([p, [0]]) # force closure:
	for i in range(0,len(p)):
		if p[i]>0:
			if blob_size == 0:
				blob_start = i
			blob_size += p[i]
		else:
			if blob_size>0:
				if (max_blob_size < blob_size):
					max_blob_size = blob_size
					max_blob_start = blob_start
					max_blob_stop  = i
				blob_size = 0
	return [1.0*max_blob_start/plen, 1.0*max_blob_stop/plen]









## these functions below are depricated:	
	
	
	
	
	

					
# get basic statistics on raw data, on a window of n original samples
def hhg_bstats_raw(dta, n):
	if dta == False:
		return False, False, False, False
	else:
		tic = time.clock()
		t  = np.array(dta.t)
		dt = np.array(dta.d)
		l  = np.array(dta.l)
		xyz  = np.zeros( (len(dta),3), dtype='u4' )
		xyz[:,0] = dta.x;		xyz[:,1] = dta.y;		xyz[:,2] = dta.z
		numsamples = sum(dt)
		numfeats = 1+numsamples/n
		mv  = np.zeros( (numfeats,6), dtype='u4' )
		ts  = np.zeros( numfeats, dtype='f8' )
		env = np.zeros( numfeats, dtype='u2' )
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
				if rf==0:
					if ii+dt[j]<=n:
						mf = dt[j]; rf = 0; j += 1;
					else:
						mf = n-ii;  rf = ii+dt[j]-n;
				else:
					if rf<=n:
						mf = rf;    rf = 0; j += 1;
					else:
						mf = n;	   rf -= n;
				ii += mf
				mv[i,:] += np.concatenate([acc, acc**2]) * mf
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
		t  = np.array(dta.t)
		l  = np.array(dta.l)
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
		t  = np.array(dta.t)
		l  = np.array(dta.l)
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


