#include "dsleep_alarm.h"

//Global structures used in deep sleep library
SRC ptr;
CONTEXT read_state;
rtccTimeDate RtccTimeDate ,RtccAlrmTimeDate, Rtcc_read_TimeDate ;



void RTCC_configure( )
{
	unsigned int i = 0;
	unsigned int j = 0;
	RtccInitClock();	// Turn on RTCC clock source
	for (i=0; i<4; i++) {
		for(j=0; j<4; j++)
		;
	}
	
	RtccWrOn();
	
	RtccReadTimeDate(&RtccTimeDate);
        RtccAlrmTimeDate.f.hour = RtccTimeDate.f.hour;
        RtccAlrmTimeDate.f.min = RtccTimeDate.f.min +1 ;
        RtccAlrmTimeDate.f.sec = RtccTimeDate.f.sec + 6;
        RtccAlrmTimeDate.f.mday = RtccTimeDate.f.mday;
        RtccAlrmTimeDate.f.mon = RtccTimeDate.f.mon;
        RtccAlrmTimeDate.f.year = RtccTimeDate.f.year;
        RtccWriteTimeDate(&RtccTimeDate,1); //write into registers
        RtccSetAlarmRpt(RTCC_RPT_TEN_SEC,1); //Set the alarm repeat to every 10 seconds
        RtccSetAlarmRptCount(5,1);
        RtccWriteAlrmTimeDate(&RtccAlrmTimeDate);

        mRtccOn(); //enable the rtcc
        mRtccAlrmEnable(); //enable the rtcc alarm to wake the device up from deep sleep
}


void goto_deep_sleep(void)
{
	while(1)
	{
		{
			Write_DSGPR(0x67,0x7A); //Save important data prior to deep sleep
			RTCC_configure(); //Configure RTCC as one of sources of wake up
			
			
//*************** configure deep sleep wake up sources ********************************************
			GotoDeepSleep(DPSLP_ULPWU_DISABLE | DPSLP_RTCC_WAKEUP_ENABLE);        //This function puts the device into deep sleep

		}
	}
}
