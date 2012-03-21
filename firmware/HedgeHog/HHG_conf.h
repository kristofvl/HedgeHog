/*******************************************************************************
 FileName:     	HHG_conf.h,     the HedgeHog's configuration structure
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        TaimoorB, KristofVL
 ******************************************************************************/

#ifndef HHG_CONFIG_H
#define	HHG_CONFIG_H

#include "GenericTypeDefs.h"
#include "flash.h"

#define HHG_CONF_FLASHADDR 0xFB00
#define HHG_CONF_BYTES 32

#define HHG_CONF_IN_FIFOMODE (hhg_conf.cs.acc_s.f.mode == '1')

typedef union {
            UINT32 u32;
            struct {
                UINT8 range;
                UINT8 bw;
                UINT8 mode; // operating mode fifo, rle, etc.
                UINT8 power; // low power options
            } f;
        } hhg_conf_accs_t;

// HedgeHog configuration variables:
typedef union {
    char   cstr[HHG_CONF_BYTES];   // c bytestring access
    UINT16 uint16s[HHG_CONF_BYTES/2];     // word access
    UINT32 uint32s[HHG_CONF_BYTES/4];     // uint32 access
    struct {                       // config structure:
        UINT32 ID;                  // identifier
        UINT32 time;                // time stamp
        UINT32_VAL acc;             // accelerometer configuration
        hhg_conf_accs_t acc_s;      // accelerometer sensitivity
        UINT32_VAL logg;            // logging & processing setup
    } cs;
} hhg_conf_t;

void write_HHG_conf(hhg_conf_t conf);
void read_HHG_conf(hhg_conf_t* conf);

#endif