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

In order to perform this actions, you first need to setup your PC properly.

	- Clone this repository
	- Execute the command ./install_HHG.py in ~/HedgeHog/HHG

This will create a few Desktop shortcuts to scripts, that will be discussed later on.

If you have a brand new HedgeHog, you will need to do some extra adjustments, if not, then just continue at *Configure the HedgeHog*. The following instructions might also help, if there are other issues with the HedgeHog. You need to put the right image on the SD-Card. To do this, put the SD-Card in the SD-Card slot in yout PC. You need to find out, where the SD-Card is mounted (e.g. with *dmesg*). In this example, it is assumed, the SD-Card is mounted at /dev/sdc. Go to the folder *~/HedgeHog/HHG/dd_img/* and execute the commands

	- sudo dd if=dd.img of=/dev/sdc
	- sync

This will export the correct image to the SD-Card. After exporting the image, disconnect the SD-Card and reconnect it again. If it is named *HEDGHG*, the export was succesfull. Now put your SD-Card into your HedgeHog.

Now you need to flash the HedgeHog with *MPLab*. Make sure to choose the correct hardware profile.


## Configure the HedgeHog

If you plug in the HedgeHog into the USB-Connector of your PC, it should be recognized correctly now. The install command has created a shortcut to the configuration script. Start the script now and choose the configuration you want, then click *configure*. The HedgeHog will unmount and then mount again by itself. As soon as the HedgeHog is mounted again, the configuration is applied.


## Start logging

When the HedgeHog has the right configuration, it is ready to be started. Therefore use the start script, that also was created by the install command. The HedgeHog will be started and will log data, that are stored at the SD-Card. 
Since firmware version 1.4000, the HedgeHog will continue logging, even if it is plugged into the USB-Connector. When plugged in, you can visualize the data, as shown in *Download the logged data* and *Display the downloaded data*. When the HedgeHog is unpluged again, it will continue logging data.


## Download the logged data

To download the logged data, you can use the download script. A shortcut to the script was also created during the installation progress. The data will be saved at 
*~/hhg_logs/HHG_device_number/date/d.npz* where *HHG-device_number* is the number entered in the config file and *date* is the starting date


## Display the downloaded data

To visualize the data, a python script is contained in the repository. To use it, got to *~/HedgeHog/HHG* and execute

	- ./viz_HHG.py ~/hhg_logs/HHG_device_number/date/d.npz 
	- HHG-device_number is the number entered in the config file
	- date is the starting date