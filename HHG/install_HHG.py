#!/usr/bin/python2.7

import sys 
import os
import subprocess

home_dir = os.environ['HOME']
curr_dir = os.getcwd()

subprocess.call(["mkdir", "-p", home_dir+"/.hhg"])
subprocess.call(["cp", "conf_HHG.py", "Conf.ui", "start_HHG.py", "Start.ui", "plot_HHG.py", "HHG", home_dir+"/.hhg"])
subprocess.call(["cp", "-r", "hhg_dialogs", "hhg_io", "hhg_features", "hhg_plot", home_dir+"/.hhg"])
