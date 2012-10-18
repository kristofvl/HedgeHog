/********************************************************************
 FileName:     	HardwareProfileBasicNew.h
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC
 Compiler:  	Microchip C18
 Author:        EBerlin
 ********************************************************************/

#ifndef HARDWARE_PROFILE_HEDGEHOG_BASIC_NEW_H
#define HARDWARE_PROFILE_HEDGEHOG_BASIC_NEW_H

/*******************************************************************/
/******** Board-specific definitions *******************************/
/*******************************************************************/
#define CLKFREQ_LOG 8000000
#define CLKFREQ_USB 48000000

extern char is_logging;

// used for some of the time-out counters:
#define GetInstructionClock() ((is_logging)?CLKFREQ_LOG:CLKFREQ_USB)
#define GetSystemClock() (CLKFREQ_USB)

//#define DISPLAY_ENABLED		// don't use the oled display
//#define SOFTSTART_ENABLED		// don't use the softstart circuit
#define ADXL345_ENABLED			// use the ADXL345 accelerometer
//#define BMA150_ENABLED		// don't use BMA150 accelerometer

/*******************************************************************/
/******** USB stack hardware selection options *********************/
/*******************************************************************/
// definitions required by the MCHPFSUSB framework. 
//#define USE_SELF_POWER_SENSE_IO
#define tris_self_power     TRISCbits.TRISC2    // Input
#define self_power          1
//#define USE_USB_BUS_SENSE_IO
#define tris_usb_bus_sense  TRISCbits.TRISC2    // Input
#define USB_BUS_SENSE       1 

/*******************************************************************/
/******** SPI interface definitions ********************************/
/*******************************************************************/
#define SPICLOCK            TRISCbits.TRISC2
#define SPIIN               TRISDbits.TRISD6
#define SPIOUT              TRISBbits.TRISB3
#define SPICLOCKLAT         LATCbits.LATC2	// Latch pins SCK/SDI/SDO 
#define SPIINLAT            LATDbits.LATD6
#define SPIOUTLAT           LATBbits.LATB3
#define SPICLOCKPORT        PORTCbits.RC2	// Port pins SCK/SDI/SDO 
#define SPIINPORT           PORTDbits.RD6
#define SPIOUTPORT          PORTBbits.RB3
#define SPICON1             SSP2CON1		// Registers SPI module
#define SPISTAT             SSP2STAT
#define SPIBUF              SSP2BUF
#define SPISTAT_RBF         SSP2STATbits.BF
#define SPICON1bits         SSP2CON1bits
#define SPISTATbits         SSP2STATbits
#define SPI_INTERRUPT_FLAG  PIR3bits.SSP2IF 
#define SPIENABLE           SSP2CON1bits.SSPEN

/*******************************************************************/
/******** MDD File System selection options ************************/
/*******************************************************************/
#define USE_PIC18                               // used by FSConfig.h
#define USE_SD_INTERFACE_WITH_SPI
#define SD_CS               PORTBbits.RB5       // Chip Select
#define SD_CS_TRIS          TRISBbits.TRISB5
#define SD_CD               0                   // Card Detect
#define SD_CD_TRIS          TRISAbits.TRISA3
#define SD_WE               0
#define SD_WE_TRIS          TRISAbits.TRISA3
#define SPI_INTERRUPT_FLAG_ASM PIR3, 7

/*******************************************************************/
/******** Accelerometer definitions and options ********************/
/*******************************************************************/
#define ACC_CS              LATBbits.LATB4
#define ACC_CS_TRIS         TRISBbits.TRISB4
#define ACC_INT             PORTBbits.RB2
#define ACC_INT_TRIS        TRISBbits.TRISB2

/*******************************************************************/
/******** Power Circuit sense pins definitions and options *********/
/*******************************************************************/
#define USBP_INT_TRIS       TRISDbits.TRISD4   // POK_INT_TRIS = charger "POK"
#define USBP_INT            PORTDbits.RD4      // POK_INT
#define PWRGD_INT_TRIS      TRISDbits.TRISD5   // Voltage converter "power good"
#define PWRGD_INT           PORTDbits.RD5

/*******************************************************************/
/******** Light Sensor definitions and options *********************/
/*******************************************************************/
#define LIGHTCHANNEL        6               // CHS=6 == AN6 == RE1 (PIN26)
#define LIGHT_PWR           LATEbits.LATE0  // RE0          == RE0 (PIN25)

/*******************************************************************/
/******** remap pins ***********************************************/
/*******************************************************************/
#define ul_reg() { EECON2 = 0x55; EECON2 = 0xAA; PPSCONbits.IOLOCK = 0; }
#define l_reg()  { EECON2 = 0x55; EECON2 = 0xAA; PPSCONbits.IOLOCK = 1; }

// RP6 as SDO2 (o/p), RP13 as SCK2 (o/p), RP23 as SDI2 (i/P), RP5(B2) as INT1
#define remap_pins() {ul_reg();RPOR6=9;RPOR13=10;RPINR21=23;RPINR1=5;l_reg();}

// set pins to input: B2 (acc INT) | D4 (POK) | D5 (PWRGD)
#define set_unused_pins_to_output() {TRISA=0;TRISB=0xb00000010;TRISD=0xb00010000;}
#endif  //HARDWARE_PROFILE_HEDGEHOG_BASIC_NEW_H
