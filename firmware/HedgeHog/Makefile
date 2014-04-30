# MPLAB IDE generated this makefile for use with GNU make.
# Project: HHOS.mcp
# Date: Thu May 20 02:17:21 2010

AS = MPASMWIN.exe
CC = mcc18.exe
LD = mplink.exe
AR = mplib.exe
RM = rm

HHOS.cof : Objects/main.o Objects/usb_descriptors.o Objects/usb_function_msd.o Objects/usb_device.o Objects/usb_function_cdc.o Objects/oled.o Objects/rtcc.o Objects/BMA150.o Objects/soft_start.o Objects/osc.o Objects/SD-SPI.o Objects/emswab.o
	$(LD) /l"C:\mcc18\lib" "rm18f46j50_g.lkr" "Objects\main.o" "Objects\usb_descriptors.o" "Objects\usb_function_msd.o" "Objects\usb_device.o" "Objects\usb_function_cdc.o" "Objects\oled.o" "Objects\rtcc.o" "Objects\BMA150.o" "Objects\soft_start.o" "Objects\osc.o" "Objects\SD-SPI.o" "Objects\emswab.o" /u_CRUNTIME /z__MPLAB_BUILD=1 /m"HHOS.map" /w /o"HHOS.cof"

Objects/main.o : main.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h ../Microchip/Include/usb/usb_common.h ../Microchip/Include/usb/usb_device.h HardwareProfile\ -\ Hedgehog\ Testbed.h ../Microchip/Include/MDD\ File\ System/SD-SPI.h ../Microchip/Include/MDD\ File\ System/FSIO.h ../Microchip/Include/USB/usb_function_msd.h SD_FAT.h ../Microchip/Include/USB/usb_function_cdc.h BMA150\ driver/BMA150.h OLED\ driver/oled.h porclogo.h RTC/rtcc.h ../../../../MCC18/h/delays.h main.c USBCallbacks.c main.c ../Microchip/Include/USB/USB.h ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h usb_config.h ../../../../MCC18/h/limits.h ../Microchip/Include/usb/usb_ch9.h ../Microchip/Include/usb/usb_hal.h ../Microchip/Include/USB/usb_hal_pic18.h HardwareProfile.h FSconfig.h ../Microchip/Include/MDD\ File\ System/FSDefs.h ../Microchip/Include/USB/usb.h display_config.h osc.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "main.c" -fo=".\Objects\main.o" -DHEDGEHOG_TESTBED -mL

Objects/usb_descriptors.o : usb_descriptors.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h ../Microchip/Include/usb/usb_common.h ../Microchip/Include/usb/usb_device.h ../Microchip/Include/USB/usb_function_msd.h ../Microchip/Include/USB/usb_function_cdc.h usb_descriptors.c ../Microchip/Include/USB/usb.h ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h usb_config.h ../../../../MCC18/h/limits.h ../Microchip/Include/usb/usb_ch9.h ../Microchip/Include/usb/usb_hal.h ../Microchip/Include/USB/usb_hal_pic18.h ../Microchip/Include/MDD\ File\ System/FSDefs.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "usb_descriptors.c" -fo=".\Objects\usb_descriptors.o" -DHEDGEHOG_TESTBED -mL

Objects/usb_function_msd.o : ../Microchip/USB/MSD\ Device\ Driver/usb_function_msd.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h ../Microchip/Include/usb/usb_common.h ../Microchip/Include/usb/usb_device.h HardwareProfile\ -\ Hedgehog\ Testbed.h ../Microchip/Include/USB/usb_function_msd.h ../Microchip/Include/MDD\ File\ System/SD-SPI.h ../Microchip/USB/MSD\ Device\ Driver/usb_function_msd.c ../Microchip/Include/USB/USB.h ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h usb_config.h ../../../../MCC18/h/limits.h ../Microchip/Include/usb/usb_ch9.h ../Microchip/Include/usb/usb_hal.h ../Microchip/Include/USB/usb_hal_pic18.h HardwareProfile.h FSConfig.h ../Microchip/Include/MDD\ File\ System/FSDefs.h FSconfig.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "..\Microchip\USB\MSD Device Driver\usb_function_msd.c" -fo=".\Objects\usb_function_msd.o" -DHEDGEHOG_TESTBED -mL

Objects/usb_device.o : ../Microchip/USB/usb_device.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h ../Microchip/Include/usb/usb_common.h ../Microchip/Include/usb/usb_device.h HardwareProfile\ -\ Hedgehog\ Testbed.h ../Microchip/Include/USB/usb_function_msd.h ../Microchip/USB/usb_device.c ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h ../Microchip/Include/USB/USB.h usb_config.h ../../../../MCC18/h/limits.h ../Microchip/Include/usb/usb_ch9.h ../Microchip/Include/usb/usb_hal.h ../Microchip/Include/USB/usb_hal_pic18.h HardwareProfile.h ../Microchip/Include/MDD\ File\ System/FSDefs.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "..\Microchip\USB\usb_device.c" -fo=".\Objects\usb_device.o" -DHEDGEHOG_TESTBED -mL

Objects/usb_function_cdc.o : ../Microchip/USB/CDC\ Device\ Driver/usb_function_cdc.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h ../Microchip/Include/usb/usb_common.h ../Microchip/Include/usb/usb_device.h ../Microchip/Include/USB/usb_function_cdc.h ../Microchip/USB/CDC\ Device\ Driver/usb_function_cdc.c ../Microchip/Include/USB/usb.h ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h usb_config.h ../../../../MCC18/h/limits.h ../Microchip/Include/usb/usb_ch9.h ../Microchip/Include/usb/usb_hal.h ../Microchip/Include/USB/usb_hal_pic18.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "..\Microchip\USB\CDC Device Driver\usb_function_cdc.c" -fo=".\Objects\usb_function_cdc.o" -DHEDGEHOG_TESTBED -mL

Objects/oled.o : OLED\ driver/oled.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h OLED\ driver/oled.h OLED\ driver/oled.c ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "OLED driver\oled.c" -fo=".\Objects\oled.o" -DHEDGEHOG_TESTBED -mL

Objects/rtcc.o : RTC/rtcc.c RTC/rtcc.h RTC/rtcc.c ../../../../MCC18/h/p18f46j50.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "RTC\rtcc.c" -fo=".\Objects\rtcc.o" -DHEDGEHOG_TESTBED -mL

Objects/BMA150.o : BMA150\ driver/BMA150.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h HardwareProfile\ -\ Hedgehog\ Testbed.h BMA150\ driver/BMA150.h BMA150\ driver/BMA150.c ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h ../../../../MCC18/h/stddef.h ../Microchip/Include/GenericTypeDefs.h HardwareProfile.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "BMA150 driver\BMA150.c" -fo=".\Objects\BMA150.o" -DHEDGEHOG_TESTBED -mL

Objects/soft_start.o : Soft\ Start/soft_start.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h Soft\ Start/soft_start.c ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "Soft Start\soft_start.c" -fo=".\Objects\soft_start.o" -DHEDGEHOG_TESTBED -mL

Objects/osc.o : osc.c osc.h ../../../../MCC18/h/p18f46j50.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "osc.c" -fo=".\Objects\osc.o" -DHEDGEHOG_TESTBED -mL

Objects/SD-SPI.o : ../Microchip/MDD\ File\ System/SD-SPI.c ../../../../MCC18/h/stdio.h ../../../../MCC18/h/stdlib.h ../../../../MCC18/h/string.h HardwareProfile\ -\ Hedgehog\ Testbed.h ../Microchip/Include/MDD\ File\ System/SD-SPI.h ../Microchip/Include/MDD\ File\ System/FSIO.h ../Microchip/MDD\ File\ System/SD-SPI.c ../Microchip/Include/Compiler.h ../../../../MCC18/h/p18cxxx.h ../../../../MCC18/h/p18f46j50.h ../../../../MCC18/h/stdarg.h ../../../../MCC18/h/stddef.h ../Microchip/Include/GenericTypeDefs.h FSconfig.h HardwareProfile.h ../Microchip/Include/MDD\ File\ System/FSDefs.h FSConfig.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "C:\Documents and Settings\All Users\Documents\Microchip\MDD File System\SD-SPI.c" -fo=".\Objects\SD-SPI.o" -DHEDGEHOG_TESTBED -mL

Objects/emswab.o : emswab.c emswab.h emswab.c ../Microchip/Include/GenericTypeDefs.h ../../../../MCC18/h/stddef.h
	$(CC) -p=18F46J50 /i"..\Microchip\Include" "emswab.c" -fo=".\Objects\emswab.o" -DHEDGEHOG_TESTBED -mL

clean : 
	$(RM) "Objects\main.o" "Objects\usb_descriptors.o" "Objects\usb_function_msd.o" "Objects\usb_device.o" "Objects\usb_function_cdc.o" "Objects\oled.o" "Objects\rtcc.o" "Objects\BMA150.o" "Objects\soft_start.o" "Objects\osc.o" "Objects\SD-SPI.o" "Objects\emswab.o" "HHOS.cof" "HHOS.hex" "HHOS.map"

