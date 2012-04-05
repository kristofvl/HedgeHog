/*******************************************************************************
 FileName:     	dsleep_alarm.h,   the HedgeHog's deep sleep behavior
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        TaimoorB
 ******************************************************************************/
#ifndef	DSLEEP_ALARM_H
#define	DSLEEP_ALARM_H

#include "HardwareProfile.h"
#include "dpslp.h"
#include "portb.h"
#include "RTC/rtc.h"
#include "delays.h"
#include "osc.h"

void goto_deep_sleep(rtc_timedate *tm, int seconds);
void wakeup_check(rtc_timedate *tm, int seconds);
#endif
