More information about this package can currently be found at:
 http://kristofvl.github.io/HedgeHog/ 

****************************************************************

In short, this repository contains three packages:

1. The HedgeHog firmware (operating system), requires:
    - MPLAB X (free IDE, download from Microchip.com)
    - Microchip Application Library (free library set, download 
      from Microchip.com)

2. The HedgeHog Graphical interface software, requires:
    - the basic python libraries
    - matplotlib

3. The hardware design files for the HedgeHog sensor, requires:
    - eagleCAD (free PCB design tool, download from 
      CadSoftusa.com)

****************************************************************

# User Manual

This manual will help you use your HedgeHog properly. Therefore, we will discuss the following themes

[1) Prepare your computer](#prepare-your-computer)<br>
[2) Configure the HedgeHog](#configure-the-hedgehog)<br>
[3) Start logging](#start-logging)<br>
[4) Download the logged data](#download-the-logged-data)<br>
[5) Display the downloaded data](#display-the-downloaded-data)<br>


## Prepare your computer

There is some software required on your computer in order for the graphical interface to work

* the basic python libraries (https://www.python.org/)
* matplotlib (http://matplotlib.org/)

Once this software is installed, please clone this repository by executing the command

	$ git clone https://github.com/kristofvl/HedgeHog

Now execute the installation script

	$ ./HedgeHog/HHG/install_HHG.py

This will create a few Desktop shortcuts to scripts, that will be discussed later on. Now your computer is set up for working with the HedgeHog.


## Configure the HedgeHog

If you plug in the HedgeHog into the USB-Connector of your PC, it should be recognized correctly now. The install command has created a shortcut to the configuration script. Start the script and choose the desired configuration, then click *Save Settings*. The HedgeHog will unmount, apply the settings and then mount again by itself. Do not unplug it during this process! 
In the configuration script you also have the option of formating your SD-Card. By pressing format the HedgeHog will unmount, format the SD-Card and then remount again. Don't forget to configure the HedgeHog after formatting. 

In case you dont want to start the script using the created buttons, you can also run them in a terminal. The script is in the folder *~/HedgeHog/HHG/* and is named *conf_HHG.py*. To run it, go to the folder and execute

	- python conf_HHG.py /media/<username>/HedgeHog<HHG-device_id>/config.URE


## Start logging

Now that your HedgeHog has the right configuration, you are ready to start logging. Use the start script, that was also created during the installation. You will find the shortcut on your Desktop. Choose the logging period. The default is set to one week. After pressing start, the HedgeHog will disconnect automatically and start logging. Remember to unplug it form the USB-Connector instantaneously after starting it.

Since firmware version 1.4000, the HedgeHog will continue logging as long as it has energy supply, even if it is plugged into the USB-Connector. When plugged in, the HedgeHog will interrupt the logging process and resume, as soon as it is plugged out. You can visualize the data, as shown in [4) Download the logged data](#download-the-logged-data) and [5) Display the downloaded data](#display-the-downloaded-data) when the device is attatched to your PC.

In case you dont want to start the script using the created buttons, you can also run them in a terminal. The script is in the folder *~/HedgeHog/HHG/* and is named *start_HHG.py*. To run it, go to the folder and execute

	- python start_HHG.py /media/<username>/HedgeHog<HHG-device_id>/config.URE


## Download the logged data

To download the logged data, you can use the download script. A shortcut to the script was also created during the installation. The data will be saved at 

	- ~/hhg_logs/<HHG_device_id>/<date>/d.npz 

where 'HHG-device_id' is the number you gave in the configuration and 'date' is the starting date.


## Display the downloaded data

To visualize the data, use the python script in the repository as follows:

	- cd ~/HedgeHog/HHG/
	- ./viz_HHG.py ~/hhg_logs/<HHG_device_id>/<date>/d.npz 
