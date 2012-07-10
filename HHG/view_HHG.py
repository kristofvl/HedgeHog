########################################################################
#
# Filename: view_HHG.py   								Author: Enzo Torella
#
# Descript: displays the previous images of HHG dataset
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
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
#######################################################################     



import pygtk, gtk
pygtk.require('2.0')
import os
import re
import Image
import plot_img_HHG as hplt
import wx

homedir=os.path.expanduser("~")
src=os.path.join(homedir, 'HHG')
lst = [dir for dir in (os.listdir(src)) if dir.isdigit()]
lst.sort()
			

class EventBoxExample:
	def cli(self):
		print 'click'

	def onSelectionChanged(self, widget, liststore) :
		#directory is the clicked directory
		(model, iter) = widget.get_selected()
		directory=liststore.get_value(iter, 0)
		pth=os.path.join(src, directory)
		#im is the preview image
		im = [im for im in os.listdir(pth) if im.endswith('.png')]
		
		if im == []:
			flenpy=[flenpy for flenpy in os.listdir(pth) if flenpy.endswith('.npy') and flenpy.startswith('p')]
			jj=str('\n'.join(flenpy))
					
			num=re.sub("\D", "", jj)
			#call of the function plot_HHG_image in order to create the 
			#preview image
			hplt.plot_HHG_image(pth,jj, num)
		
		hh='\n'.join(im)
		immagine = os.path.join(pth, hh)
		pixbuf = gtk.gdk.pixbuf_new_from_file(immagine)#set_from_file(immagine)
		scaled_buf=pixbuf.scale_simple(800,800,gtk.gdk.INTERP_BILINEAR)
		self.image.set_from_pixbuf(scaled_buf)
		self.image.show()
	
	def __init__(self):		
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title('Example')
		window.connect('destroy', lambda w: gtk.main_quit())
		window.set_size_request(800, 800)
		window.set_position(gtk.WIN_POS_CENTER)
		#---create a hbox----		
		hbox=gtk.HBox(False, 5)
		hbox.set_border_width(10)
		#----add hbox to window---------------
		window.add(hbox)
		
		liststore = gtk.ListStore(str)
				
		frame = gtk.Frame("Dataset")
		#create the treeview of directory containing the preview images
		for parent in lst:
			piter = liststore.append(['%s' % str(parent)])
			per=os.path.join(src, parent)
			im = [im for im in os.listdir(per) if im.endswith('png')]
			hh='\n'.join(im)
		
		treeview = gtk.TreeView(liststore)
		tvcolumn = gtk.TreeViewColumn('Column 0')
		treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 0)
		treeview.set_search_column(0)
		tvcolumn.set_sort_column_id(0)
		treeselection = treeview.get_selection()
		treeselection.set_mode(gtk.SELECTION_SINGLE)
		treeselection.connect("changed", self.onSelectionChanged, liststore)
		treeview.set_cursor(0)
		
		
		frame.add(treeview)
		
		#------add frame to vbox		
		hbox.pack_start(frame, False, False, 5)
		
		
		#------add frame to window-------------		
		window.add(frame)
		#create an other frame to display the prev images
		self.frame2 = gtk.AspectFrame("Preview", 1, 1, 1, True)#gtk.Frame("Frame")
		self.frame2.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		hbox.pack_start(self.frame2, True, False, 0)
		window.add(self.frame2)
		self.image=gtk.Image()
		self.frame2.add(self.image)
		
		#visualize always the first preview image
		fst_dir = os.path.join(src, lst[0])
		fst_im = [fst_im for fst_im in os.listdir(fst_dir) if fst_im.endswith('.png')]
		
		if fst_im == []:
			npy=[npy for npy in os.listdir(pth) if npy.endswith('.npy') and npy.startswith('p')]
			nn=str('\n'.join(npy))
			numb=re.sub("\D", "", nn)
			hplt.plot_HHG_image(fst_dir,nn, numb)
		
		hh='\n'.join(fst_im)
		immagine2 = os.path.join(fst_dir, hh)
		pixbuf = gtk.gdk.pixbuf_new_from_file(immagine2)
		scaled_buf=pixbuf.scale_simple(800,800,gtk.gdk.INTERP_BILINEAR)
		self.image.set_from_pixbuf(scaled_buf)
		self.image.show()
		#create a button quit
		button = gtk.Button("Quit")
		hbox.pack_start(button, False, False, 0)
		button.connect_object("clicked", lambda w: w.destroy(), window)
		button.show()
		
		window.show_all()
		
	


def main():
	gtk.main()
	return 0
	
if __name__ == '__main__':
	EventBoxExample()
	main()
