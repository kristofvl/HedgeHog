/********************************************************************
 FileName:     	HardwareProfileOLED.h
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog OLED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#ifndef HARDWARE_PROFILE_HEDGEHOG_OLED_513_H
#define HARDWARE_PROFILE_HEDGEHOG_OLED_513_H

/*******************************************************************/
/******** Board-specific definitions *******************************/
/*******************************************************************/
#define CLKFREQ_LOG 8000000
#define CLKFREQ_USB 48000000

extern char is_logging;

// used for some of the time-out counters:
#define GetInstructionClock() ((is_logging)?CLKFREQ_LOG:CLKFREQ_USB)
#define GetSystemClock() (CLKFREQ_USB)

#define DISPLAY_ENABLED			// use the oled display
//#define SOFTSTART_ENABLED		// don't use the softstart circuit
#define ADXL345_ENABLED			// use the ADXL345 accelerometer
//#define BMA150_ENABLED		// don't use BMA150 accelerometer

/*******************************************************************/
/******** USB stack hardware selection options *********************/
/*******************************************************************/
// definitions required by the MCHPFSUSB framework. 
//#define USE_SELF_POWER_SENSE_IO
#define tris_self_power		TRISCbits.TRISC2    // Input
#define self_power			1
//#define USE_USB_BUS_SENSE_IO
#define tris_usb_bus_sense	TRISCbits.TRISC2    // Input
#define USB_BUS_SENSE		1

/*******************************************************************/
/******** Bootloader-compatible HEX file ***************************/
/*******************************************************************/
//Uncomment this to make the output HEX of this project 
//   to be able to be bootloaded using the HID bootloader
//#define PROGRAMMABLE_WITH_USB_HID_BOOTLOADER		

/*******************************************************************/
/******** SPI interface definitions ********************************/
/*******************************************************************/
#define SPICLOCK			TRISCbits.TRISC2
#define SPIIN				TRISDbits.TRISD6
#define SPIOUT				TRISBbits.TRISB3
#define SPICLOCKLAT			LATCbits.LATC2	// Latch pins SCK/SDI/SDO
#define SPIINLAT			LATDbits.LATD6
#define SPIOUTLAT			LATBbits.LATB3
#define SPICLOCKPORT		PORTCbits.RC2	// Port pins SCK/SDI/SDO
#define SPIINPORT			PORTDbits.RD6
#define SPIOUTPORT			PORTBbits.RB3
#define SPICON1				SSP2CON1		// Registers SPI module
#define SPISTAT				SSP2STAT
#define SPIBUF				SSP2BUF
#define SPISTAT_RBF			SSP2STATbits.BF
#define SPICON1bits			SSP2CON1bits
#define SPISTATbits			SSP2STATbits
#define SPI_INTERRUPT_FLAG	PIR3bits.SSP2IF
#define SPIENABLE			SSP2CON1bits.SSPEN

/*******************************************************************/
/******** MDD File System selection options ************************/
/*******************************************************************/
#define USE_PIC18			// used by FSConfig.h
#define USE_SD_INTERFACE_WITH_SPI
#define TRIS_CARD_DETECT    TRISBbits.TRISB4    // Input
#define CARD_DETECT         PORTBbits.RB4
#define TRIS_WRITE_DETECT   TRISAbits.TRISA2    // Input
#define SD_CS               PORTCbits.RC6	// Chip Select
#define SD_CS_TRIS          TRISCbits.TRISC6
#define SD_CD               0 //PORTBbits.RB4	// Card detect
#define SD_CD_TRIS          TRISBbits.TRISB4
#define WRITE_DETECT        PORTAbits.RA2	// Write protect
#define SD_WE               PORTAbits.RA2
#define SD_WE_TRIS          TRISAbits.TRISA2
#define SPI_INTERRUPT_FLAG_ASM PIR3, 7

/*******************************************************************/
/******** OLED display selection options    ************************/
/*******************************************************************/
#define	oledWR			LATEbits.LATE1
#define	oledWR_TRIS		TRISEbits.TRISE1
#define	oledRD			LATEbits.LATE0
#define	oledRD_TRIS		TRISEbits.TRISE0
#define	oledCS			LATEbits.LATE2
#define	oledCS_TRIS		TRISEbits.TRISE2
#define	oledRESET		LATDbits.LATD1
#define	oledRESET_TRIS	TRISDbits.TRISD1
#define	oledD_C			LATBbits.LATB5
#define	oledD_C_TRIS	TRISBbits.TRISB5
// Definitions for reset pin (from oled.h)
#define RST_TRIS_BIT	TRISDbits.TRISD2
#define RST_LAT_BIT		LATDbits.LATD2

/*******************************************************************/
/******** Accelerometer definitions and options ********************/
/*******************************************************************/
#define ACC_CS			LATCbits.LATC7
#define ACC_CS_TRIS		TRISCbits.TRISC7
#define ACC_INT			PORTBbits.RB2
#define ACC_INT_TRIS	TRISBbits.TRISB2


/*******************************************************************/
/******** Power Circuit sense pins definitions and options *********/
/*******************************************************************/
#define USBP_INT_TRIS	TRISAbits.TRISA0   // POK_INT_TRIS = charger "POK"
#define USBP_INT		PORTAbits.RA0      // POK_INT
#define PWRGD_INT_TRIS	TRISAbits.TRISA1   // Voltage converter "power good"
#define PWRGD_INT		PORTAbits.RA1      // PWRGD_INT


/*******************************************************************/
/******** Light Sensor definitions and options *********************/
/*******************************************************************/
#define LIGHTCHANNEL	4						// RA5 == AN4 == CHANNEL#4
#define LIGHT_PWR		PORTAbits.RA3			// RA3 (PIN22)

/*******************************************************************/
/******** remap pins ***********************************************/
/*******************************************************************/
#define ul_reg()	{ EECON2 = 0x55;EECON2 = 0xAA;PPSCONbits.IOLOCK = 0;}
#define l_reg()		{ EECON2 = 0x55;EECON2 = 0xAA;PPSCONbits.IOLOCK = 1;}
//  RP6  as SDO2 (o/p), RP13 as SCK2 (o/p), RP23 as SDI2 (i/P),
#define remap_pins() {ul_reg(); RPOR6=9;RPOR13=10;RPINR21=23;RPINR1=5; l_reg();}

// make sure all pins are output, except for
//  A0 (POK)     - A1 (PWRGD)   - A5 (L_OUT)
//	B2 (ACC INT) - B5 (A0_OLED)
#define set_unused_pins_to_output() {TRISA=0b00100011;TRISB=0b00100100;TRISD=0;}

#endif  //HARDWARE_PROFILE_HEDGEHOG_OLED_513_H
