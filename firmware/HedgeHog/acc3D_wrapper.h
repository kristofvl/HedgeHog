/*******************************************************************************
 FileName:     	acc3D_wrapper.h,  a wrapper header for accelerometers
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#include "Compiler.h"
#include "GenericTypeDefs.h"

#ifndef ACCEL3DWRAPPER__H
#define ACCEL3DWRAPPER__H

typedef struct {
    UINT8 x, y, z;
} ACC_XYZ, *PACC_XYZ;

// ADXL345 definitions
#if defined(ADXL345_ENABLED)
#include "./ADXL345driver/ADXL345.h"        // ADXL345 Accelerometer driver
#define acc_init(cnf, init_msg)             adxl345_init(cnf, init_msg)
#define acc_write_string(accval,acc_str)    adxl345_write_str(accval, acc_str)
#define acc_getxyz(accval)                  adxl345_get_xyz(accval)
#define acc_setmode_fifo()                  adxl345_setmode_fifo()
#define acc_setmode_pull()                  adxl345_setmode_pull()
#define acc_setmode_acti(t)                 adxl345_setmode_acti((t))
#define acc_getint()                        adxl345_getint()
#define acc_SPI_init()                      adxl345_SPI_init()
#define acc_deep_sleep()                    adxl345_deep_sleep() 
#endif

// BMA150 definitions
#if defined(BMA150_ENABLED)
#include "./BMA150 driver/BMA150.h"	   // BMA150 Accelerometer driver
#define acc_init(cnf, init_msg)            bma150_init(cnf, init_msg)
#define acc_write_string(accval, acc_str)  bma150_write_str(accval, acc_str)
#define acc_getxyz(accval)                 bma150_getXYZ(accval)
#define acc_setmode_fifo()                 {;}
#define acc_setmode_pull()                 {;}
#define acc_setmode_acti(t)                {;}
#define acc_getint()                       0x00
#define tmp_init()                         {;}
#define tmp_read                           bma150_get_tmp
#define acc_SPI_init()                     bma150_SPI_init()
#define acc_deep_sleep()                   {;}

#endif

#endif //ACCEL3DWRAPPER__H