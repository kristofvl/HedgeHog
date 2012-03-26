/*******************************************************************************
 FileName:     	rtc.c
 Dependencies:  RTCOSC = T1OSCREF set in config
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#ifndef __RTCCHEDGEHOG_H
#define __RTCCHEDGEHOG_H

#include <p18f46j50.h>	// contains registers
#include <GenericTypeDefs.h> // contains UINT32

// RTCC definitions
typedef enum
{
    RTCCFG_MASK_RTCEN      =   0x80, 
    RTCCFG_MASK_FRZ        =   0x40,
    RTCCFG_MASK_RTCWREN    =   0x20,
    RTCCFG_MASK_RTCSYNC    =   0x10,
    RTCCFG_MASK_HALFSEC    =   0x08,
    RTCCFG_MASK_RTCOE      =   0x04,
    RTCCFG_MASK_RTCPTR     =   0x03
}RTCCFG_MASK;

#define RTCCAL_MASK_CAL        0xFF

//Alarm definitions
typedef enum
{
    ALRMCFG_MASK_ALRMEN    =   0x80,
    ALRMCFG_MASK_CHIME     =   0x40,
    ALRMCFG_MASK_AMASK     =   0x3c,
    ALRMCFG_MASK_ALRMPTR   =   0x03
}ALRMCFG_MASK;

#define ALRMRPT_MASK_ARPT      0xFF

// accessing the RTCC/Alarm Value Register Window pointer bits
typedef enum
{
    RTCCPTR_MASK_SECMIN     =   0x00,
    RTCCPTR_MASK_HRSWEEK    =   0x01,
    RTCCPTR_MASK_DAYMON     =   0x02,
    RTCCPTR_MASK_YEAR       =   0x03   
}RTCCPTR_MASK;

// union/structure for read/write of time and date from/to the RTCC device
typedef union
{
    struct
    {
        BYTE    year;       // 0 BCD codification for year, 00-99
        BYTE    rsvd;       // 1 reserved for future use
        BYTE    mday;       // 2 BCD codification for day of the month, 01-31
        BYTE    mon;        // 3 BCD codification for month, 01-12
        BYTE    hour;       // 4 BCD codification for hours, 00-24
        BYTE    wday;       // 5 BCD codification for day of the week, 00-06
        BYTE    sec;        // 6 BCD codification for seconds, 00-59
        BYTE    min;        // 7 BCD codification for minutes, 00-59
    }f;                     // field access
    BYTE        b[8];       // BYTE access
    WORD        w[4];       // 16 bits access
    UINT32      l[2];       // 32 bits access
}rtccTimeDate;

// valid values of alarm repetition for the RTCC device
typedef enum
{
    RTCC_RPT_HALF_SEC,      // repeat alarm every half second
    RTCC_RPT_SEC,           // repeat alarm every second
    RTCC_RPT_TEN_SEC,       // repeat alarm every ten seconds
    RTCC_RPT_MIN,           // repeat alarm every minute
    RTCC_RPT_TEN_MIN,       // repeat alarm every ten minutes
    RTCC_RPT_HOUR,          // repeat alarm every hour          
    RTCC_RPT_DAY,           // repeat alarm every day
    RTCC_RPT_WEEK,          // repeat alarm every week
    RTCC_RPT_MON,           // repeat alarm every month
    RTCC_RPT_YEAR           // repeat alarm every year (except for Feb 29th.) 
}rtccRepeat;

#define MAX_MIN         (0x59)/* BCD codification for minutes, 00-59 */
#define MAX_SEC         (0x59) /* BCD codification for seconds, 00-59 */
#define MAX_WDAY        (0x6)/* BCD codification for day of the week, 00-06 */
#define MAX_HOUR        (0x24)/* BCD codification for hours, 00-24 */
#define MAX_MON         (0x12)/* BCD codification for month, 01-12 */
#define MIN_MON         (0x1)/* BCD codification for month, 0-1 */
#define MAX_MDAY        (0x31) /* BCD codification for day of the month, 01-31*/
#define MIN_MDAY        (0x1)/* BCD codification for day of the month, 0-1 */
#define MAX_YEAR        (0x99)/* BCD codification for year, 00-99 */

// helper macros
#define mRtccIsWrEn()	(RTCCFGbits.RTCWREN)		
#define mRtccWrOff()	(RTCCFGbits.RTCWREN = 0)	
#define mRtccIsOn()	(RTCCFGbits.RTCEN)				
#define mRtccOff()	(RTCCFGbits.RTCEN=0)			
#define mRtccOn()	(RTCCFGbits.RTCEN=1)			
#define mRtccIsAlrmEnabled()	(ALRMCFGbits.ALRMEN)
#define mRtccAlrmEnable()	(ALRMCFGbits.ALRMEN=1)
#define mRtccAlrmDisable()	(ALRMCFGbits.ALRMEN=0)
#define mRtccIsSync()	(RTCCFGbits.RTCSYNC)
#define mRtccWaitSync()	while((BOOL)RTCCFGbits.RTCSYNC)		
#define mRtccIs2ndHalfSecond()	(RTCCFGbits.HALFSEC)		
#define mRtccClearRtcPtr()	(RTCCFG&=~RTCCFG_MASK_RTCPTR)	
#define mRtccSetRtcPtr(mask)	(RTCCFG|=mask) 				
#define mRtccSetAlrmPtr(mask)	(ALRMCFG |= mask)				
#define mRtccClearAlrmPtr()	(ALRMCFG&=~ALRMCFG_MASK_ALRMPTR)	
#define mRtccGetChimeEnable()	(ALRMCFGbits.CHIME)			
#define mRtccGetCalibration()   (RTCCAL)					
#define mRtccSetClockOe(enable)   (RTCCFGbits.RTCOE=enable)	
#define mRtccGetClockOe()	(RTCCFGbits.RTCOE)	
#define mRtccSetInt(enable)   (PIE3bits.RTCIE=enable)	
#define mRtcc_Clear_Intr_Status_Bit     (PIR3bits.RTCCIF = 0)
#define mRtccGetAlarmRpt()   (ALRMCFGbits.AMASK)	
#define mRtccGetAlarmRptCount()	(ALRMRPT)	

void   rtc_init(void);
void   rtc_read(rtccTimeDate *tm);
void   rtc_write(rtccTimeDate *tm);
BYTE   rtc_get_sec(void);
void   rtc_writestr(rtccTimeDate *tm, char* date_buff, char* time_buff);
UINT32 rtc_2uint32(rtccTimeDate *tm);

#endif /* __RTCCHEDGEHOG_H */
