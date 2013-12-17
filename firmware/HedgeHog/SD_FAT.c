/********************************************************************
 FileName:      SD_FAT.c,     the HedgeHog's FAT routines source code
 Dependencies:
 Processor: PIC18F46J50
 Hardware:  Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:      Microchip C18
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
#define OFFSET_FLS              0x1C   // offset file size

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

#define NUM_FILES            9

rom UINT16 startC[NUM_FILES] = { 3, 68, 133, 263, 523,  978, 1693, 2733, 4163 };
            //, 6048, 8453, 11443, 15083, 19438, 24573 };
rom UINT16 endC[NUM_FILES] = { 67, 132, 262, 522, 977, 1692, 2732, 4162, 6047};
            //, 8452, 11442, 15082, 19437, 24572, 30552  };
rom UINT32 fileSz[NUM_FILES] = { 2129920,  2129920,  4259840, 8519680, 14909440,
                                 23429120, 34078720, 46858240, 61767680 };
            //78807040, 97976320, 119275520, 142704640, 168263680, 195952640 };

// The following 32 bytes describe the volume label of the SD Card:
rom BYTE SDVolLabel[] = {
//0    1    2    3    4    5    6    7    8    9    A    B   C   D   E    F
'H','E','D','G','E','H','G','0','0','0','0',0x08,0,0,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x66,0x86,0xA7,0x3C,0x00,0x00,0,0,0x00,0x00
                                    // ... [2:start cluster] [4:file size]
};
rom BYTE SDLogFiles[] = {
    'L','O','G','0','0','0',' ',' ','H','H','G',' ',8,6,0x3B,0x8A,
0xA7,0x3C,0xA7,0x3C,0x00,0x00,0x62,0x57,0xA6,0x3C,0x45,0x00,0x00,0x80,0x01,0x00
};
rom BYTE SDConfigFile[] = {
    'c','o','n','f','i','g',' ',' ','u','r','e',' ',8,6,0x3B,0x8A,
0xA7,0x3C,0xA7,0x3C,0x00,0x00,0x62,0x57,0xA6,0x3C,0x02,0x00,0x00,0x80,0x20,0x00
};

const BYTE SDMasterBootRecord[] = { // based on MSDOS MBR, without boot code
    0xEB, 0x3C, 0x90,       // x86 machine code jump
    0x4D, 0x53, 0x44, 0x4F, 0x53, 0x35, 0x2E, 0x30, // OEM name
    0x00, 0x02,             // 512 bytes per sector
    0x40,               // 64 sectors per cluster
    0x08, 0x00,             // 8-1 reserved sectors
    0x01,               // 1 FATs
    0x00, 0x02,             // max. 512 entries in root
    0x00, 0x00,
    0xF8,               // media descriptor: HD
    0xEC, 0x00,             // sectors per FAT
    0x3F, 0x00,             // sectors per track
    0xFF, 0x00,             // number of pages / heads
    0x87, 0x00, 0x00, 0x00,     // number of hidden sectors
    0x00, 0xD0, 0x1D, 0x00,     // total number of sectors
        //0xC6, 0xC0, 0x1E, 0x00,
    0x00,               // physical BIOS number
    0x00,               // reserved
    0x29,               // ext. boot signature
    0x0A, 0x38, 0x86, 0xC8,     // data system id
        //name of data system: 'NO NAME    '
    0x4E, 0x4F, 0x20, 0x4E, 0x41, 0x4D, 0x45, 0x20, 0x20, 0x20, 0x20,
    0x46, 0x41, 0x54, 0x31, 0x36, 0x20, 0x20, 0x20,  // 'FAT16   ' string
    // normally 448 more bytes here for the boot code (not used)
    0x55, 0xAA          // final two bytes of bootrecord
};

void write_MBR(sd_buffer_t *sd_buffer)
{
    UINT16 sdbuff_i = 0;
    for (sdbuff_i = 0; sdbuff_i < 62; sdbuff_i++)
        sd_buffer->bytes[sdbuff_i] = SDMasterBootRecord[sdbuff_i];
    for (sdbuff_i = 62; sdbuff_i < 64; sdbuff_i++)
        sd_buffer->bytes[448 + sdbuff_i] = SDMasterBootRecord[sdbuff_i];
}

// Writes the Root Table for a FAT16 filesystem, with the ID in volume label
void write_root_table(sd_buffer_t *sd_buffer, char *id_str)
{
    UINT16 clustp = 0;
    UINT16 file_i = 0;
    UINT16 sdbuffer_i;

    // Clean buffer, we assume the config file is always there
    for (sdbuffer_i = 96; sdbuffer_i<512; sdbuffer_i++)
        sd_buffer->bytes[sdbuffer_i] =  0;

    // Write Volume Label
    for (sdbuffer_i = 0; sdbuffer_i < 32; sdbuffer_i++)
        sd_buffer->bytes[sdbuffer_i] = SDVolLabel[sdbuffer_i];
    // update with 4-byte ID string (if not NULL)
    if (id_str != NULL) {
        for (sdbuffer_i = 7; sdbuffer_i < 11; sdbuffer_i++)
            sd_buffer->bytes[sdbuffer_i] = id_str[sdbuffer_i-7];
    }
    
    // Write config file
    clustp = startC[0];
    for(sdbuffer_i=32; sdbuffer_i<64; sdbuffer_i++)
        sd_buffer->bytes[sdbuffer_i] = SDConfigFile[sdbuffer_i%32];
    sd_buffer->bytes[64-5] = clustp >> 8;
    sd_buffer->bytes[64-6] = clustp;

    // Write File Size
    sd_buffer->bytes[32+OFFSET_FLS+0] = fileSz[0];
    sd_buffer->bytes[32+OFFSET_FLS+1] = fileSz[0]>>8;
    sd_buffer->bytes[32+OFFSET_FLS+2] = fileSz[0]>>16;
    sd_buffer->bytes[32+OFFSET_FLS+3] = fileSz[0]>>24;

    // Write log files
    for (file_i=0; file_i<NUM_FILES-1; file_i++) {
        for (sdbuffer_i=64+32*file_i;sdbuffer_i<(64+32*(file_i+1));sdbuffer_i++)
        {
            sd_buffer->bytes[sdbuffer_i] = SDLogFiles[sdbuffer_i%32];
        }
        sd_buffer->bytes[32+36+(32*file_i)] = 48 + (file_i / 10);
        sd_buffer->bytes[32+37+(32*file_i)] = 48 + (file_i % 10);
        // Write Start Cluster:
        sd_buffer->bytes[32+32+(32*(file_i+1))-5] = startC[file_i+1]>>8;
        sd_buffer->bytes[32+32+(32*(file_i+1))-6] = startC[file_i+1];
        // Write File Size:
        sd_buffer->bytes[32+(32*(file_i+1))+OFFSET_FLS+0] =fileSz[file_i+1];
        sd_buffer->bytes[32+(32*(file_i+1))+OFFSET_FLS+1] =fileSz[file_i+1]>>8;
        sd_buffer->bytes[32+(32*(file_i+1))+OFFSET_FLS+2] =fileSz[file_i+1]>>16;
        sd_buffer->bytes[32+(32*(file_i+1))+OFFSET_FLS+3] =fileSz[file_i+1]>>24;
    }
}

void write_FAT(sd_buffer_t *sd_buffer, UINT16 i)
{
    UINT16 check_byte = 0;
    UINT16 test = 0;
    UINT8  look_i = 0;
    for (sdbuffer_i=0; sdbuffer_i<256; sdbuffer_i++) {
        check_byte = sdbuffer_i + 256*(i) + 1;
        sd_buffer->wrd[sdbuffer_i] = check_byte;
        if(check_byte-1 == 0x00)
            sd_buffer->wrd[sdbuffer_i] = 0xFFF8;
        if(check_byte-1 == 0x01)
            sd_buffer->wrd[sdbuffer_i] = 0xFFFF;
        for(look_i=0; look_i<NUM_FILES; look_i++) {
            test = endC[look_i];
            if(test == (check_byte-1))
                sd_buffer->wrd[sdbuffer_i] =  0xFFFF;
        }
    }
}

void close_FAT(sd_buffer_t *sd_buffer)
{
    sd_buffer->wrd[255] = 0xFFFF;
}