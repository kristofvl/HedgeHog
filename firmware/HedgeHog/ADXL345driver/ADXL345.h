/********************************************************************
 FileName:     	ADXL345.h,     the ADXL345 lib header file
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, or OLED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#ifndef ADXL345__H
#define ADXL345__H

#include "Compiler.h"
#include "GenericTypeDefs.h"
#include "HardwareProfile.h"
#include "HHG_conf.h"       // for acc configuration
#include "acc3D_wrapper.h"

// registers:
#define ADXL345_CHIP_ID  0x00
// 0x01 to 0x1C reserved
#define ADXL345_TAP_TH   0x1D
#define ADXL345_X_OFFSET 0x1E
#define ADXL345_Y_OFFSET 0x1F
#define ADXL345_Z_OFFSET 0x20
#define ADXL345_TAP_DUR  0x21  // Tap Duration
#define ADXL345_TAP_LAT  0x22  // Tap Latency
#define ADXL345_TAP_WIN  0x23  // Tap Window
#define ADXL345_ACT_TH   0x24  // Activity Threshold
#define ADXL345_INA_TH   0x25  // Inactivity Threshold
#define ADXL345_INA_TIME 0x26  // Inactivity Time
#define ADXL345_ACT_INA  0x27  // Activity Inactivity Detection
#define ADXL345_FREEF_TH 0x28  // Freefall Threshold
#define ADXL345_FREEF_TM 0x29  // Freefall Time
#define ADXL345_TAP_AXES 0x2A  // Axis control for single/double tap
#define ADXL345_TAP_STAT 0x2B  // Tap Status
#define ADXL345_BWRATE   0x2C  // Data Rate and Power Mode Control
#define ADXL345_POWR_CTL 0x2D  // Power Saving Features
#define ADXL345_INT_EN   0x2E  // Interrupt Enable
#define ADXL345_INT_MAP  0x2F  // Interrupt Mapping Control
#define ADXL345_INT_SRC  0x30  // Interrupt Source
#define ADXL345_DATA_FMT 0x31  // Data Format

// Power Control register:
#define ADXL345_POW_LINK      0x20
#define ADXL345_POW_AUTOSLEEP 0x10
#define ADXL345_POW_MEASURE   0x08
#define ADXL345_POW_SLEEP     0x04
#define ADXL345_POW_WAKEUP1   0x03
#define ADXL345_POW_WAKEUP2   0x02
#define ADXL345_POW_WAKEUP4   0x01
#define ADXL345_POW_WAKEUP8   0x00

// Format Register:
#define ADXL345_FORM_2G       0x00
#define ADXL345_FORM_4G       0x01
#define ADXL345_FORM_8G       0x02
#define ADXL345_FORM_16G      0x03
#define ADXL345_FORM_LFTJUST  0x04
#define ADXL345_FORM_FULLRES  0x08
#define ADXL345_FORM_INVIINT  0x20
#define ADXL345_FORM_SPI3WRE  0x40
#define ADXL345_FORM_SELFTST  0x80

// Bandwidth and Rate Register:
#define ADXL345_BWRATE_LOWPWR 0x10
#define ADXL345_BWRATE_0_10HZ 0x00
#define ADXL345_BWRATE_0_20HZ 0x01
#define ADXL345_BWRATE_0_39HZ 0x02
#define ADXL345_BWRATE_0_78HZ 0x03
#define ADXL345_BWRATE_1_56HZ 0x04
#define ADXL345_BWRATE_3_13HZ 0x05
#define ADXL345_BWRATE_6_25HZ 0x06
#define ADXL345_BWRATE_12_5HZ 0x07
#define ADXL345_BWRATE_25_0HZ 0x08
#define ADXL345_BWRATE_50_0HZ 0x09
#define ADXL345_BWRATE_100_HZ 0x0A
#define ADXL345_BWRATE_200_HZ 0x0B
#define ADXL345_BWRATE_400_HZ 0x0C
#define ADXL345_BWRATE_800_HZ 0x0D
#define ADXL345_BWRATE_1600HZ 0x0E
#define ADXL345_BWRATE_3200HZ 0x0F

#define ADXL345_ACC_X_LSB 0x32
#define ADXL345_ACC_X_MSB 0x33
#define ADXL345_ACC_Y_LSB 0x34
#define ADXL345_ACC_Y_MSB 0x35
#define ADXL345_ACC_Z_LSB 0x36
#define ADXL345_ACC_Z_MSB 0x37

#define ADXL345_INT_DTBIT    0x20   // double tap bit
#define ADXL345_INT_ACBIT    0x10   // activity bit
#define ADXL345_INT_INBIT    0x08   // inactivity bit

#define ADXL345_FIFO_CTL 0x38   // Fifo Control
#define ADXL345_FIFO_ST  0x39   // Fifo Status

#define ADXL345_FIFOMODE_BYPASS  0x00 // bypass fifo
#define ADXL345_FIFOMODE_FIFO    0x40 // stop after 32 values
#define ADXL345_FIFOMODE_STREAM  0x80 // overwrite new data
#define ADXL345_FIFOMODE_TRIGGER 0xC0 // only fill fifo when triggered

#define ADXL345_FIFOSAMPLES_0   0x00
#define ADXL345_FIFOSAMPLES_32  0x1F

#define ADXL345_ACTEN_AC        0x80
#define ADXL345_ACTEN_XYZ       0x70
#define ADXL345_INACTEN_AC      0x08
#define ADXL345_INACTEN_XYZ     0x07

#define ADXL345_READ 0x80  // set first bit to read
#define ADXL345_MREAD 0xC0 // set two first bits to do a multi-read

#define adxl345_doubletap (PORTBbits.RB2)
#define adxl345_clear_int1() {adxl345_read_byte(ADXL345_INT_SRC);}

void adxl345_init(hhg_conf_accs_t cnf, UINT32* initmsg);
void adxl345_get_xyz(PACC_XYZ adxl345);
void adxl345_setmode_fifo();
void adxl345_setmode_pull();
void adxl345_setmode_acti(UINT8 th);
UINT8 adxl345_getint();
void adxl345_conf_tap(UINT8 axes, UINT8 th, UINT8 dur, UINT8 lat, UINT8 win);
void adxl345_write_byte(BYTE address, BYTE data);
BYTE adxl345_read_byte(BYTE address);
void adxl345_write_str(PACC_XYZ adxl345_xyz, char* acc_buff);

#endif // ADXL345__H