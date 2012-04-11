/********************************************************************
 FileName:     	osc.h,     the HedgeHog's oscillator lib header
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#ifndef OSC__H
#define OSC__H

#include <p18f46j50.h>	// contains registers

void set_osc_31khz(void);
void set_osc_8Mhz(void);
void set_osc_48Mhz(void);
void set_osc_sleep_t1(unsigned char to);
void set_osc_sleep_int1(void);
void set_osc_deep_sleep(void);
void release_deep_sleep(void);

#endif // OSC__H