
########################################################################
#
# Filename: hhg_plot_image.py								Author: Kristof VL/ Enzo Torella
#
# Descript: Plotting image routines for HedgeHog datasets
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


import os
import matplotlib, numpy, gtk
matplotlib.use('GTKAgg')
matplotlib.use('Agg')
from matplotlib.pyplot import *
from matplotlib.pylab import *
import matplotlib.dates as mld
import hhg_dialogs.hhg_fsave as fsave_dlg


# main plotting routine for generic purposes
class Hhg_plot:
	def __init__(self, fig_x=10, fig_y=6, fdpi=80):
		self.fig = 0
		self.save_dta_file = ''
		self.labels = None
		self.a_ax = None
		try:
			self.fig = figure(	num=None, figsize=(fig_x, fig_y), 
										dpi=fdpi, facecolor='w', edgecolor='k' )
		except ValueError:
			return 0
	def fix_margins(self):
			subplots_adjust(	left  = 0.02, right = 0.98, # left, right, 
									bottom = 0.05,top = 0.9, # bottom and top
									wspace = 0.2, # width space betw. subplots
									hspace = 0.1  # height space btw. subplots
								)
	def draw_top_text(self, strs):
		# evenly draw the strings at the top of the plotting window
		total_strlength = sum([ len(i) for i in strs])
		# draw the first string aligned to the left, last to the right:
		t = self.fig.text( 0.02, 0.95, strs[0], ha='left')
		setp(t, va='baseline', family='monospace', size='medium', 
				bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4))
		if len(strs)>1:	
			t = self.fig.text( 0.98, 0.95, strs[-1], ha='right')
			setp(t, va='baseline', family='monospace', size='medium', 
					bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4))
			# the middle ones should be spread across the plot  <-------->
			for i in range(1,len(strs)-1):
				t =self.fig.text(.2+float((i)*(.9/(len(strs)))),.95,strs[i])
				setp(t, ha='center', va='baseline', family='monospace',
					size='medium', 
					bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4))	
	# obtain the filename to which the original data should be saved
	def save_data(self, tdata):
		self.save_dta_file = fsave_dlg.hhg_fsave()
	# read user clicks on the plot for annotation
	def mark_label(self, tb_data):
		res = ginput(2,timeout=-1) # wait for the user to mark two points
		self.labels = [res[0][0], res[1][0]]
		self.add_labels(self.lblcombo.get_active_text())
	def add_labels(self, label_str):
		arrow_props = dict(arrowstyle="<|-|>", connectionstyle="arc3")
		self.ann_a = self.a_ax.annotate("", xy=(self.labels[0], 230), 
							xycoords='data', xytext=(self.labels[1], 230), 
							textcoords='data', arrowprops=arrow_props)
		bbox_props = dict(boxstyle="round,pad=0.3",fc="cyan",ec="b",lw=1)
		middle_co = self.labels[0] + (self.labels[1]-self.labels[0])/2
		self.ann_t = self.a_ax.text(middle_co, 240, 
							label_str, ha="center", va="bottom", 
							rotation=0, size=10, bbox=bbox_props)
		self.fig.canvas.draw()
	def add_extra_tools(self):
		# create annotation combo box on tool item
		self.lblcombo = gtk.combo_box_new_text(); 
		self.lblcombo.show()
		self.lblcombo.append_text("Sleep"); # should be loaded from file
		self.lblcombo.append_text("Breakfast")
		self.lblcombo.append_text("Lunch")
		self.lblcombo.append_text("Dinner")
		self.lblcombo.append_text("Badminton")
		self.lblcombo.set_active(0);
		# add annotation and quit buttons to the toolbar:
		toolbar = get_current_fig_manager().toolbar
		savedta_tb = gtk.ToolButton(gtk.STOCK_SAVE_AS); savedta_tb.show()
		savedta_tb.connect("clicked", self.save_data)
		sep1_tb = gtk.SeparatorToolItem(); sep1_tb.show()
		labelstr_tb = gtk.ToolItem(); labelstr_tb.show()
		labelstr_tb.add(self.lblcombo)
		label_tb = gtk.ToolButton(gtk.STOCK_INDEX); label_tb.show()
		label_tb.connect("clicked", self.mark_label)
		sep2_tb = gtk.SeparatorToolItem(); sep2_tb.show()
		exit_tb = gtk.ToolButton(gtk.STOCK_QUIT); exit_tb.show()
		exit_tb.connect("clicked", gtk.main_quit)
		try:
			savedta_tb.set_tooltip( toolbar.tooltips,'Save data')
			labelstr_tb.set_tooltip( toolbar.tooltips,'Select annotation')
			label_tb.set_tooltip( toolbar.tooltips,'Annotate')
			exit_tb.set_tooltip( toolbar.tooltips,'Close window')
		except:
			print 'Tooltips not available. Hm.'
		toolbar.insert(savedta_tb, 8)
		toolbar.insert(sep1_tb,  	9)
		toolbar.insert(labelstr_tb,10)
		toolbar.insert(label_tb, 	11)
		toolbar.insert(sep2_tb,  	12)
		toolbar.insert(exit_tb,  	13)
	def show(self):
		self.fix_margins()
		self.fig.show(); show()
		

# plots long-term raw data from the HedgeHog and suggested sleep blocks
class Hhg_nights_plot(Hhg_plot):
	def init(self):
		self.itr = 1
		self.accd = self.envd = None
	def plot(self, t, xyz, l, t_ngt, f_ngt, r_ngt, filename, num, ns=0, uid='anon0001'):
		self.init()
		self.adapt_res([t[0], t[-1]])
		self.t = t; self.xyz = xyz; self.l = l
		if ns==0: ns = len(t)
		if   numpy.shape(xyz)[1]==3: self.plot_raw_acc(); self.raw = True
		elif numpy.shape(xyz)[1]==6: self.plot_mv_acc();  self.raw = False
		self.plot_env()
		self.plot_ngt(t_ngt, f_ngt, r_ngt)
		self.draw_top_text((('dates_span: '+str(mld.num2date(t[0]))[:10]+
							 ' -> '+str(mld.num2date(t[-1]))[:10] ),
							('samples_#: ' + str(ns) ),
							('entries_#: ' + str(len(t)) ),
							('features_#: ' + str(len(t_ngt))),
							('subject_id: ' + uid) ) )
		
		prev=os.path.join(filename, 'prev_img%03d.png' % num)
		fig.savefig(prev)

	def plot_raw_acc(self, rws=2, cls=1, whr=2):
		self.a_ax = self.fig.add_subplot(rws,cls,whr)
		self.accd = self.a_ax.plot_date(	self.t[::self.itr], 
													self.xyz[::self.itr], '-',lw=.5)
	def plot_mv_acc(self, rws=2, cls=1, whr=2):
		self.a_ax = self.fig.add_subplot(rws,cls,whr)
		self.accd = self.a_ax.plot_date(self.t[::self.itr],
												self.xyz[::self.itr,:], '-', lw=0.5)
	def plot_ngt(self, t, feat_ngt, res_ngt, rws=4, cls=1, whr=1):
		self.n_ax = self.fig.add_subplot(rws,cls,whr)
		self.n_ax.plot(t,feat_ngt[:,0],'-',color='b',lw=.5,label='motion')
		self.n_ax.plot(t,feat_ngt[:,1],'-',color='g',lw=.5,label='light')
		self.n_ax.plot(t,feat_ngt[:,2],'-',color='r',lw=.5,label='time')
		self.n_ax.plot(t, res_ngt,'s', color='#000000',lw=.5)
	def plot_env(self, rws=4, cls=1, whr=2):
		self.e_ax = self.fig.add_subplot(rws,cls,whr, axisbg='#777777')
		self.envd = self.e_ax.fill_between(self.t[::self.itr], 
			     self.l[::self.itr]>>8, facecolor='yellow', lw=0, alpha=.6)
		self.e_ax.plot(self.t[::self.itr],((self.l[::self.itr]&0xFF)/2-30), 
					'-', color='r', lw=.5, label='temperature')
	def show(self):
		self.fix_margins()
		self.add_extra_tools()
		for ax in self.fig.axes:
			ax.grid(color='k', linestyle=':', linewidth=0.5)
			setp(ax.get_xticklabels(), visible=False)
			setp(ax.get_yticklabels(), visible=False)
			ax.xaxis.set_major_formatter(mld.DateFormatter('%H:%M'))
			ax.fmt_xdata = mld.DateFormatter('%Y-%m-%d, %H:%M:%S')
			ax.fmt_ydata = lambda y: '%03.03f'%y
			ax.axes.set_xlim(self.t[0],self.t[-1])
		self.a_ax.axes.set_ylim(0, 256)
		self.n_ax.axes.set_ylim(0, 420)
		self.e_ax.axes.set_ylim(0, 256)
		self.a_ax.yaxis.set_label_text('acceleration', fontsize=10)
		self.n_ax.yaxis.set_label_text('night', fontsize=10)
		self.e_ax.yaxis.set_label_text('ambient light', fontsize=10)
		setp(self.a_ax.get_xticklabels(), visible=True)
		self.a_ax.axes.callbacks.connect('xlim_changed',self.onredraw)
		self.fig.show(); show()
	def adapt_res(self, xlims):  # check if data resolution is optimal 
		tspan = xlims[1] - xlims[0]
		old_itr = self.itr
		if   tspan > 5: 	self.itr = 500	# plot spans more than 5 days:
		elif tspan > 1: 	self.itr = 100	# plot spans more than a day:
		elif tspan > .1: 	self.itr = 10 	# plot spans more than an hour:
		else:					self.itr = 1 
		if old_itr != self.itr:	# we zoomed so much we need updated data:
			if self.accd is not None:
				for i,tl in enumerate(self.accd):
					tl.set_xdata(self.t[::self.itr])
					tl.set_ydata(self.xyz[::self.itr,i])

	def onredraw(self, event): # event handler to redraw after zoom/pan
		self.n_ax.set_xlim(self.a_ax.axes.get_xlim())
		self.e_ax.set_xlim(self.a_ax.axes.get_xlim())
		self.adapt_res(self.a_ax.get_xlim()) # change res. if needed
		
		
# plots comparison of datasets
class Hhg_comp_plot(Hhg_plot):
	def plot(self, i, n, ts, dta, sumv):
		if i==0:
			self.ax1 = self.fig.add_subplot(n,1,i+1); ax = self.ax1
		else:
			ax = self.fig.add_subplot(n,1,i+1, sharex=self.ax1)
		ax.plot_date(ts, dta, '-', lw=0.5)
		ax.yaxis.set_label_text('mean', fontsize=8)
		setp(ax.get_xticklabels(), visible=False)
		setp(ax.get_yticklabels(), fontsize=8)
		ax = self.fig.add_subplot(n,1,i+2, sharex=self.ax1)
		ax.plot_date(ts, sumv,'-', color='#35A384', lw=0.5)
		ax.yaxis.set_label_text('var', fontsize=8)
		setp(ax.get_yticklabels(), fontsize=8)
		if n==i+2: # last plot?
			ax.xaxis.set_major_formatter(mld.DateFormatter('%H:%M'))
			setp(ax.get_xticklabels(), visible=True, fontsize=10)
		else:
			setp(ax.get_yticklabels(), fontsize=8)
			setp(ax.get_xticklabels(), visible=False)


# plots raw representation of datasets
class Hhg_raw_plot(Hhg_plot):
	def plot(self, i, n, ts, dta, filename, num, plot_label = '') :
		if i==1:
			self.a_ax = self.fig.add_subplot(n,1,i); ax = self.a_ax
		else:
			ax = self.fig.add_subplot(n,1,i, sharex=self.a_ax)
		ax.plot_date(ts, dta, '-', lw=0.5)
		ax.yaxis.set_label_text(plot_label, fontsize=10)
		setp(ax.get_xticklabels(), visible=False)
		setp(ax.get_yticklabels(), visible=False)
		ax.grid(color='k', linestyle=':', linewidth=0.5)
		if n==i: # last plot?
			ax.xaxis.set_major_formatter(mld.DateFormatter('%H:%M'))
			setp(ax.get_xticklabels(), visible=True, fontsize=10)
		
		
		prev=os.path.join(filename, 'prev_img%03d.png' % int(num))
		self.fig.savefig(prev)
		
	def equidist_plot(self, i, n, ts, dta, plot_label = ''):
		ax = self.fig.add_subplot(n,1,i)
		ax.plot(ts, dta, '-', lw=0.5)
		ax.yaxis.set_label_text(plot_label, fontsize=10)
		setp(ax.get_xticklabels(), visible=True, fontsize=10)
		setp(ax.get_yticklabels(), visible=False)
		setp(ax.get_yticklabels(), fontsize=8)
		ax.grid(color='k', linestyle=':', linewidth=0.5)
		ax.axes.set_xlim(0, len(dta))
	def show(self):
		self.fix_margins()
		self.add_extra_tools()
		
