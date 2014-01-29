

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



import matplotlib, numpy, gtk
matplotlib.use('GTKAgg')
from matplotlib.pyplot import *
from matplotlib.pylab import *
import matplotlib.dates as mld
import hhg_io.hhg_import as hgi
import hhg_dialogs.hhg_fsave as fsave_dlg




## plotting routine for vizualizing stuff while loading data from HHG:
class Hhg_load_plot:
	def __init__(self, fig_x=10, fig_y=6, fdpi=80):
		self.fig = 0
		self.bw_lookup = [0.1, 5, 10, 25, 50, 100, 200, 400, 800, 1500]
		self.md_lookup = ['controller', 'sensor']			
		self.pw_lookup = ['normal', 'low-power', 'auto-sleep', 'low/auto']
		self.ax = None
		self.first_plot = 1
		try: # disable toolbar:
			rcParams['toolbar'] = 'None';		
			self.fig = figure(	num=None, figsize=(fig_x, fig_y), 
										dpi=fdpi, facecolor='w', edgecolor='k' )
			self.fig.show()
		except ValueError:
			return 0
	def fix_margins(self):
			subplots_adjust(	left  = 0.03, right = 0.98, # left, right, 
									bottom = 0.1,top = 1, # bottom and top
									wspace = 0.1, # width space betw. subplots
									hspace = 0.1  # height space btw. subplots
								)
	def plot(self, dta_t,dta_x,dta_y,dta_z, dta_e1,dta_e2, fn='',cnf=''):
		## plot data and clean up the axes: ##############################
		self.fix_margins()
		self.ax = self.fig.add_subplot(2,1,2, axisbg='#FFFFFF')
		self.linesx, = self.ax.plot_date(dta_t, dta_x, '-r', lw=0.5)
		self.linesy, = self.ax.plot_date(dta_t, dta_y, '-g', lw=0.5)
		self.linesz, = self.ax.plot_date(dta_t, dta_z, '-b', lw=0.5)
		self.axe = self.fig.add_subplot(4,1,2, axisbg='#777777')
		self.ambfill = self.axe.fill_between(dta_t, dta_e1, 
			facecolor='yellow', lw=0.1, alpha=.6, label='ambient light')
		self.ax.grid(color='k', linestyle=':', linewidth=0.5)
		self.ax.xaxis.set_major_formatter(mld.DateFormatter('%H'))
		setp(self.ax.get_xticklabels(), visible=True, fontsize=10)
		setp(self.ax.get_yticklabels(), visible=False)
		self.ax.axes.set_ylim(0, 256)
		self.ax.axes.set_xlim(int(dta_t[-1]), int(dta_t[-1])+1)
		self.axe.grid(color='w', linestyle=':', linewidth=0.5)
		self.axe.axes.set_xlim(int(dta_t[-1]), int(dta_t[-1])+1)
		setp(self.axe.get_xticklabels(), visible=False)
		self.axe.axes.set_ylim(0, 128)
		setp(self.axe.get_yticklabels(), visible=False)
		self.axe.xaxis.axis_date()
		self.ax.legend([self.linesx, self.linesy, self.linesz],
			["x acceleration", "y acceleration", "z acceleration"], 
			loc=2, prop={'size':10})
		self.rect = Rectangle((0,1),1,1,fc='y')
		self.axe.legend([self.rect], ['ambient light'],
			loc=2, prop={'size':10})
		## plot infos: ###################################################
		if cnf == '':  # dummy incase conf is empty (no configuration)
			cnf = '000?________1311____1___HedgeHog___v.1.30?___' 
		self.fig.text( 0.04, 0.96, 'Sensor unit settings', 
			ha='left', va='top', family='monospace',fontsize=11,
			bbox=dict(boxstyle='round',facecolor='grey',alpha=.4))			
		self.fig.text( 0.04, 0.927,
			'HedgeHog_ID: ' + cnf[:4] + '\nfirmware:    ' + cnf[35:42]
			+' \nlogging end: 20' +str(ord(cnf[71])) +'-'
			+str(1+ord(cnf[72])).zfill(2) +'-'+ str(ord(cnf[73])).zfill(2),
			ha='left', va='top', family='monospace', fontsize=11,
			bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4))
		## display accelerometer settings: ###############################
		g_range = pow(2,1+ord(cnf[12])-48)
		self.fig.text( 0.32, 0.96, 'accelerometer settings', 
			ha='left', va='top', family='monospace',fontsize=11,
			bbox=dict(boxstyle='round',facecolor='grey',alpha=.4))
		self.fig.text( 0.32, 0.927, 
			'acc. range : '+ u"\u00B1" + str(g_range) +'g'
			+ '\nsampled at : ' + str(self.bw_lookup[ord(cnf[13])-48])
			+ 'Hz (' + str(self.md_lookup[ord(cnf[14])-48])
			+ ')\npower mode : ' + str(self.pw_lookup[ord(cnf[15])-48])
			+ '\nRLE delta  : ' + str(cnf[20]),
			ha='left', va='top', family='monospace',fontsize=11,
			bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4))
		## display log file settings: ####################################
		self.fig.text( 0.64, 0.96, 'Log information', 
			ha='left', va='top', family='monospace',fontsize=11,
			bbox=dict(boxstyle='round',facecolor='grey',alpha=.4))
		self.t_tme = self.fig.text( 0.64, 0.927, 'log started at:  ' 
			+ str(mld.num2date(dta_t[0]))[:19]  + '\nlog stopped at:  ', 
			ha='left', va='top', family='monospace', fontsize=11, 
			bbox=dict(boxstyle='round',facecolor='yellow',alpha=.4))
		self.b = self.fig.text( 0.02, 0.03, 'statistics loading...', 
			ha='left',va='top',family='monospace',fontsize=10)
		## set window title: #############################################
		self.fig.canvas.set_window_title(
			'loading from '+fn+' on HHG#'+cnf[:4])
		ion()
		draw()
		self.fig.show()
	def update_plot(self, dta_, s=''):
		## update the timeseries plots: ##################################
		self.linesx.set_xdata(dta_.t)
		self.linesy.set_xdata(dta_.t)
		self.linesz.set_xdata(dta_.t)
		self.linesx.set_ydata(dta_.x)
		self.linesy.set_ydata(dta_.y)
		self.linesz.set_ydata(dta_.z)
		## clear and replot ambient data: ################################
		self.ambfill.remove()
		self.ambfill = self.axe.fill_between(dta_.t, dta_.e1, 
			facecolor='yellow', lw=0, alpha=.6)
		## make sure to update x axes to current day: ####################
		self.ax.axes.set_xlim(int(dta_.t[-1]), int(dta_.t[-1])+1)
		self.axe.axes.set_xlim(int(dta_.t[-1]), int(dta_.t[-1])+1)
		## update the log info ###########################################
		self.t_tme.set_text( self.t_tme.get_text()[:54]  
			+ str(mld.num2date(dta_.t[-1]))[:19])
		## update the stats info #########################################
		self.b.set_text(s)
		draw()
		##################################################################
	def save_plot(self, fn):
		self.fig.savefig(fn, format='png', dpi=50, bbox_inches='tight')







		











		
### Beyond this point, we're just listing old stuff that you *really*
### shouldn't use. Just stop scrolling. Really.



# main plotting routine for generic purposes
class Hhg_plot:
	def __init__(self, fig_x=10, fig_y=6, fdpi=80):
		self.fig = 0
		self.save_dta_file = ''
		self.labels = None
		self.a_ax = None
		self.dayborders = []
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
		self.save_dta_file,self.save_dta_type = fsave_dlg.hhg_fsave()
	def mark_day(self,tb_data):
		res = ginput(1,timeout=-1)
		self.dayborders.append(res[0][0])
		print self.dayborders
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
		self.lblcombo.append_text("Leisure")
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
		day_tb = gtk.ToolButton(gtk.STOCK_CUT);  day_tb.show()
		day_tb.connect("clicked",self.mark_day)
		sep3_tb = gtk.SeparatorToolItem(); sep3_tb.show()
		exit_tb = gtk.ToolButton(gtk.STOCK_QUIT); exit_tb.show()
		exit_tb.connect("clicked", gtk.main_quit)
		try:
			savedta_tb.set_tooltip_text( 'Save data')
			labelstr_tb.set_tooltip_text( 'Select annotation')
			label_tb.set_tooltip_text( 'Annotate')
			exit_tb.set_tooltip_text( 'Close window')
			day_tb.set_tooltip_text( 'Mark days')
		except:
			print 'Tooltips not available. Hm.'
		toolbar.insert(sep1_tb,  	8)
		toolbar.insert(labelstr_tb,9)
		toolbar.insert(label_tb, 	10)
		toolbar.insert(sep2_tb,  	11)
		toolbar.insert(day_tb,  	12)
		save_fig = toolbar.get_nth_item(13) # the save figure toolitem
		save_fig.set_icon_name(gtk.STOCK_SAVE_AS) # changes the icon 
		toolbar.insert(savedta_tb, 14)
		toolbar.insert(sep3_tb,  	15)
		toolbar.insert(exit_tb,  	16)
	def show(self):
		self.fix_margins()
		self.fig.show(); show()
		

# plots long-term raw data from the HedgeHog and suggested sleep blocks
class Hhg_nights_plot(Hhg_plot):
	def init(self):
		self.itr = 1
		self.accd = self.envd = None
	def plot(self, t, xyz, l, t_ngt, f_ngt, r_ngt, ns=0, uid='anon0001'):
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
		self.show()
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
		self.envd = self.e_ax.fill_between(self.t[::self.itr], self.l[::self.itr]>>8, facecolor='yellow', lw=0, alpha=.6)
		self.e_ax.plot(self.t[::self.itr],((self.l[::self.itr]&0xFF)/2-30), '-', color='r', lw=.5, label='temperature')
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
			#if self.envd is not None:
			#	print self.envd
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
	def plot(self, i, n, ts, dta, plot_label = '', uid='anon0001'):
		if i==1:
			self.a_ax = self.fig.add_subplot(n,1,i); ax = self.a_ax
			self.draw_top_text((('dates_span: '+str(mld.num2date(ts[0]))[:10]+
							 ' -> '+str(mld.num2date(ts[-1]))[:10] ),
							('entries_#: ' + str(len(ts)) ),
							('subject_id: ' + uid) ) )
		else:
			ax = self.fig.add_subplot(n,1,i, sharex=self.a_ax)
		ax.plot_date(ts, dta, '-', lw=0.5)
		ax.yaxis.set_label_text(plot_label, fontsize=10)
		setp(ax.get_xticklabels(), visible=False)
		setp(ax.get_yticklabels(), visible=False)
		ax.grid(color='k', linestyle=':', linewidth=0.5)
		if n==i: # last plot?
			ax.xaxis.set_major_formatter(mld.DateFormatter('%Y-%m-%d\n %H:%M:%S'))
			setp(ax.get_xticklabels(), visible=True, fontsize=10)
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
		self.fig.show(); show()
		
		

