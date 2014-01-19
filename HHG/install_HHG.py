#!/usr/bin/env python2.7

import sys 
import os
import subprocess

homeDir = os.environ['HOME']
currDir = os.getcwd()

subprocess.call(["mkdir", "-p", homeDir+"/.hhg"])
subprocess.call(["ln", "-sf", "conf_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "start_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "import_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "plot_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "viz_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "dd_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "dmesg_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "download_HHG.py",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "Conf.ui",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", "Start.ui",homeDir+"/.hhg"]);

subprocess.call(["ln", "-sf", currDir+"/hhg_dialogs",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", currDir+"/hhg_features",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", currDir+"/hhg_plot",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", currDir+"/hhg_io",homeDir+"/.hhg"]);
subprocess.call(["ln", "-sf", currDir+"/dd_img",homeDir+"/.hhg"]);
