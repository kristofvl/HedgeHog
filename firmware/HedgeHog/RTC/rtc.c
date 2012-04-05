/*******************************************************************************
 FileName:     	rtc.c
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#include "rtc.h"

void RTCLock(char Lock);
unsigned char mBcd2Dec(BYTE bcd);
unsigned char mDec2Bcd(BYTE dec);


void rtc_init(void) {
    T1CONbits.T1OSCEN = 1; // enable Timer1 Osc
    mRtcc_Clear_Intr_Status_Bit;
    RTCLock(1);
    mRtccOn();
    RTCLock(0);
}

void rtc_read(rtc_timedate *tm) {
    RTCCFG |= 0x03; // set RTCPTR bits to 11
    tm->f.year = mBcd2Dec(RTCVALL); //RTCPTR = 11
    tm->f.rsvd = RTCVALH; //RTCPTR = 11
    tm->f.mday = mBcd2Dec(RTCVALL); //RTCPTR = 10
    tm->f.mon = mBcd2Dec(RTCVALH); //RTCPTR = 10
    tm->f.hour = mBcd2Dec(RTCVALL); //RTCPTR = 01
    tm->f.wday = RTCVALH; //RTCPTR = 01
    tm->f.sec = mBcd2Dec(RTCVALL); //RTCPTR = 00
    tm->f.min = mBcd2Dec(RTCVALH); //RTCPTR = 00
}

void rtc_write(rtc_timedate *tm) {
    RTCLock(1);
    RTCCFG |= 0x03; // set RTCPTR bits to 11
    RTCVALL = mDec2Bcd(tm->f.year); //RTCPTR = 11
    RTCVALH = tm->f.rsvd; //RTCPTR = 11
    RTCVALL = mDec2Bcd(tm->f.mday); //RTCPTR = 10
    RTCVALH = mDec2Bcd(tm->f.mon); //RTCPTR = 10
    RTCVALL = mDec2Bcd(tm->f.hour); //RTCPTR = 01
    RTCVALH = tm->f.wday; //RTCPTR = 01
    RTCVALL = mDec2Bcd(tm->f.sec); //RTCPTR = 00
    RTCVALH = mDec2Bcd(tm->f.min); //RTCPTR = 00
    RTCLock(0);
}

void rtc_write_alarm(rtc_timedate *tm) {
    RTCLock(1);
    while (RTCCFGbits.RTCSYNC!=0); // wait till 0
    ALRMRPT = 0;
    while (RTCCFGbits.RTCSYNC!=0); // wait till 0
    ALRMCFG = 0b00000000;
    ALRMCFG |= (RTCC_RPT_YEAR<<2);
    ALRMCFG |= 0x02; // set RTCPTR bits to 10
    ALRMVALL = mDec2Bcd(tm->f.mday); //RTCPTR = 10
    ALRMVALH = mDec2Bcd(tm->f.mon); //RTCPTR = 10
    ALRMVALL = mDec2Bcd(tm->f.hour); //RTCPTR = 01
    ALRMVALH = tm->f.wday; //RTCPTR = 01
    ALRMVALL = mDec2Bcd(tm->f.sec); //RTCPTR = 00
    ALRMVALH = mDec2Bcd(tm->f.min); //RTCPTR = 00
    RTCLock(0);
}

void rtc_set_timeout_s(rtc_timedate *tm, int seconds)
{
    tm->f.year = 1; tm->f.mon  = 1; tm->f.mday = 1; tm->f.wday = 1;
    tm->f.hour = 1; tm->f.min  = 1; tm->f.sec  = 0;
    rtc_write(tm);

    tm->f.sec   = seconds;
    rtc_write_alarm(tm);

    mRtccOn();
    mRtccAlrmEnable();
}

BYTE rtc_get_sec(void) {
    RTCCFG |= 0x00; // set RTCPTR bits to 00
    return mBcd2Dec(RTCVALL); //RTCPTR = 00
}

void rtc_writestr(rtc_timedate *tm, char* date_buff, char* time_buff) {
    rtc_read(tm);
    time_buff[0] = 48 + (tm->f.hour / 10);
    time_buff[1] = 48 + (tm->f.hour % 10);
    //time_buff[2] = ':';
    time_buff[3] = 48 + (tm->f.min / 10);
    time_buff[4] = 48 + (tm->f.min % 10);
    //time_buff[5] = ':';
    time_buff[6] = 48 + (tm->f.sec / 10);
    time_buff[7] = 48 + (tm->f.sec % 10);
    //time_buff[8] = 0;
    date_buff[0] = 48 + (tm->f.mday / 10);
    date_buff[1] = 48 + (tm->f.mday % 10);
    //date_buff[2] = '/';
    date_buff[3] = 48 + (tm->f.mon / 10);
    date_buff[4] = 48 + (tm->f.mon % 10);
    //date_buff[5] = '/';
    //date_buff[6] = '2'; date_buff[7] = '0';
    date_buff[8] = 48 + (tm->f.year / 10);
    date_buff[9] = 48 + (tm->f.year % 10);
    //date_buff[10] = 0;
}

UINT32 rtc_2uint32(rtc_timedate *tm) {
    UINT32 ret = (UINT32) tm->f.sec;
    ret |= ((UINT32) tm->f.min << 6);
    ret |= ((UINT32) tm->f.hour << 12);
    ret |= ((UINT32) tm->f.mday << 17);
    ret |= ((UINT32) tm->f.mon << 22);
    ret |= ((UINT32) tm->f.year << 26);
    return ret;
}

/******************************************************************************/
void RTCLock(char Lock) {
    if (Lock == 0)
        mRtccWrOff();
    else {
        _asm
        movlb 0x0f
        movlw 0x55
        movwf EECON2, 0
        movlw 0xAA
        movwf EECON2, 0
        bsf RTCCFG, 5, 1
        _endasm
    }
}

unsigned char mBcd2Dec(BYTE bcd) {
    return (((bcd) >> 4)*10 + ((bcd) & 0x0F));
}

unsigned char mDec2Bcd(BYTE dec) {
    return ((((dec) / 10) << 4) | ((dec) % 10));
}