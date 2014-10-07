/********************************************************************
 FileName:     	HardwareProfile.h,
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#ifndef HARDWARE_PROFILE_H
#define HARDWARE_PROFILE_H

#if defined(HEDGEHOG_TESTBED)
#include "HardwareProfileTestbed.h"
#elif defined(HEDGEHOG_OLED)
#include "HardwareProfileOLED.h"
#elif defined(HEDGEHOG_OLED_513)
#include "HardwareProfileOLED513.h"
#elif defined(HEDGEHOG_BASIC)
#include "HardwareProfileBasic.h"
#elif defined(HEDGEHOG_BASIC_417)
#include "HardwareProfileBasic417.h"
#elif defined(HEDGEHOG_BASIC_418)
#include "HardwareProfileBasic418.h"
#elif defined(HEDGEHOG_BASIC_419)
#include "HardwareProfileBasic419.h"
#else
#error No Hardware Profile Defined. See HardwareProfile.h
#endif

/** I/O pin definitions ***********************************/
#define INPUT_PIN 1
#define OUTPUT_PIN 0

#endif  //HARDWARE_PROFILE_H

