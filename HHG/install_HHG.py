#!/usr/bin/env python
#
########################################################################
#
# Filename: install_HHG.py								Author: Kristof VL
#
# Descript: Install script that creates and installs the launchers 
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
 
 
 
import sys, os, stat
 
exefiles = ('plot_HHG.py', 'conf_HHG.py', 'comp_HHG.py', 
				'rawplot_HHG.py', 'install_HHG.py', 'readme1st.py')
icnfiles = ('plot_HHG.py', 'conf_HHG.py', 'comp_HHG.py', 
				'rawplot_HHG.py')
 
 
 
# create a desktop or menu launcher file in a Ubuntu distro
def create_Ublauncher(where, exefile, name, icn='gnome-panel-launcher'):
	fid = open(where,'wt')
	fid.write('[Desktop Entry]\nVersion=1.0\nType=Application\n')
	fid.write('Terminal=false\nIcon[en_US]=' +icn+ '\n')
	fid.write('Name[en_US]='+name+'\nExec=' + exefile+'\n')
	fid.write('Name='+name+'\nIcon=' +icn+ '\n')
	fid.close()
	os.chmod(where, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)

# recursively clean a directory of non-python files
def cleandir_nonpy(dname):
	for each in os.listdir(dname):
		cleanit = True
		if each == '.' or each == '..': cleanit = False
		if len(each)>3:
			if each[-3:] == '.py':
				cleanit = False
		if os.path.isdir(each):
			cleandir_nonpy(each)
			cleanit = False
		if cleanit:
			os.remove(os.path.join(dname,each))

# install and clean the HHG package
if sys.platform.startswith('linux'):
	# get variables to most basic paths:
	homedir = os.environ['HOME']
	currdir = os.getcwd()
	deskdir = os.path.join(homedir,'Desktop')
	# create shortcut launchers on the desktop:
	for f in icnfiles:
		desktop_f = os.path.join(deskdir, f[:-3]+'.desktop')
		create_Ublauncher(desktop_f, (currdir+'/'+f), f[:-3])
	# make sure all standalone script files are executable:
	fattribs = stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO
	for f in exefiles:
		os.chmod(os.path.join(currdir,f), fattribs)
	# clean up all non-python files:
	cleandir_nonpy(currdir)
			


