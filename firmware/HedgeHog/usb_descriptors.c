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
#include "./USB/usb_function_cdc.h"

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
    0x02,                   // Class Code
    0x00,                   // Subclass code
    0x00,                   // Protocol code
    USB_EP0_BUFF_SIZE,      // Max packet size for EP0, see usb_config.h
    0xFFF0,                 // Vendor ID
    0x0033,                 // Product ID
    0x0001,                 // Device release number in BCD format
    0x01,                   // Manufacturer string index
    0x02,                   // Product string index
    0x00,                   // Device serial number string index
    0x01                    // Number of possible configurations
};

/* Configuration 1 Descriptor */
ROM BYTE configDescriptor1[]={
// Configuration Descriptor
    9, USB_DESCRIPTOR_CONFIGURATION,                
    98, 0,          		// Total length of data for this cfg
    3,                      // Number of interfaces in this cfg
    1,                      // Index value of this configuration
    2,                      // Configuration string index
    _DEFAULT | _SELF,       // Attributes, see usb_device.h
    250,                    // Max power consumption (2X=500mA)
// Interface Descriptor: Mass Storage Device 
    9, USB_DESCRIPTOR_INTERFACE,     
    0,                      // Interface Number
    0,                      // Alternate Setting Number
    2,                      // Number of endpoints in this intf
    MSD_INTF,               // Class code
    MSD_INTF_SUBCLASS,      // Subclass code
    MSD_PROTOCOL, 		    // Protocol code
    0,                      // Interface string index
    /* Endpoint Descriptors */
    7, USB_DESCRIPTOR_ENDPOINT, _EP01_IN,  _BULK, MSD_IN_EP_SIZE, 0x00, 0x01,
    7, USB_DESCRIPTOR_ENDPOINT, _EP01_OUT, _BULK, MSD_OUT_EP_SIZE,0x00, 0x01,
// Interface Association Descriptor
	8, 0x0B, 				// Interface association descriptor 
	1, 						// The first associated interface 
	2, 						// Number of contiguous associated interface 
	COMM_INTF, 				// bInterfaceClass of the first interface 
	ABSTRACT_CONTROL_MODEL, // bInterfaceSubclass of the first interface 
	V25TER, 				// bInterfaceProtocol of the first interface 
	0, 						// Interface string index
// Interface Descriptor: Communication Control
    9, USB_DESCRIPTOR_INTERFACE,      
    1,                      // Interface Number
    0,                      // Alternate Setting Number
    1,                      // Number of endpoints in this intf
    COMM_INTF,              // Class code
    ABSTRACT_CONTROL_MODEL, // Subclass code
    V25TER,                 // Protocol code
    0,                      // Interface string index
    // CDC Class-Specific Descriptors:
    sizeof(USB_CDC_HEADER_FN_DSC),   CS_INTERFACE, DSC_FN_HEADER,   0x10, 0x01,  
    sizeof(USB_CDC_ACM_FN_DSC),      CS_INTERFACE, DSC_FN_ACM,      USB_CDC_ACM_FN_DSC_VAL,
    sizeof(USB_CDC_UNION_FN_DSC),    CS_INTERFACE, DSC_FN_UNION,    CDC_COMM_INTF_ID, 2, //CDC_DATA_INTF_ID,
    sizeof(USB_CDC_CALL_MGT_FN_DSC), CS_INTERFACE, DSC_FN_CALL_MGT, 0x00, 0x02, //CDC_DATA_INTF_ID,
	// Endpoint Descriptor
    7, USB_DESCRIPTOR_ENDPOINT, _EP02_IN, _INTERRUPT, 0x08,0x00, 0x02,
// Interface Descriptor: Communications Data
    9, USB_DESCRIPTOR_INTERFACE,  
    2,                      // Interface Number
    0,                      // Alternate Setting Number
    2,                      // Number of endpoints in this intf
    DATA_INTF,              // Class code (Communications Data)
    0,                      // Subclass code 
    V25TER, //NO_PROTOCOL,            // Protocol code
    0,                      // Interface string index
    // Bulk Endpoint Descriptors:
    7, USB_DESCRIPTOR_ENDPOINT, _EP03_OUT, _BULK, 0x40,0x00, 0x01, 
    7, USB_DESCRIPTOR_ENDPOINT, _EP03_IN,  _BULK, 0x40,0x00, 0x01,
};


//Language code string descriptor
ROM struct{BYTE bLength;BYTE bDscType;WORD string[1];}sd000={
    sizeof(sd000),USB_DESCRIPTOR_STRING,{0x0409}
};

//Manufacturer string descriptor
ROM struct{BYTE bLength;BYTE bDscType;WORD string[16];}sd001={
sizeof(sd001),USB_DESCRIPTOR_STRING,
{'E','S','S',' ','T','U','-','D','a','r','m','s','t','a','d','t'}};

//Product string descriptor
ROM struct{BYTE bLength;BYTE bDscType;WORD string[8];}sd002={
sizeof(sd002),USB_DESCRIPTOR_STRING,
{'H','e','d','g','e','H','o','g'}};

//Array of configuration descriptors
ROM BYTE *ROM USB_CD_Ptr[]=
{
    (ROM BYTE *ROM)&configDescriptor1
};

//Array of string descriptors
ROM BYTE *ROM USB_SD_Ptr[]=
{
    (ROM BYTE *ROM)&sd000,
    (ROM BYTE *ROM)&sd001,
    (ROM BYTE *ROM)&sd002
};

/** EOF usb_descriptors.c ***************************************************/

#endif
