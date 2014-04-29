/*******************************************************************************
 FileName:     	main.h,     the HedgeHog Operating System
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Authors:       KristofVL, HanyA
 ******************************************************************************/

rom char HH_NAME_STR[9] = {'H', 'e', 'd', 'g', 'e', 'H', 'o', 'g',0};
rom char HH_VER_STR[8]  = {'v', '.', '1', '.', '3', '0', '5',0};

/******************************************************************************/
char is_logging; // needs to be defined before SD-SPI.h -> GetInstructionClock

/** INCLUDES ******************************************************************/
#include "USB/usb.h"				// USB stack, USB_INTERRUPT
#include "HardwareProfile.h"		// Hardware design wrapper
#if defined(USBP_INT)
#include "dsleep_alarm.h"
#endif
#include "sensor_wrapper.h"			// all sensors 
#include "USB/usb_function_msd.h"	// Mass storage over USB
#include "SD_Buffer.h"
#include "SD_FAT.h"					// SD card FAT tables
#include "RTC/rtc.h"				// RTC functions
#include "osc.h"
#include "delays.h"


#if defined(SOFTSTART_ENABLED)
#include "./Soft Start/soft_start.h"	// controls soft start
#endif
#if defined(DISPLAY_ENABLED)
#include "display_config.h"				// OLED display defines
#endif


/** CONFIGURATION *************************************************************/
#pragma config WDTEN = OFF          //WDT disabled
#pragma config PLLDIV = 3           //Divide by 3 (12 MHz)
#pragma config STVREN = ON          //Stack over/underflow reset
#pragma config XINST = OFF          //Extended instruction set 
#pragma config CPUDIV = OSC1        //No CPU system clock divide
#pragma config CP0 = OFF            //Program not code-protected
#pragma config OSC = HSPLL          //HS oscillator, PLL, 
#pragma config FCMEN = OFF          //Fail-Safe Clock Monitor 
#pragma config IESO = OFF           //Two-Speed Start-up
#pragma config WDTPS = 32768        //1:32768
#pragma config DSWDTOSC = INTOSCREF //DSWDT clock
#pragma config RTCOSC = T1OSCREF    //RTCC clock <- 32kH crystal
#pragma config DSBOREN = OFF        //Deep Sleep Zero-Power BOR
#pragma config DSWDTEN = OFF        //Disabled
#pragma config DSWDTPS = 8192       //1:8,192 (8.5 seconds)
#pragma config IOL1WAY = OFF        //IOLOCK can be set/cleared
#pragma config MSSP7B_EN = MSK7     //7 Bit address masking
#pragma config WPFP = PAGE_1        //Write Protect Program 
#pragma config WPEND = PAGE_0       //Start protection 
#pragma config WPCFG = OFF          //Write/Erase last page 
#pragma config WPDIS = OFF          //no WPFP[5:0],WPEND,WPCFG
#pragma config T1DIG = ON           //Sec Osc clock source
#pragma config LPT1OSC = OFF        //no high power Timer1

/** VARIABLES *****************************************************************/
#pragma udata

sd_buffer_t sd_buffer;

// time variables
rtc_timedate tm;		//  holding time info for current time
char date_str[11] = "01/01/2012";
char time_str[9]  = "00:00:00";
char date_stop_str[11] = "01/01/2016";
char time_stop_str[9]  = "00:00:00";

UINT32 tm_stop;

// sensor variables:
WORD_VAL light;
UINT8 thermo = 21;
ACC_XYZ accval;			// variable for current acceleration readings
char acc_str[12];
char lt_str[4];
char tmp_str[4];
char id_str[4];

// config variables:
UINT8           rle_delta = 0;
hhg_conf_accs_t acc_settings = 0;

/** CONSTANTS *****************************************************************/
/* Standard Response to INQUIRY command stored in ROM 	*/
const ROM InquiryResponse inq_resp = {
	0x00, // peripheral device connected, direct access block
	0x80, // removable
	0x04, // version = 04 => SPC-2
	0x02, // response is in format specified by SPC-2
	0x20, // n-4 = 36-4 = 32 = 0x20
	0x00, // sccs etc.
	0x00, // other device -> using 00
	0x00, // 00 obsolete, 0x80 for basic task queueing
	{'E','S','S',' ','T','U','D','.'},
	{'M','a','s','s',' ','S','t','o','r','a','g','e',' ',' ',' ',' '},
	{'0', '0', '0', '1'}
};

/** PRIVATE PROTOTYPES ********************************************************/
#include "USBCallbacks.c"
void high_priority_ISR(void);		// interrupt service routines
void low_priority_ISR(void);
static void init_system(void);
void process_IO(void);
void update_display(void);
void user_init(void);
void log_process(void);
void config_process(void);

/** VECTOR REMAPPING **********************************************************/
#pragma code REMAPPED_HIGH_INTERRUPT_VECTOR = 0x08
void remapped_high_ISR(void) {
    _asm goto high_priority_ISR _endasm
}
#pragma code REMAPPED_LOW_INTERRUPT_VECTOR = 0x18
void remapped_low_ISR(void) {
    _asm goto low_priority_ISR _endasm
}
#pragma code	
// interrupt handling routines:
#pragma interrupt high_priority_ISR
void high_priority_ISR() {
	if (PIE1bits.TMR1IE && PIR1bits.TMR1IF) { // handle TIMER1 interrupts
		PIE1bits.TMR1IE = 0;	// turn interrupt tmr1 off
		PIR1bits.TMR1IF = 0;
		T1CONbits.TMR1ON = 0;	// turn timer 1 off
	} else
		#if defined(ADXL345_ENABLED)
		if (INTCON3bits.INT1IE && INTCON3bits.INT1IF) { // handle INT1 interrupt
			INTCON3bits.INT1IE = 0; // turn interrupt int1 off
		} else
		#endif
		{
			USBDeviceTasks();
		}
}
#pragma interruptlow low_priority_ISR

void low_priority_ISR() {
}

/** DECLARATIONS **************************************************************/
#pragma code

/*******************************************************************************
 * Function:        void main(void)
 *
 * Overview:        Main program entry point.
 ******************************************************************************/
void main(void) {
	#if defined(USBP_INT) // If we detect USB (See HardwareProfile.h)
	wakeup_check(&tm, 2); // wake up and check every 2 seconds for USB presence
	#endif
	init_system();
	USBDeviceAttach();
	while (1) {
		process_IO(); // Application tasks: logging, configuring
	}
}

/*******************************************************************************
 * Function:        static void init_system(void)
 *
 * Overview:        InitializeSystem is a centralized initialization
 *                  routine. All required USB initialization routines
 *                  and user init routines are called from here.
 ******************************************************************************/
static void init_system(void) {
	set_osc_48Mhz();

	ANCON0 = ANCON1 = 0xFF;	// Default all pins to digital
	set_unused_pins_to_output();

	//Configure interrupts:
	RCONbits.IPEN = 1;		// Enable  Interrupt Priority levels
	INTCONbits.GIEH = 1;	// Enable  High-priority Interrupts
	INTCONbits.GIEL = 0;	// Disable Low-priority Interrupts

	#if defined(USE_USB_BUS_SENSE_IO)
	tris_usb_bus_sense = INPUT_PIN;	// See HardwareProfile.h
	#endif

	#if defined(USE_SELF_POWER_SENSE_IO)
	tris_self_power = INPUT_PIN;	// See HardwareProfile.h
	#endif

	remap_pins();		// remap IO and INT pins

	USBDeviceInit();	// usb_device.c

	#if defined(DISPLAY_ENABLED)
	oled_init();
	#endif

	// wait 5,000,000 ticks till SD card is powered
	Delay10KTCYx(250);
	Delay10KTCYx(250);
	sdbuf_init();

	// Our other init routines come last
	user_init();
}

/*******************************************************************************
 * Function:        void user_init(void)
 *
 * Overview:        This routine should take care of all of the 
 *                  application's code initialization.
 ******************************************************************************/
void user_init(void) {
	// By default, start in configuration mode
	is_logging = 0;

	// wait 5,000,000 ticks till system is powered
	Delay10KTCYx(250);
	Delay10KTCYx(250);

	rtc_init();			// init clock
	acc_deep_sleep();	// put accelerometer to sleep for now
	env_init();			// set up environment sensors (light, temp, ...)

	#if defined(DISPLAY_ENABLED)
	disp_init();		// init display
	#endif

	#if defined(USBP_INT)		// If we detect USB (See HardwareProfile.h)
	rtc_set_timeout_s(&tm, 5);	//     set alarm after 5 seconds (to check USB)
	#endif
}

/*******************************************************************************
 * Function:        void ProcessIO(void)
 *
 * Overview:        This function runs all basic application tasks
 ******************************************************************************/
void process_IO(void) {
	#if defined(SOFTSTART_ENABLED)
	if (AppPowerReady() == FALSE) return; // Soft Start APP_VDD
	#endif

	#if defined(DISPLAY_ENABLED)
	update_display();	// Update routine for the display
	#endif

	if (is_logging)		// go to the logging process
		log_process();
	else {				// not logging, no USB connection present
		if ((USBDeviceState < CONFIGURED_STATE) || (USBSuspendControl == 1)) {
			#if defined(USBP_INT)
			if (!rtc_alrm()) {
				#if !defined(DISPLAY_ENABLED)	// no deepsleep for OLED -> demo
				goto_deep_sleep(&tm, 3);
				#endif
			}
			#endif
		}
		else {				// not logging and USB connection present
			MSDTasks();		// mass storage device tasks
			if (MSD_State == MSD_WAIT) {
				config_process();	// update configuration when we're not busy
			}
		}
	}
}

/*******************************************************************************
 * Function:        void update_display(void)
 *
 * Overview:        Handles screen update commands and refreshes,
 *                  using the disp_cmd, disp_mode, and disp_cycle variables
 ******************************************************************************/
void update_display(void) {
#if defined(DISPLAY_ENABLED)
	up_dispcycle();
	if (is_logging) { // in logging mode:
		if (button_pressed) { // user interaction? => switch mode:
			button_clear();
			disp_user_log_toggle();
		}
		if (disp_update_log_time()) // refresh display:
			rtc_writestr(&tm, date_str, time_str);
	} else { // in config mode:
		// user interaction? => switch mode:
		if (button_pressed) {
			button_clear();
			disp_user_conf_toggle();
		}
		// prepare to refresh display:
		if (disp_update_time()) {
			rtc_writestr(&tm, date_str, time_str);
		} else if (disp_update_env()) {
			env_read(light, thermo);
			write2str(light.Val, lt_str);
			write2str(((thermo / 2) - 30), tmp_str);
		} else if (disp_update_accl()) {
			acc_write_string(&accval, acc_str);
		} else if (disp_update_init()) {
			acc_init(sd_buffer.conf.acc_s, &(sd_buffer.conf.acc));
		}
	}
	// execute possible commands to the display update routine:
	if (disp_refresh() == DISP_CMD_ACCUP)
		disp_acc_update(&accval, acc_str);
	else if (disp_refresh() == DISP_CMD_LGTMP)
		disp_env_update((BYTE) (((light.Val > 950) ? 950 : light.Val) >> 5), lt_str, tmp_str);
	else if (disp_refresh() == DISP_CMD_CLOCK)
		disp_time_update(date_str, time_str);
	else if (disp_refresh() == DISP_CMD_INTRO)
		disp_init_intro(HH_NAME_STR, HH_VER_STR);
#endif // DISPLAY_ENABLED
}

/*******************************************************************************
 * Function:        void log_process(void)
 *
 * Overview:        Does the logging to SD card per page
 *                  no matter what type of logging, the first 8 bytes per page
 *                  are header, the other 504 are data increments
 ******************************************************************************/
void log_process() {
	static UINT8 startup = 0; // startup after a while
	if (startup == 0) { // to init light sensors, accelerometer & SD card
		startup++;
		Delay10KTCYx(250);
		set_osc_8Mhz();
		set_unused_pins_to_output();
		#if defined(USBP_INT)
		USBP_INT_TRIS = INPUT_PIN; // set USB Power interrupt pin
		#endif
		sdbuf_init();
		// initialize Sensors with settings	
		env_init();
		acc_init(acc_settings, NULL);
		#if defined(DISPLAY_ENABLED)
		disp_start_log();
		#endif
		#if defined(HEDGEHOG_OLED) || defined(HEDGEHOG_OLED_513)
		adxl345_conf_tap(0x09, 0xA0, 0x72, 0x30, 0xFF); // configure double tap
		#endif
		#if defined(USBP_INT)
		while ((USBP_INT == 0) && (startup < 128)) { // wait till usb disconnect
			set_osc_sleep_t1(255); // +-70ms timeout
			startup++;
		}
		#endif
		return;
	}
	if (sdbuf_is_onhold()) { // log time stamp and env data in first 8 bytes
		env_on(); // pull down power pin for light, do something else:
		rtc_read(&tm);
		sd_buffer.f.timestmp = rtc_2uint32(&tm);
		env_read(light, thermo); // read time stamp and light (env) value
		sd_buffer.f.envdata = ((light.Val >> 3) << 8) | (thermo);
		sdbuf_init_buffer();
		/*
		if (sd_buffer.f.timestmp > tm_stop) { // go into shutdown mode
			Reset();
		}
		 */
		return;
	}
	if (sdbuf_notfull()) {// log the main data
		#if defined(ADXL345_ENABLED)
		if (acc_settings.f.mode == '1') { // does AsDXL do sampling in buffer?
			while (((adxl345_read_byte(ADXL345_FIFO_ST)&0b00011111) > 0) ||
					(ACC_INT == 1)) { // while FIFO not empty or interrupt high:
				acc_getxyz(&accval);
				if (!sdbuf_is_new_accslot()) { // if not in fresh slot,
					if (sdbuf_check_rle(&accval, rle_delta)) // and different
						sdbuf_goto_next_accslot(); // then go to next slot
				}
				if (sdbuf_notfull())
					sdbuf_add_acc(&accval); // add/overwrite new sensor values
				if (sdbuf_deltaT_full())
					sdbuf_goto_next_accslot();
				if (sdbuf_full())
					return;
			}
			set_osc_sleep_int1(); // sleep till watermark is reached
		} else // PIC pulls for ADXL samples
		#endif // ADXL345_ENABLED
		{ // pull new accelerometer samples each 10 ms by default:
			acc_getxyz(&accval);
			if (!sdbuf_is_new_accslot()) { // if not in fresh new slot,
				if (sdbuf_check_rle(&accval, rle_delta)) // and different
					sdbuf_goto_next_accslot(); // then go to the next slot
			}
			if (sdbuf_notfull()) {
				sdbuf_add_acc(&accval);	// add/overwrite the new sensor values
				set_osc_sleep_t1(36);	// go to sleep for timeout of ~9.5ms
			}
			if (sdbuf_deltaT_full())
				sdbuf_goto_next_accslot();
		}
		#if defined(USBP_INT)
		if (USBP_INT == 0)				// if user plugged usb back in
		{
			#if defined(DISPLAY_ENABLED)
			oled_reset();
			_oledw("USB POWER DETECTED",0,3);
			Delay10KTCYx(250);
			Delay10KTCYx(250);
			#endif
			goto_deep_sleep(&tm, 1);	// go for a second in deep sleep
		}
		#endif
	}
	if (sdbuf_full()) {		// write log to page
		#if defined(DISPLAY_ENABLED)
		disp_log_subdue();	// switch off the display if it is on
		#endif
		sdbuf_write();		// write to SD card and update counters (~8.5ms)
		#if defined(DISPLAY_ENABLED)
		disp_log_revive();
		#endif
		return;				// return to IOProcess, buffer is now on_hold
	}
}

/*******************************************************************************
 * Function:        void config_process(void)
 *
 * Overview:        Setting the HedgeHog's configuration via serial
 ******************************************************************************/
void config_process(void) {
	int i;
	read_SD(SECTOR_LF, sd_buffer.bytes);	// read 512 Bytes from config.URE

	switch (sd_buffer.conf.flag) {

		case 'f':
			Delay10KTCYx(250);
			USBSoftDetach();
			Delay10KTCYx(250);

			// write 0s to sectors 0-250
			memset((void*) &sd_buffer, 0, 512);
			for (i = 0; i <= 250; i++)
				MDD_SDSPI_SectorWrite(i, sd_buffer.bytes, 1);

			// write MBR to sector 0
			memset((void*) &sd_buffer, 0, 512);
			write_MBR(&sd_buffer);
			MDD_SDSPI_SectorWrite(0, sd_buffer.bytes, 1);

			// write FAT
			memset((void*) &sd_buffer, 0, 512);
			for (i = 0; i <= 24; i++) {
				write_FAT(&sd_buffer, i);
				write_SD(i + 8, sd_buffer.bytes);
			}

			// write root table
			memset((void*) &sd_buffer, 0, 512);
			write_root_table(&sd_buffer, NULL);
			write_SD(SECTOR_RT, sd_buffer.bytes);

			// Erase SD_Buffer_Struct
			memset((void*) &sd_buffer, 0, 512);

			// reset flag
			sd_buffer.conf.flag = 0;
			write_SD(SECTOR_LF, sd_buffer.bytes);
			memset((void*) &sd_buffer, 0, 512);

			break;

		case 'c':
			Delay10KTCYx(250);
			USBSoftDetach(); // force flush on system side
			Delay10KTCYx(250);

			// updating root table to reflect ID
			memset((void*) &sd_buffer, 0, 512);
			read_SD(SECTOR_CF, sd_buffer.bytes);
			id_str[0] = sd_buffer.bytes[0];
			id_str[1] = sd_buffer.bytes[1];
			id_str[2] = sd_buffer.bytes[2];
			id_str[3] = sd_buffer.bytes[3];
			memset((void*) &sd_buffer, 0, 512);
			write_root_table(&sd_buffer, id_str);
			write_SD(SECTOR_RT, sd_buffer.bytes);

			memset((void*) &sd_buffer, 0, 512);
			read_SD(SECTOR_CF, sd_buffer.bytes);

			// write Version String to SD-Buffer
			sd_buffer.conf.ver[0] = HH_VER_STR[0];
			sd_buffer.conf.ver[1] = HH_VER_STR[1];
			sd_buffer.conf.ver[2] = HH_VER_STR[2];
			sd_buffer.conf.ver[3] = HH_VER_STR[3];
			sd_buffer.conf.ver[4] = HH_VER_STR[4];
			sd_buffer.conf.ver[5] = HH_VER_STR[5];
			sd_buffer.conf.ver[6] = HH_VER_STR[6];

			// write Name String to SD-Buffer
			sd_buffer.conf.name[0] = HH_NAME_STR[0];
			sd_buffer.conf.name[1] = HH_NAME_STR[1];
			sd_buffer.conf.name[2] = HH_NAME_STR[2];
			sd_buffer.conf.name[3] = HH_NAME_STR[3];
			sd_buffer.conf.name[4] = HH_NAME_STR[4];
			sd_buffer.conf.name[5] = HH_NAME_STR[5];
			sd_buffer.conf.name[6] = HH_NAME_STR[6];
			sd_buffer.conf.name[7] = HH_NAME_STR[7];

			write_SD(SECTOR_CF, sd_buffer.bytes);
			memset((void*) &sd_buffer, 0, 512);

			sd_buffer.conf.flag = 0;
			write_SD(SECTOR_LF, sd_buffer.bytes);
			memset((void*) &sd_buffer, 0, 512);

			break;

		case 'l':
			Delay10KTCYx(250);
			USBSoftDetach(); // force flush on system side
			Delay10KTCYx(250);
			
			memset((void*) &sd_buffer, 0, 512);
			read_SD(SECTOR_CF, sd_buffer.bytes);

			// read and set System Time from SD-Buffer
			memcpy(tm.b, (const void*) sd_buffer.conf.systime, 8 * sizeof (BYTE));
			rtc_init();
			rtc_write(&tm);
			rtc_writestr(&tm, date_str, time_str);

			// read and set Stop Time from SD-Buffer
			memcpy(tm.b, (const void*) sd_buffer.conf.stptime, 8 * sizeof (BYTE));
			tm_stop = rtc_2uint32(&tm);
			rtc_writestr(&tm, date_stop_str, time_stop_str);
			
			// initialize measurement settings
			rle_delta = sd_buffer.conf.rle_delta - 48;
			acc_settings = sd_buffer.conf.acc_s;

			// Erase SD_Buffer_Struct
			memset((void*) &sd_buffer, 0, 512);

			// start logging
			sd_buffer.conf.flag = 0;
			write_SD(SECTOR_LF, sd_buffer.bytes);
			memset((void*) &sd_buffer, 0, 512);
			
			is_logging = 1;

			break;
	}
}
/******************************************************************************/

