

########################################################################
#
# Filename: hhg_plotter.py								Author: Kristof VL
#
# Descript: Plotting routines for HedgeHog datasets
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



import matplotlib.pyplot as plt
import matplotlib.dates as mld
import numpy





# main plotting routine for generic purposes
class HHG_plotter:
	
	def __init__(self, fig_x=10, fig_y=6, fdpi=80):
		try:
			self.fig = plt.figure(	num=None, figsize=(fig_x, fig_y), 
									dpi=fdpi, facecolor='w', edgecolor='k' )
			self.acc_ax = plt.subplot(2,1,2)
			self.ngt_ax = plt.subplot(4,1,1, sharex=self.acc_ax)
			self.env_ax = plt.subplot(4,1,2, 
									axisbg='#777777', sharex=self.acc_ax)
			plt.subplots_adjust(	left  = 0.02, # left side of the subplots
										right = 0.98, # right side of the subplots
										bottom = 0.05,# bottom of the subplots 
										top = 0.9,    # top of the subplots 
										wspace = 0.2, # width space betw. subplots
										hspace = 0.1  # height space btw. subplots
										)
			self.acc_samples = 0
			self.ngt_samples = 0
			self.begin_date = 'unknown'
			self.end_date = 'unknown'
			self.user_name = 'anonymous'
		except ValueError:
			return 0
			
	def plot_ov(self, d):
		# title:
		self.fig.text( 0.02, 0.95, 'dates_span: ' + 
			self.begin_date +' -> '+self.end_date, 
			ha='left',va='baseline',bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4),
			family='monospace', size='medium')
		self.fig.text( 0.4, 0.95, 'samples_#: ' + str(self.acc_samples), 
			ha='left',va='baseline',bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4),
			family='monospace', size='medium')
		self.fig.text( 0.6, 0.95, 'features_#: ' + str(self.ngt_samples), 
			ha='left',va='baseline',bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4),
			family='monospace', size='medium')
		self.fig.text( 0.98, 0.95, 'user_id: ' + self.user_name, 
			ha='right',va='baseline',bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4),
			family='monospace', size='medium')
		plt.show()
			 
	def plot_acc_finish(self):
		self.acc_ax.grid(color='k', linestyle=':', linewidth=0.5)
		plt.axis('tight')
		plt.setp(self.acc_ax.get_yticklabels(), visible=False)
		self.acc_ax.yaxis.set_label_text('acceleration', fontsize=10)
		self.acc_ax.xaxis.set_major_formatter(mld.DateFormatter('%H:%M'))
		self.acc_ax.fmt_xdata = mld.DateFormatter('%Y-%m-%d, %H:%M:%S')
		self.acc_ax.fmt_ydata = lambda y: '%03.03f'%y
		# todo: check out how we can rotate x=axis without xshare interfering:
		#plt.setp(self.acc_ax.get_xticklabels(), fontsize=8)
		#plt.setp(self.acc_ax.get_xticklabels(), rotation=45)
		#self.fig.autofmt_xdate()
		#for l in self.acc_ax.get_xticklabels():
		#	l.set_fontsize(8)
		#	l.set_rotation(45)
					 
	def plot_env(self, t, l):
		self.env_ax.fill_between(t,l,facecolor='yellow', linewidth=0, 
			alpha=.6)
		self.env_ax.grid(color='k', linestyle=':', linewidth=0.5)
		ca = self.env_ax.axes
		ca.set_xlim(t[1],t[-1])
		ca.set_ylim(0,128)
		plt.setp(self.env_ax.get_xticklabels(), visible=False)
		plt.setp(self.env_ax.get_yticklabels(), visible=False)
		ca.yaxis.set_label_text('ambient light', fontsize=10)
		
	def plot_ngt(self, t, acc_ngt, lgt_ngt, min_ngt, res_ngt):
		ca = self.ngt_ax
		ca.plot(t, acc_ngt, '-', color='b', linewidth=0.5, label='motion')
		ca.plot(t, lgt_ngt+100,'-', color='g', linewidth=0.5, label='light')
		ca.plot(t, min_ngt+200,'-', color='r', linewidth=0.5, label='time')
		ca.plot(t, res_ngt*4-20,'s', color='#000000', linewidth=0.5)
		ca.grid(color='k', linestyle=':', linewidth=0.5)
		ca.axes.set_ylim(0, 420)
		plt.setp(ca.get_xticklabels(), visible=False)
		plt.setp(ca.get_yticklabels(), visible=False)
		ca.axes.yaxis.set_label_text('night', fontsize=10)
		self.ngt_samples = len(t)
		
# plots raw acceleration data
class HHG_raw_plotter(HHG_plotter):
	def plot_acc(self, t, x, y, z):
		self.acc_ax.plot_date(t,x,'-', linewidth=0.5)
		self.acc_ax.plot_date(t,y,'-', linewidth=0.5)
		self.acc_ax.plot_date(t,z,'-', linewidth=0.5)
		self.begin_date = str(mld.num2date(t[0]))[:10]
		self.end_date   = str(mld.num2date(t[-1]))[:10]
		self.acc_samples = len(t)
		
# plots mean-variance accunulated data
class HHG_mv_plotter(HHG_plotter):
	def plot_acc(self, t, xm, ym, zm, xv, yv, zv):
		self.acc_ax.plot_date(t,xm,'-', linewidth=0.5)
		self.acc_ax.plot_date(t,ym,'-', linewidth=0.5)
		self.acc_ax.plot_date(t,zm,'-', linewidth=0.5)
		self.acc_ax.plot_date(t,xv,'-', linewidth=0.5)
		self.acc_ax.plot_date(t,yv,'-', linewidth=0.5)
		self.acc_ax.plot_date(t,zv,'-', linewidth=0.5)
		self.begin_date = str(mld.num2date(t[0]))[:10]
		self.end_date   = str(mld.num2date(t[-1]))[:10]
		self.acc_samples = len(t)
		
			
