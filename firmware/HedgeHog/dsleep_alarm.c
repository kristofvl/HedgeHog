/*******************************************************************************
 FileName:     	dsleep_alarm.c,   the HedgeHog's deep sleep behavior
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        TaimoorB
 ******************************************************************************/

#include "dsleep_alarm.h"

#if !defined(USBP_INT)
#error USB interrupt pin not set in HardwareProfile!
#endif

void goto_deep_sleep(rtc_timedate *tm, int seconds)
{
	INTCONbits.GIE = 0;  //global interrupts disable (to stop interference)
	rtc_init();
	rtc_set_timeout_s(tm, seconds);
	while (RTCCFGbits.RTCSYNC != 0); // make sure RTC is ready to roll
	set_osc_deep_sleep();
}


void wakeup_check(rtc_timedate *tm, int seconds)
{
	if (WDTCONbits.DS) {	// woke up from deep sleep?
		release_deep_sleep();
	}
	INTCON2bits.RBPU = 1;	// disable all port B pull-ups
	ANCON0 = ANCON1 = 0xFF;	// Default all pins to digital
	set_unused_pins_to_output();
	SPIINLAT = 1;			// SPIINLAT = LATD6 = SDO, is pulled up in hardware
	set_osc_31khz();
	Delay10TCYx(1);

	// check whether USB is there:
	if (USBP_INT != 0) {
		goto_deep_sleep(tm, seconds);	// sleep if USB power is not present
	} else
		return;							// continue if USB power present
}
