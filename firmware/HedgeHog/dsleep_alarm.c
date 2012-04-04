/*******************************************************************************
 FileName:     	dsleep_alarm.c,   the HedgeHog's deep sleep behavior
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        TaimoorB
 ******************************************************************************/

#include "dsleep_alarm.h"

//Global structures used in deep sleep library
SRC ptr;
CONTEXT read_state;
rtccTimeDate RtccTimeDate ,RtccAlrmTimeDate, Rtcc_read_TimeDate ;

void RTCC_configure( )
{
	/*unsigned int i = 0;
	unsigned int j = 0;

        RtccInitClock();	// turn on RTCC clock source
	for (i=0; i<4; i++)
		for(j=0; j<60000; j++);
	
        RtccWrOn();
        RtccTimeDate.f.hour = 0;
        RtccTimeDate.f.min = 0;
        RtccTimeDate.f.sec = 0;
        RtccTimeDate.f.mday = 1;
        RtccTimeDate.f.mon = 1;
        RtccTimeDate.f.year = 1;
        
        RtccAlrmTimeDate.f.hour = 0;
        RtccAlrmTimeDate.f.min = 0;
        RtccAlrmTimeDate.f.sec = 9;
        RtccAlrmTimeDate.f.mday = 1;
        RtccAlrmTimeDate.f.mon = 1;
        RtccAlrmTimeDate.f.year = 1;

        RtccWriteTimeDate(&RtccTimeDate,1);
        RtccSetAlarmRpt(RTCC_RPT_TEN_SEC,1); // set the alarm repeat every 10s
        RtccSetAlarmRptCount(1,1);
        RtccWriteAlrmTimeDate(&RtccAlrmTimeDate);
        mRtccOn(); // enable the rtcc
        mRtccAlrmEnable(); // enable the rtcc alarm to wake up from deep sleep
        */

        rtc_read(&RtccTimeDate);
        RtccAlrmTimeDate.f.mon  = RtccTimeDate.f.mon;
        RtccAlrmTimeDate.f.mday = RtccTimeDate.f.mday;
        RtccAlrmTimeDate.f.wday  = RtccTimeDate.f.mon;
        RtccAlrmTimeDate.f.hour = RtccTimeDate.f.hour;
        RtccAlrmTimeDate.f.min  = RtccTimeDate.f.min;
        RtccAlrmTimeDate.f.sec = RtccTimeDate.f.sec+9;

        rtc_write_alarm(&RtccAlrmTimeDate);
        mRtccOn();
        mRtccAlrmEnable();
}

void goto_deep_sleep(void) {
    char config = 0;
    while (1) {
        INTCONbits.GIE = 0;  //global interrupts disable
        Write_DSGPR(0x67, 0x7A); // save important data prior to deep sleep
        RTCC_configure(); // configure RTCC as one of sources of wake up
        //*************** configure deep sleep wake up sources ************
        config = DPSLP_ULPWU_DISABLE | DPSLP_RTCC_WAKEUP_ENABLE;
        if (RTCCFGbits.RTCSYNC == 0)
            GotoDeepSleep(config);
    }
}

void d2s_48M(void)
{
    char i=40;
    while (i--)
        Delay10KTCYx(0);
}

void wakeup_check(void)
{
    if( IsResetFromDeepSleep() == TRUE )
    {
        ReadDSGPR(&read_state);
        DeepSleepWakeUpSource(&ptr);
        ReleaseDeepSleep();
        Reset();
    }
}