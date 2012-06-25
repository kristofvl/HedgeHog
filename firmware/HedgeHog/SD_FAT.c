/********************************************************************
 FileName:     	SD_FAT.c,     the HedgeHog's FAT routines source code
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#include "SD_FAT.h"
#define ROOT_ENTRY_LENGTH       32      // Root Table has 32-byte entries
#define OFFSET_FILENAME         0x00
#define OFFSET_FILE_EXT         0x08
#define OFFSET_FILE_ATTRIB      0x0B
#define OFFSET_FILE_CR_MS       0x0D
#define OFFSET_FILE_CR_HMS      0x0E
#define OFFSET_FILE_CR_DATE     0x10
#define OFFSET_LAST_ACC_DATE    0x12
#define OFFSET_EXT_ADDR_IND     0x14
#define OFFSET_LAST_UP_T        0x16
#define OFFSET_LAST_UP_DATE     0x18
#define OFFSET_FIRST_CLUSTER    0x1A
#define OFFSET_FILE_SIZE        0x1C

#define FILENAME__SZ         8
#define FILE_EXT__SZ         3
#define FILE_ATTRIB__SZ      1
#define FILE_CR_MS__SZ       1
#define FILE_CR_HMS__SZ      1
#define FILE_CR_DATE__SZ     2
#define LAST_ACC_DATE__SZ    2
#define EXT_ADDR_IND__SZ     2
#define LAST_UP_T__SZ        2
#define LAST_UP_DATE__SZ     2
#define FIRST_CLUSTER__SZ    2
#define FILE_SIZE__SZ        4

// Root Table for Logging SD card, naming the disk to HEDGEHOG,
// and displaying logfile (LOGXXX.HHG) to log to:
const BYTE SDRootTable[] = {
//0    1    2    3    4    5    6    7    8    9    A    B  C D   E    F
0x48,0x45,0x44,0x47,0x45,0x48,0x4F,0x47,0x20,0x20,0x20,0x08,0,0,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x66,0x86,0xA7,0x3C,0x00,0x00,0,0,0x00,0x00,
0x4C,0x4F,0x47,0x30,0x30,0x30,0x20,0x20,0x48,0x48,0x47,0x20,8,6,0x3B,0x8A,
0xA7,0x3C,0xA7,0x3C,0x00,0x00,0x62,0x57,0xA6,0x3C,0x02,0x00,0,0,0x19,0x00
                                    // ... [2:start cluster] [4:file size]
};
const BYTE SDRootTable2[] = {
    0x4C,0x4F,0x47,0x30,0x30,0x30,0x20,0x20,0x48,0x48,0x47,0x20,8,6,0x3B,0x8A,
0xA7,0x3C,0xA7,0x3C,0x00,0x00,0x62,0x57,0xA6,0x3C,0x02,0x00,0,0,0x19,0x00
};

const BYTE SDRootTable3[] = {
    'c','o','n','f','i','g',0x20,0x20,0x48,0x48,0x47,0x20,8,6,0x3B,0x8A,
0xA7,0x3C,0xA7,0x3C,0x00,0x00,0x62,0x57,0xA6,0x3C,0x02,0x00,0,0,0x19,0x00
};

const BYTE SDMasterBootRecord[] = {	// based on MSDOS MBR, without boot code
	0xEB, 0x3C, 0x90, 		// x86 machine code jump
	0x4D, 0x53, 0x44, 0x4F, 0x53, 0x35, 0x2E, 0x30, // OEM name
	0x00, 0x02, 			// 512 bytes per sector
	0x40, 				// 64 sectors per cluster
	0x08, 0x00, 			// 8-1 reserved sectors
	0x02, 				// 2 FATs
	0x00, 0x02, 			// max. 512 entries in root
	0x00, 0x00,
	0xF8, 				// media descriptor: HD
	0xEC, 0x00, 			// sectors per FAT
	0x3F, 0x00, 			// sectors per track
	0xFF, 0x00, 			// number of pages / heads
	0x87, 0x00, 0x00, 0x00, 	// number of hidden sectors
	0x39, 0xE0, 0x3A, 0x00, 	// total number of sectors
	0x00, 				// physical BIOS number
	0x00, 				// reserved
	0x29, 				// ext. boot signature
	0x0A, 0x38, 0x86, 0xC8, 	// data system id
        //name of data system: 'NO NAME    '
	0x4E, 0x4F, 0x20, 0x4E, 0x41, 0x4D, 0x45, 0x20, 0x20, 0x20, 0x20,
	0x46, 0x41, 0x54, 0x31, 0x36, 0x20, 0x20, 0x20,  // 'FAT16   ' string
	// normally 448 more bytes here for the boot code (not used)
	0x55, 0xAA			// final two bytes of bootrecord
};

void write_MBR(sd_buffer_t *sd_buffer) {
    UINT16 sdbuff_i = 0;
    for (sdbuff_i = 0; sdbuff_i < 62; sdbuff_i++)
        sd_buffer->bytes[sdbuff_i] = SDMasterBootRecord[sdbuff_i];
    for (sdbuff_i = 62; sdbuff_i < 64; sdbuff_i++)
        sd_buffer->bytes[448 + sdbuff_i] = SDMasterBootRecord[sdbuff_i];
}

void write_root_table(sd_buffer_t *sd_buffer)
{
    UINT16 clustp = 0;
    UINT16 file_i = 0;

    //Write Volume Label
    for (sdbuffer_i = 0; sdbuffer_i < 32; sdbuffer_i++)
        sd_buffer->bytes[sdbuffer_i] = SDRootTable[sdbuffer_i];

    // Write config file
    clustp = 0x0002;
    for(sdbuffer_i=32; sdbuffer_i<64; sdbuffer_i++)
        sd_buffer->bytes[sdbuffer_i] = SDRootTable3[sdbuffer_i%32];
    clustp += 0x32;
    sd_buffer->bytes[64-5] = clustp >> 8;
    sd_buffer->bytes[64-6] = clustp;

    // Write log files
    for (file_i=0; file_i<14; file_i++) {
        for (sdbuffer_i=64+32*file_i;sdbuffer_i<(64+32*(file_i+1));sdbuffer_i++)
            sd_buffer->bytes[sdbuffer_i] = SDRootTable2[sdbuffer_i%32];
        sd_buffer->bytes[32+36+(32*file_i)] = 48 + (file_i / 10);
        sd_buffer->bytes[32+37+(32*file_i)] = 48 + (file_i % 10);
        clustp += 0x32;
        sd_buffer->bytes[32+32+(32*(file_i+1))-5] = clustp >> 8;
        sd_buffer->bytes[32+32+(32*(file_i+1))-6] = clustp;
    }
    sd_buffer->bytes[511] = 0x01; // last file holds 17Mb
}

void write_FAT(sd_buffer_t *sd_buffer, UINT16 i)
{
    for (sdbuffer_i=0;sdbuffer_i<256;sdbuffer_i++) {
        sd_buffer->wrd[sdbuffer_i] = sdbuffer_i + 256*(i)+1;
    }
}

void close_FAT(sd_buffer_t *sd_buffer)
{
    sd_buffer->bytes[510] = 0xFF;
    sd_buffer->bytes[511] = 0xFF;
}