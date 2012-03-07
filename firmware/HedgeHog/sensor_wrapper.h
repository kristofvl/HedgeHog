/*******************************************************************************
 FileName:     	sensor_wrapper.h,  a wrapper header for all sensors
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#ifndef SENSORWRAPPER__H
#define SENSORWRAPPER__H

#include "Compiler.h"
#include "GenericTypeDefs.h"

/******************************************************************************/
/******** Accelerometer definitions and options *******************************/
/******************************************************************************/
#include "acc3D_wrapper.h"

/******************************************************************************/
/******** Photodiode definitions and options **********************************/
/******************************************************************************/
#include "ambient_light driver/ambient_light.h" // ambient light

/******************************************************************************/
/******** Thermometer definitions and options *********************************/
/******************************************************************************/
#if defined(BMA150_ENABLED)
// sensor definitions are taken care of the bma150 in acc3D_wrapper.h
#else
// stubs for now:
#define tmp_init()       { ; }
#define tmp_read()       100
#endif

/******************************************************************************/
/******** Button options ******************************************************/
/******************************************************************************/
#if defined(ADXL345_ENABLED)
#define button_init()    {;}
#define button_pressed   adxl345_doubletap
#define button_clear()   adxl345_clear_int1()
#else
#define button_init()    {button_TRIS=1;}
#define button_pressed   (button_pin==0)
#define button_clear()   {while(button_pin==0){;};}
#endif

/******************************************************************************/
/******** Environmental reading definitions and options ***********************/
/******************************************************************************/
#define env_init() { light_init(); tmp_init(); button_init();}
#if defined(LIGHT_PWR)
#define env_on()  { LIGHT_PWR = 0; }
#define env_off()  { LIGHT_PWR = 1; }
#else
#define env_on()   { ; }
#define env_off()  { ; }
#endif
#define env_read(l,t) {env_on(); l=light_read(); t=tmp_read(); env_off(); }


/******************************************************************************/
/******** TODO: string functions need cleaning up *****************************/
/******************************************************************************/
#define write2str(v,s) {s[0]=48+(v/100); s[1]=48+(v/10)-10*(v/100); s[2]=48+(v%10); s[3]=0;}

#endif //SENSORWRAPPER__H
