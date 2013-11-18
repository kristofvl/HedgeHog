/*******************************************************************
 FileName:     	usb_descriptors.c
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 *******************************************************************
 * Descriptor specific type definitions are defined in:
 * usb_device.h
 * Configuration options are defined in:
 * usb_config.h
 *******************************************************************/

#ifndef __USB_DESCRIPTORS_C
#define __USB_DESCRIPTORS_C

/** INCLUDES *******************************************************/
#include "./USB/usb.h"
#include "./USB/usb_function_msd.h"

/** CONSTANTS ******************************************************/
#if defined(__18CXX)
#pragma romdata
#endif

/* Device Descriptor */
ROM USB_DEVICE_DESCRIPTOR device_dsc=
{
    0x12,                   // Size of this descriptor in bytes
    USB_DESCRIPTOR_DEVICE,  // DEVICE descriptor type
    0x0200,                 // USB Spec Release Number in BCD format
    0x00,                   // Class Code
    0x00,                   // Subclass code
    0x00,                   // Protocol code
    USB_EP0_BUFF_SIZE,      // Max packet size for EP0, see usb_config.h
    0xFFF0,                 // Vendor ID
    0x0037,                 // Product ID
    0x0001,                 // Device release number in BCD format
    0x01,                   // Manufacturer string index
    0x02,                   // Product string index
    0x03,                   // Device serial number string index
    0x01                    // Number of possible configurations
};

/* Configuration Descriptor */
ROM BYTE configDescriptor[]={
    /* Configuration Descriptor */
    9,    // Size of this descriptor in bytes
    USB_DESCRIPTOR_CONFIGURATION,  // CONFIGURATION descriptor type
    0x20,0x00,          // Total length of data for this cfg
    1,                      // Number of interfaces in this cfg
    1,                      // Index value of this configuration
    0,                      // Configuration string index
    _DEFAULT | _SELF,               // Attributes, see usb_device.h
    50,                     // Max power consumption (2X mA)
    /* Interface Descriptor */
    9,   // Size of this descriptor in bytes
    USB_DESCRIPTOR_INTERFACE,               // INTERFACE descriptor type
    0,                      // Interface Number
    0,                      // Alternate Setting Number
    2,                      // Number of endpoints in this intf
    MSD_INTF,               // Class code
    MSD_INTF_SUBCLASS,      // Subclass code
    MSD_PROTOCOL, 		    // Protocol code
    0,                      // Interface string index

    // Endpoint Descriptors:
    7, USB_DESCRIPTOR_ENDPOINT, _EP01_IN,  _BULK, MSD_IN_EP_SIZE, 0x00, 0x01,
    7, USB_DESCRIPTOR_ENDPOINT, _EP01_OUT, _BULK, MSD_OUT_EP_SIZE,0x00, 0x01
};

//Language code string descriptor
ROM struct{BYTE bLength;BYTE bDscType;WORD string[1];}sd000={
    sizeof(sd000),USB_DESCRIPTOR_STRING,{0x0409}       // language = English
};

//Manufacturer string descriptor
ROM struct{BYTE bLength;BYTE bDscType;WORD string[16];}sd001={
sizeof(sd001),USB_DESCRIPTOR_STRING,
{'E','S','S',' ','T','U','-','D','a','r','m','s','t','a','d','t'}};

//Product string descriptor
ROM struct{BYTE bLength;BYTE bDscType;WORD string[8];}sd002={
sizeof(sd002),USB_DESCRIPTOR_STRING,
{'H','e','d','g','e','H','o','g'}};

//Serial number string descriptor.  Note: This should be unique for each unit
ROM struct{BYTE bLength;BYTE bDscType;WORD string[4];}sd003={
sizeof(sd003),USB_DESCRIPTOR_STRING,
{'0','2','3','4'}};


//Array of configuration descriptors
ROM BYTE *ROM USB_CD_Ptr[]= {  (ROM BYTE *ROM)&configDescriptor };

//Array of string descriptors
ROM BYTE *ROM USB_SD_Ptr[]=
{
    (ROM BYTE *ROM)&sd000,
    (ROM BYTE *ROM)&sd001,
    (ROM BYTE *ROM)&sd002,
    (ROM BYTE *ROM)&sd003
};

/** EOF usb_descriptors.c ***************************************************/

#endif
