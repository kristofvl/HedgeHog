#!/usr/bin/env python
#
########################################################################
#
# Filename: conf_hhg.py									Author: Kristof VL
#
# Descript: Configure the HedgeHog module via serial 
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
 




import hhg_comms.hhg_comms as hcs
import gtk
import pango							# for tweaking the conf window font
import datetime


# the main configuration dialog window
class conf_HHG_dialog:

	def select(self, widget, data=None):
		hhgfinder = hcs.HHG_find()
		hhglist = hhgfinder.list()
		if not hhglist:
			md = gtk.MessageDialog(self.window, 
					gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
					gtk.BUTTONS_CLOSE, "No HedgeHog units found")
			md.run()
			md.destroy()
			return False 
		dlg = gtk.Dialog('HHG port select', self.window, 
								gtk.DIALOG_DESTROY_WITH_PARENT)
		dlg.set_size_request(450, 150)
		dlglbl = gtk.Label('Select one of the HedgeHog ports below:')
		dlglbl.set_line_wrap(True)
		dlglbl.set_justify(gtk.JUSTIFY_LEFT)
		dlglbl.show()
		dlg.vbox.add(dlglbl)
		for i in range(len(hhglist)):
			dlg.add_button(hhglist[i],i+1)
		i = dlg.run()
		dlg.destroy()
		self.connected = True
		self.portname = hhglist[i-1]
		self.portstr.set_text(self.portname)
		self.currentHHG = hcs.HHG_comms(self.portname)
		self.currentHHG.connect()
		ret = self.currentHHG.init_HHG(0, 18)
		if len(ret) == 18:
			self.initstr.set_text(ret[6:14])
		print "init:", ret, len(ret)
		ret = self.currentHHG.read_data(0,65)
		print "data:", ret, len(ret)
		if len(ret) == 65:
			self.datastr.set_text(ret[:35])
			self.timestr.set_text(ret[40:59])
		ret = self.currentHHG.get_version(0,16)
		print "ver:", ret, len(ret)
		if len(ret) == 16:
			self.versionstr.set_text(ret[:16])
		self.currentHHG.disconnect()
				
	def syncHHG(self, widget, data=None):
		if not self.connected:
			self.select(None)
		if self.connected:
			progressbar = 1
			if progressbar:
				pgrsdlg = gtk.Dialog("Syncing...", None, 0, None)
				pbar = gtk.ProgressBar()
				pgrsdlg.vbox.add(pbar)
				pbar.set_fraction(0.05)
				pbar.show()
				pgrsdlg.vbox.show()
				pgrsdlg.show()
				while gtk.events_pending(): gtk.main_iteration()
			self.currentHHG = hcs.HHG_comms(self.portname)
			self.currentHHG.connect(0.5)
			ret = self.currentHHG.init_HHG(0, 18)
			print "init:", ret, len(ret)
			if len(ret) == 18:
				self.initstr.set_text(ret[6:14])
			if progressbar:
				pbar.set_fraction(0.1)
				while gtk.events_pending(): gtk.main_iteration()
			ret = self.currentHHG.synchronize_clock(0.1, 3)
			print "set clock:", ret, len(ret)
			if progressbar:
				pbar.set_fraction(0.3)
				while gtk.events_pending(): gtk.main_iteration()
			ret = self.currentHHG.read_data(0, 65)
			print "data:", ret, len(ret)
			if len(ret) == 65:
				self.datastr.set_text(ret[:35])
				self.timestr.set_text(ret[40:59])
			ret = self.currentHHG.get_version(0, 16)
			if len(ret) == 16:
				self.versionstr.set_text(ret[:16])
			print "ver:", ret, len(ret)
			if progressbar:
				pbar.set_fraction(0.8)
				while gtk.events_pending(): gtk.main_iteration()
			ret = self.currentHHG.get_HHGID(0, 21)
			print "conf IO:", ret[:4], len(ret)
			if len(ret) > 19:
				self.idstr.set_text(ret[:20])
			if progressbar:
				pgrsdlg.hide()
				pgrsdlg.destroy()
				while gtk.events_pending(): gtk.main_iteration()
			self.currentHHG.disconnect()

	def record(self, widget, data=None):
		if not self.connected:
			self.select(None)
		if self.connected:
			### time set dialog ###########################################
			dlg =  gtk.MessageDialog( None, 
						gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK, None)
			dlg.set_size_request(450, 360)
			dlg.set_markup("Enter below the time to <b>stop</b> logging\n"+
			"<i>(by default, the HedgeHog stops logging after a week)</i>")
			entry_date = gtk.Calendar()
			now_date = datetime.datetime.now()
			rec_date = now_date + datetime.timedelta(days=7)
			entry_date.select_month(rec_date.month-1, rec_date.year)
			entry_date.select_day(rec_date.day)
			if rec_date.month == now_date.month:
				entry_date.mark_day(now_date.day)
			entry_date.set_display_options( gtk.CALENDAR_SHOW_HEADING |
				gtk.CALENDAR_SHOW_DAY_NAMES | gtk.CALENDAR_SHOW_WEEK_NUMBERS
				| gtk.CALENDAR_WEEK_START_MONDAY );
			entry_hour = gtk.combo_box_new_text()
			for i in range(0,24): 
				entry_hour.append_text( str(i).zfill(2) )
			entry_hour.set_active(rec_date.hour)
			entry_mins = gtk.combo_box_new_text()
			for i in range(0,60,5):
				entry_mins.append_text( str(i).zfill(2) )
			entry_mins.set_active(rec_date.minute/5)
			box1 = gtk.VBox(homogeneous=False, spacing=1)
			box1_text = gtk.Label("Date:");   ###### TODO: left-justify
			box1_text.set_justify(gtk.JUSTIFY_LEFT)  ### doesn't work
			box1.pack_start(box1_text, False, False, 1)
			box1.pack_start(entry_date, True, True, 2)
			box2 = gtk.HBox(homogeneous=False, spacing=1)
			box2.pack_start(gtk.Label("Time:"), False, False, 2)
			box2.pack_start(entry_hour, False, False, 2)
			box2.pack_start(gtk.Label(":"), False, False, 2)
			box2.pack_start(entry_mins, False, False, 2)
			dlg.vbox.pack_end(box2, True, False, 0)
			dlg.vbox.pack_end(box1, True, True, 0)
			dlg.show_all()
			dlg.run()
			rd = entry_date.get_date(); 
			rt = (entry_hour.get_active(), entry_mins.get_active())
			rec_date = rec_date.replace(rd[0],rd[1],rd[2], rt[0], rt[1]*5)
			dlg.destroy()
			print rec_date
			#### serial comms #############################################
			self.currentHHG = hcs.HHG_comms(self.portname)
			self.currentHHG.connect()
			ret = self.currentHHG.set_timeout_clock(rec_date, 0.1, 3)
			print "set timeout:", ret, len(ret)
			ret = self.currentHHG.synchronize_clock(0.1, 3)
			print "set clock:", ret, len(ret)
			ret = self.currentHHG.record_HHG()
			print ret
			self.currentHHG.disconnect()
			self.connected = False
			dlg= gtk.MessageDialog(self.window, 
					gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
					gtk.BUTTONS_CLOSE, "Your HedgeHog is now recording")
			dlg.set_size_request(320, 80)
			dlg.run()
			dlg.destroy()
        
	def refat(self, widget, data=None):
		if not self.connected:
			self.select(None)
		if self.connected:
			progressbar = 1
			if progressbar:
				pgrsdlg = gtk.Dialog("Formatting...", None, 0, None)
				pbar = gtk.ProgressBar()
				pgrsdlg.vbox.add(pbar)
				pbar.set_fraction(0.05)
				pbar.show()
				pgrsdlg.vbox.show()
				pgrsdlg.show()
				while gtk.events_pending(): gtk.main_iteration()
			self.currentHHG = hcs.HHG_comms(self.portname)
			self.currentHHG.connect(0.5)
			ret = self.currentHHG.set_FAT(0.1, 3)
			print "FAT IO:", ret, len(ret)
			if progressbar:
				pgrsdlg.hide()
				pgrsdlg.destroy()
				while gtk.events_pending(): gtk.main_iteration()
			self.currentHHG.disconnect()

	def conf(self, widget, data=None):
		if not self.connected:
			self.select(None)
		if self.connected:
			dlg =  gtk.MessageDialog( None, 
						gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
						gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK, None)
			dlg.set_size_request(450, 250)
			dlg.set_markup('Enter below the HedgeHog configuration:')
			entry_id = gtk.Entry()
			entry_range = gtk.combo_box_new_text()
			entry_range.append_text("-2 to +2 g")
			entry_range.append_text("-4 to +4 g")
			entry_range.append_text("-8 to +8 g")
			entry_range.append_text("-16 to +16 g")
			entry_range.set_active(1)
			entry_bw = gtk.combo_box_new_text()
			entry_bw.append_text("0.1Hz")
			entry_bw.append_text("5Hz")
			entry_bw.append_text("10Hz")
			entry_bw.append_text("25Hz")
			entry_bw.append_text("50Hz")
			entry_bw.append_text("100Hz")
			entry_bw.append_text("0.2kHz")
			entry_bw.append_text("0.4kHz")
			entry_bw.append_text("0.8kHz")
			entry_bw.append_text("1.5kHz")
			entry_bw.set_active(5)
			hbox1 = gtk.HBox()
			hbox1.pack_start(gtk.Label("Name:"), False, False, 1)
			hbox1.pack_end(entry_id)
			hbox2 = gtk.HBox()
			hbox2.pack_start(gtk.Label("Acc range:"), False, False, 1)
			hbox2.pack_end(entry_range)
			hbox3 = gtk.HBox()
			hbox3.pack_start(gtk.Label("Acc bandwidth:"), False, False, 1)
			hbox3.pack_end(entry_bw)
			dlg.vbox.pack_end(hbox3, True, True, 0)
			dlg.vbox.pack_end(hbox2, True, True, 0)
			dlg.vbox.pack_end(hbox1, True, True, 0)
			dlg.show_all()
			dlg.run()
			id_text = entry_id.get_text()
			if len(id_text)!=4:
				id_text.zfill(4) # pad with zeros for a valid entry
				print id_text
			range_sel = entry_range.get_active()
			if range_sel > -1:
				acc_text = str(range_sel)
			else:
				acc_text = "-"
			range_sel = entry_bw.get_active()
			if range_sel > -1:
				acc_text += str(range_sel)
			else:
				acc_text += "-"
			acc_text += "--"
			dlg.destroy()
			self.currentHHG = hcs.HHG_comms(self.portname)
			self.currentHHG.connect()
			ret = self.currentHHG.set_HHGID(id_text, acc_text, 0.05, 3)
			print "set conf:", ret, len(ret)
			self.currentHHG.disconnect()

	def leave(self, widget, data=None):
		return False
        
	def delete_event(self, widget, event, data=None):
		return False

	def destroy(self, widget, data=None):
		self.connected = False
		gtk.main_quit()
		return True
			
	def update_conf(self):
		return True

	def __init__(self):
		self.currentHHG = 0		# id for current HedgeHog
		self.connected = False	# are we connected?
		self.portname = ''		# what port?
		# GUI construction:
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(500, 250)
		self.window.connect('delete_event', self.delete_event)
		self.window.connect('destroy', self.destroy)
		self.window.set_border_width(4)
		self.window.set_title('HHG control interface')
		self.vbox = gtk.VBox()
		##################################################################
		bas_f = gtk.Frame("main functions")
		vbox_bas = gtk.VBox()
		bas_f.add(vbox_bas)
		self.selt_button = gtk.Button('select HedgeHog')
		self.selt_button.connect('clicked', self.select, None)
		vbox_bas.add(self.selt_button)
		self.recd_button = gtk.Button('start recording')
		self.recd_button.connect("clicked", self.record, None)
		vbox_bas.add(self.recd_button)
		self.quit_button = gtk.Button("exit")
		self.quit_button.connect("clicked", self.leave, None)
		self.quit_button.connect_object("clicked", 
											gtk.Widget.destroy, self.window)
		vbox_bas.add(self.quit_button)
		self.vbox.pack_start(bas_f, True, True, 0)
		##################################################################
		adv_f = gtk.Frame("advanced")
		vbox_adv = gtk.VBox()
		adv_f.add(vbox_adv)
		tb = gtk.Table(2,5, False); vbox_adv.add(tb)
		tb.attach(gtk.Label(' version:'), 0, 1, 0, 1)
		self.versionstr = gtk.Label('HedgeHog vX.XXX')
		tb.attach(self.versionstr, 1, 2, 0, 1)
		tb.attach(gtk.Label(' device configuration:'), 0, 1, 1, 2)
		self.idstr = gtk.Label('XXXX')
		tb.attach(self.idstr, 1, 2, 1, 2)
		tb.attach(gtk.Label(' hhg time:'), 0, 1, 2, 3)
		self.timestr = gtk.Label('XX/XX/XXXX XX:XX:XX')
		tb.attach(self.timestr, 1, 2, 2, 3)			
		tb.attach(gtk.Label(' port:'), 0, 1, 3, 4)
		self.portstr = gtk.Label('/dev/ttyAXXXX')
		tb.attach(self.portstr, 1, 2, 3, 4)
		tb.attach(gtk.Label(' init reply:'), 0, 1, 4, 5)
		self.initstr = gtk.Label('init: XX XX XX')
		tb.attach(self.initstr, 1, 2, 4, 5)
		tb.attach(gtk.Label(' last data:'), 0, 1, 5, 6)
		self.datastr = gtk.Label('acc[XXX XXX XXX] lgt[XXX] tmp[XXX]')
		tb.attach(self.datastr, 1, 2, 5, 6)
		for l in tb:	
			l.set_alignment(0, 0.5)
			l.modify_font(pango.FontDescription("courier 10"))
		hbox_adv = gtk.HBox()
		self.rfat_button = gtk.Button('quick-format SD card')
		self.rfat_button.connect("clicked", self.refat, None)
		hbox_adv.add(self.rfat_button)
		self.sync_button = gtk.Button('synchronize HedgeHog')
		self.sync_button.connect('clicked', self.syncHHG, None)
		hbox_adv.add(self.sync_button)
		self.conf_button = gtk.Button('configure HedgeHog')
		self.conf_button.connect("clicked", self.conf, None)
		hbox_adv.add(self.conf_button)
		vbox_adv.add(hbox_adv)
		self.vbox.pack_start(adv_f, False, True, 0)	
		##################################################################
		self.window.add(self.vbox)
		self.window.show_all()

	def main(self):
		gtk.main()

# If program is ran directly or passed as an argument to python:
if __name__ == "__main__":
    conf_hhg = conf_HHG_dialog()
    conf_hhg.main()
	
