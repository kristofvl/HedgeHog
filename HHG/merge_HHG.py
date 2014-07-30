#!/usr/bin/env python2.7

########################################################################
#
# Filename: merge_HHG.py 							Authors: KristofVL
#
# Descript: merge downloadeded npz files into one
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

import sys
import numpy as np

if len(sys.argv) < 4:
	print 'use: merge_HHG.py [old npz file] [new npz file] [target npz file]'
	exit(1)
else:
	o1 = np.load(sys.argv[1])
	o2 = np.load(sys.argv[2])
	dta1 = o1['dta']
	dta2 = o2['dta']
	conf = o1['conf']
	print "timestamp check:"
	if (dta1[-1][0]<dta2[0][0]) and (int(dta1[-1][0])==int(dta2[0][0])):
		print "ok"
		dta = np.concatenate([dta1,dta2])
		np.savez(sys.argv[3],dta=dta,conf=conf)
	else:	
		print "failed"

