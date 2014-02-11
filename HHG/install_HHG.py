#!/usr/bin/env python2.7

import sys 
import os, stat
import subprocess

home_dir = os.environ['HOME']
cur_dir = os.getcwd()
dsk_dir = os.path.join(home_dir, 'Desktop')

strt_f = os.path.join(dsk_dir,'hhgstart.desktop')
conf_f = os.path.join(dsk_dir,'hhgconf.desktop')
down_f = os.path.join(dsk_dir,'hhgdownload.desktop')

with open (strt_f,"w") as f:
	f.write("[Desktop Entry]\nName=Start HedgeHog\n")
	f.write("Comment=Start Logging\n")
	f.write('Exec='+os.path.join(cur_dir,'start_HHG.py') )
	f.write("\nTerminal=false\nType=Application\n")
	f.write("Icon=utilities-system-monitor-symbolic\nPath=")
	f.write(cur_dir+"\nStartupNotify=false\n")
	f.close()
with open (conf_f,"w") as f:
	f.write("[Desktop Entry]\nName=Configure HedgeHog\n")
	f.write("Comment=Set up a HedgeHog\n")
	f.write('Exec='+os.path.join(cur_dir,'conf_HHG.py') )
	f.write("\nTerminal=false\nType=Application\n")
	f.write("Icon=gnome-disks\nPath="+cur_dir+"\nStartupNotify=false\n")
	f.close()
with open (down_f,"w") as f:
	f.write("[Desktop Entry]\nName=Download from HedgeHog\n")
	f.write("Comment=Download a HedgeHog log\n")
	f.write('Exec='+os.path.join(cur_dir,'download_HHG.py') )
	f.write("\nTerminal=false\nType=Application\n")
	f.write("Icon=preferences-system-network-symbolic\nPath=")
	f.write(cur_dir+"\nStartupNotify=false\n")
	f.close()
os.chmod(strt_f, stat.S_IWUSR | stat.S_IRUSR |stat.S_IXUSR )
os.chmod(conf_f, stat.S_IWUSR | stat.S_IRUSR |stat.S_IXUSR )
os.chmod(down_f, stat.S_IWUSR | stat.S_IRUSR |stat.S_IXUSR )

subprocess.call(["mkdir", "-p", home_dir+"/.hhg"])
subprocess.call(["ln", "-sf", "conf_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "start_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "import_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "plot_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "viz_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "dd_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "dmesg_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "download_HHG.py",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "conf.ui",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", "start.ui",home_dir+"/.hhg"]);

subprocess.call(["ln", "-sf", cur_dir+"/hhg_dialogs",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", cur_dir+"/hhg_features",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", cur_dir+"/hhg_plot",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", cur_dir+"/hhg_io",home_dir+"/.hhg"]);
subprocess.call(["ln", "-sf", cur_dir+"/dd_img",home_dir+"/.hhg"]);
