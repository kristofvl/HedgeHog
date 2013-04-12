/********************************************************************
 FileName:     	SD_FAT.h,     the HedgeHog's FAT routines header
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#ifndef SD_FAT__H
#define SD_FAT__H

#include "SD_Buffer.h"

#define SDBUF_INITFAT() { sd_buffer.mvf.ID1 = 0xF8FFFFFF; }
#define write_SD(sector, buf) MDD_SDSPI_SectorWrite(sector, buf, 0);
#define read_SD(sector, buf) MDD_SDSPI_SectorRead(sector, buf);
#define SECTOR_RT 244       // root table start sector
#define SECTOR_CF 340       // configuration file start sector
#define SECTOR_LG 4500      // logging files start sector

void write_MBR(sd_buffer_t *sd_buffer);
void write_root_table(sd_buffer_t *sd_buffer, char *id_str);
void write_FAT(sd_buffer_t *sd_buffer, UINT16 i);
void close_FAT(sd_buffer_t *sd_buffer);

#endif // SD_FAT__H
