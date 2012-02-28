#ifndef USBCFG_H
#define USBCFG_H

/** DEFINITIONS ****************************************************/
#define USB_EP0_BUFF_SIZE   8
#define USB_MAX_NUM_INT     1   
#define USB_MAX_EP_NUMBER   3

// Device descriptor - if these two definitions are not defined then a
// ROM USB_DEVICE_DESCRIPTOR variable by the exact name of device_dsc must exist
#define USB_USER_DEVICE_DESCRIPTOR &device_dsc
#define USB_USER_DEVICE_DESCRIPTOR_INCLUDE extern ROM USB_DEVICE_DESCRIPTOR device_dsc

//Configuration descriptors - if these two definitions do not exist then
//  a ROM BYTE *ROM variable named exactly USB_CD_Ptr[] must exist.
#define USB_USER_CONFIG_DESCRIPTOR USB_CD_Ptr
#define USB_USER_CONFIG_DESCRIPTOR_INCLUDE extern ROM BYTE *ROM USB_CD_Ptr[]

#define USB_PING_PONG_MODE USB_PING_PONG__FULL_PING_PONG

//#define USB_POLLING
#define USB_INTERRUPT

/* Parameter definitions are defined in usb_device.h */
#define USB_PULLUP_OPTION USB_PULLUP_ENABLE

#define USB_TRANSCEIVER_OPTION USB_INTERNAL_TRANSCEIVER

#define USB_SPEED_OPTION USB_FULL_SPEED

#define USB_SUPPORT_DEVICE

#define USB_NUM_STRING_DESCRIPTORS 3

#define USB_ENABLE_ALL_HANDLERS

/** DEVICE CLASS USAGE *********************************************/
#define USB_USE_MSD
#define USB_USE_CDC

/** ENDPOINTS ALLOCATION *******************************************/

/* MSD */
#define MSD_INTF_ID             0x00
#define MSD_IN_EP_SIZE          64
#define MSD_OUT_EP_SIZE         64
#define MAX_LUN 0
#define MSD_DATA_IN_EP          1
#define MSD_DATA_OUT_EP         1
#define MSD_BUFFER_ADDRESS      0x600

/* CDC */
#define CDC_COMM_INTF_ID        0x01
#define CDC_COMM_EP              2
#define CDC_COMM_IN_EP_SIZE      8

#define CDC_DATA_INTF_ID        0x01
#define CDC_DATA_EP             3
#define CDC_DATA_OUT_EP_SIZE    64
#define CDC_DATA_IN_EP_SIZE     64

#define USB_CDC_SET_LINE_CODING_HANDLER mySetLineCodingHandler
//#define USB_CDC_SUPPORT_HARDWARE_FLOW_CONTROL

//#define USB_CDC_SUPPORT_ABSTRACT_CONTROL_MANAGEMENT_CAPABILITIES_D2 //Send_Break command
#define USB_CDC_SUPPORT_ABSTRACT_CONTROL_MANAGEMENT_CAPABILITIES_D1
//Set_Line_Coding, Set_Control_Line_State, Get_Line_Coding, and Serial_State commands

/** DEFINITIONS ****************************************************/

#endif //USBCFG_H
