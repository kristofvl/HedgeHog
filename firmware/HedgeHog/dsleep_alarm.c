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
    INTCONbits.GIE = 0;  //global interrupts disable
    Write_DSGPR(0x67, 0x7A); // save important data prior to deep sleep
    rtc_init();
    rtc_set_timeout_s(tm, seconds);

    while (RTCCFGbits.RTCSYNC != 0);
    GotoDeepSleep(DPSLP_ULPWU_DISABLE | DPSLP_RTCC_WAKEUP_ENABLE);
}

void wakeup_check(rtc_timedate *tm, int seconds)
{
    if( IsResetFromDeepSleep() ) {
        ReleaseDeepSleep();
        Reset();
    }
    else {
        set_osc_31khz();
        ANCON0 = ANCON1 = 0xFF; // Default all pins to digital
        set_unused_pins_to_output();
        // check whether USB is there:
        USBP_INT_TRIS = INPUT_PIN;
        Delay1KTCYx(2);
        if (USBP_INT != 0) { // if USB power is not present:
            goto_deep_sleep(tm, seconds);
        }
        else
            Reset();
    }
}
