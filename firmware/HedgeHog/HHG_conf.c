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

void write_HHG_conf(hhg_conf_t conf)
{
    EraseFlash((UINT32)HHG_CONF_FLASHADDR,(UINT32)HHG_CONF_FLASHADDR+0x400);
    WriteBytesFlash( (UINT32) HHG_CONF_FLASHADDR, 32, (BYTE*) conf.cstr );
}

void read_HHG_conf(hhg_conf_t* conf)
{
    ReadFlash(HHG_CONF_FLASHADDR, 32, (BYTE*) conf->cstr);
}

