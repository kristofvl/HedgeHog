/********************************************************************
 FileName:     	FSconfig.h,     the HedgeHog's SD configuration
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/


#ifndef _FS_DEF_

#include "HardwareProfile.h"

/***************************************************************************/
/*   Note:  There are likely pin definitions present in the header file    */
/*          for your device (SP-SPI.h, CF-PMP.h, etc).  You may wish to    */
/*          specify these as well                                          */
/***************************************************************************/
   
// The FS_MAX_FILES_OPEN #define is only applicable when Dynamic
// memeory allocation is not used (FS_DYNAMIC_MEM not defined).
// Defines how many concurent open files can exist at the same time.
// Takes up static memory. If you do not need to open more than one
// file at the same time, then you should set this to 1 to reduce
// memory usage
#define FS_MAX_FILES_OPEN 	1
/************************************************************************/

// The size of a sector
#define MEDIA_SECTOR_SIZE 		512
/************************************************************************/



/******************************************************************************/
/***Compiler options to enable/Disable Features based on user's application ***/
/******************************************************************************/


// Uncomment this to use the FindFirst, FindNext, and FindPrev
//#define ALLOW_FILESEARCH
/************************************************************************/
// Comment this line out if you don't intend to write data to the card
//#define ALLOW_WRITES
/************************************************************************/
// Comment this line out if you don't intend to format your card
// Writes must be enabled to use the format function
//#define ALLOW_FORMATS
/************************************************************************/
// Uncomment this definition if you're using directories
// Writes must be enabled to use directories
//#define ALLOW_DIRS
/************************************************************************/

// Allows the use of FSfopenpgm, FSremovepgm, etc with PIC18
#if defined(__18CXX)
//    #define ALLOW_PGMFUNCTIONS
#endif
/************************************************************************/

// Allows the use of the FSfprintf function
// Writes must be enabled to use the FSprintf function
//#define ALLOW_FSFPRINTF
/************************************************************************/

// If FAT32 support required then uncomment the following
//#define SUPPORT_FAT32
/* ******************************************************************************************************* */




// Select how you want the timestamps to be updated
// Use the Real-time clock peripheral to set the clock
// You must configure the RTC in your application code
//#define USEREALTIMECLOCK
// The user will update the timing variables manually using the SetClockVars function
// The user should set the clock before they create a file or directory (Create time),
// and before they close a file (last access time, last modified time)
//#define USERDEFINEDCLOCK
// Just increment the time- this will not produce accurate times and dates
#define INCREMENTTIMESTAMP

#ifdef USE_PIC18
	#ifdef USEREALTIMECLOCK
		#error The PIC18 architecture does not have a Real-time clock and calander module
	#endif
#endif

#ifdef ALLOW_PGMFUNCTIONS
	#ifndef USE_PIC18
		#error The pgm functions are unneccessary when not using PIC18
	#endif
#endif

#ifndef USEREALTIMECLOCK
    #ifndef USERDEFINEDCLOCK
        #ifndef INCREMENTTIMESTAMP
            #error Please enable USEREALTIMECLOCK, USERDEFINEDCLOCK, or INCREMENTTIMESTAMP
        #endif
    #endif
#endif

/************************************************************************/
// Define FS_DYNAMIC_MEM to use malloc for allocating
// FILE structure space.  uncomment all three lines
/************************************************************************/
#if 0
	#define FS_DYNAMIC_MEM
	#ifdef USE_PIC18
		#define FS_malloc	SRAMalloc
		#define FS_free		SRAMfree
	#else
		#define FS_malloc	malloc
		#define FS_free		free
	#endif
#endif

// Associate the physical layer functions with the correct physical layer
// USE_SD_INTERFACE_WITH_SPI       // SD-SPI.c and .h

    #define MDD_MediaInitialize     MDD_SDSPI_MediaInitialize
    #define MDD_MediaDetect         MDD_SDSPI_MediaDetect
    #define MDD_SectorRead          MDD_SDSPI_SectorRead
    #define MDD_SectorWrite         MDD_SDSPI_SectorWrite
    #define MDD_InitIO              MDD_SDSPI_InitIO
    #define MDD_ShutdownMedia       MDD_SDSPI_ShutdownMedia
    #define MDD_WriteProtectState   MDD_SDSPI_WriteProtectState
    #define MDD_ReadSectorSize      MDD_SDSPI_ReadSectorSize
    #define MDD_ReadCapacity        MDD_SDSPI_ReadCapacity
    #define MDD_FINAL_SPI_SPEED     2000000


#endif
