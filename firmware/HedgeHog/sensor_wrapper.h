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
#define init_tmp()       { ; }
#define read_tmp()       100
#endif

/******************************************************************************/
/******** Button options ******************************************************/
/******************************************************************************/
#if defined(ADXL345_ENABLED)
#define init_button()    {;}
#define button_pressed   adxl345_doubletap
#define button_clear()   adxl345_clear_int1()
#else
#define init_button()    {button_TRIS=1;}
#define button_pressed   (button_pin==0)
#define button_clear()   {while(button_pin==0){;};}
#endif

/******************************************************************************/
/******** Environmental reading definitions and options ***********************/
/******************************************************************************/
#define init_env() { init_light(); init_tmp(); init_button();}
#if defined(LIGHT_PWR)
#define env_on()  { LIGHT_PWR = 0; }
#define env_off()  { LIGHT_PWR = 1; }
#else
#define env_on()   { ; }
#define env_off()  { ; }
#endif
#define read_env(l,t) {env_on(); l=read_light(); t=read_tmp(); env_off(); }


/******************************************************************************/
/******** TODO: string functions need cleaning up *****************************/
/******************************************************************************/
#define write2str(v,s) {s[0]=48+(v/100); s[1]=48+(v/10)-10*(v/100); s[2]=48+(v%10); s[3]=0;}

#endif //SENSORWRAPPER__H
