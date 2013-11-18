/*******************************************************************************
 FileName:     	HHG_conf.c,     the HedgeHog's configuration structure
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        TaimoorB, KristofVL
 ******************************************************************************/

#include "HHG_conf.h"

#pragma romdata HHG_CONF_ADDRESS = HHG_CONF_FLASHADDR
rom char reserve_HHG_conf[0x400];
#pragma code

void write_HHG_conf(hhg_conf_t* conf, sd_buffer_t* sd_buffer)
{
    UINT16 i;
    // write the configuration string to program memory:
    EraseFlash((UINT32)HHG_CONF_FLASHADDR,(UINT32)HHG_CONF_FLASHADDR+0x400);
    WriteBytesFlash((UINT32)HHG_CONF_FLASHADDR,HHG_CONF_BYTES,(BYTE*)conf->cstr);
    // write the configuration string to the sd card / config.hhg file:
    for (i=0; i<HHG_CONF_BYTES; i++)
        sd_buffer->bytes[i] = conf->cstr[i] ;
    sd_buffer->bytes[HHG_CONF_BYTES] = 0;
    write_SD(SECTOR_CF, sd_buffer->bytes);
    // update the disk label to reflect the ID:
    write_root_table(sd_buffer, (char*) conf->cstr);
    write_SD(SECTOR_RT, sd_buffer->bytes);
}

void read_HHG_conf(hhg_conf_t* conf, sd_buffer_t* sd_buffer)
{
    UINT16 i;
    // read the configuration string from program memory:
    //ReadFlash(HHG_CONF_FLASHADDR, HHG_CONF_BYTES, (BYTE*) conf->cstr);
    // if that fails (the ID is zero'd), then read the configuration string
    // from the sd card / config.hhg file:
    //if ((conf->cstr[0] < 32)||(conf->cstr[0] > 126))
    { // ( no character? )
        i=0;
        while (i<8) { // we have 7 retries / 8 tries, 
            if ( MDD_SDSPI_SectorRead(SECTOR_CF, (BYTE*) sd_buffer) )
                i=9;
            else i++;
        }
        if (i==9) { // if we have valid data:
            for (i=0; i<HHG_CONF_BYTES; i++)
                conf->cstr[i] = sd_buffer->bytes[i];
        }
    }
    // update the disk label to reflect the ID:
    write_root_table(sd_buffer, (char*) conf->cstr);
    write_SD(SECTOR_RT, sd_buffer->bytes);
}

