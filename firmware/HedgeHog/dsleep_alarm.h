#ifndef	DSLEEP_ALARM_H
#define	DSLEEP_ALARM_H

#if	!defined(USE_OR_MASKS)
	#define USE_OR_MASKS
#endif

#include "dpslp.h"
#include "portb.h"
#include "RTC/rtc.h"
#include "delays.h"
#include "USB/usb.h"


void goto_deep_sleep(void);
void RTCC_configure(void);
void d2s_48M(void);
void wakeup_check(void);
#endif
