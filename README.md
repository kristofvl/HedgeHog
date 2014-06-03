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

## Setup a new HedgeHog

There are four basic interactions, that you can do with your HedgeHog:

[Configure the HedgeHog](#configure-the-hedgehog)<br>
[Start logging](#start-logging)<br>
[Download the logged data](#download-the-logged-data)<br>
[Display the downloaded data](#display-the-downloaded-data)<br>

In order to be able to use the HedgeHog, you first need to setup your PC properly:

	- cd ~
	- git clone https://github.com/kristofvl/HedgeHog.git
	- cd ~/HedgeHog/HHG
	- ./install_HHG.py

This will create a few Desktop shortcuts to scripts, that will be discussed later on.

If you have a brand new HedgeHog, you will need to prepare your device, if not, just continue from section *Configure the HedgeHog*. The following instructions might also help, if there are other issues with the HedgeHog. You need to export the right image to the SD-Card. To do this, put the SD-Card into the SD-Card slot of your computer. Now you need to find out, where the SD-Card is mounted (e.g. with *dmesg*):

	- dmesg 
	- cd ~/HedgeHog/HHG/dd_img/
	- sudo dd if=dd.img of=/dev/<HedgeHog device>
	- sync

Those commands will export the correct image to the SD-Card. After exporting the image, disconnect the SD-Card and reconnect it again. If it is named *HEDGHG*, the export was succesfull and you can put your SD-Card back into the HedgeHog, if not repeat last commands.

After formatting your SD-Card with dd, insert it in your HedgeHog device. Make sure to have the newest version of the firmware, if not, flash the HedgeHog with *MPLab*. Now you are ready to configure the HedgeHog.


## Configure the HedgeHog

If you plug in the HedgeHog into the USB-Connector of your PC, it should be recognized correctly now. The install command has created a shortcut to the configuration script. Start the script now and choose the configuration you want, then click *Save Settings*. The HedgeHog will unmount, apply the settings and then mount again by itself. In the configuration script you also have the option of formating your SD-Card. By pressing format the HedgeHog will unmount, format the SD-Card and then remount again. Don't forget to configure the HedgeHog after formatting. 


## Start logging

Now that your HedgeHog has the right configuration, you are ready to start logging. Use the start script, that was also created by the installation. Choose the logging period. The default is set to one week. After pressing start the HedgeHog will disconnect automatically and start logging.  
Since firmware version 1.4000, the HedgeHog will continue logging, even if it is plugged into the USB-Connector. When plugged in, you can visualize the data, as shown in *Download the logged data* and *Display the downloaded data*. When unplugged the device will continue logging with the last configuration without deleting the existing data.

In case you dont want to start the script using the created buttons, you can also run them in a terminal. The script is in the folder *~/HedgeHog/HHG/* and is named *start_HHG.py*. To run it, go to the folder and execute

	- python start_HHG.py /media/<username>/HedgeHog<HHG-device_id>/config.URE


## Download the logged data

To download the logged data, you can use the download script. A shortcut to the script was also created during the installation. The data will be saved at 
*~/hhg_logs/<HHG_device_id>/<date>/d.npz* where <HHG-device_id> is the number you gave in the configuration and <\date> is the starting date.


## Display the downloaded data

To visualize the data, use the python script in the repository as follows:

	- cd ~/HedgeHog/HHG/
	- ./viz_HHG.py ~/hhg_logs/<HHG_device_id>/<date>/d.npz 
