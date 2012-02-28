#ifndef AMBIENT_LIGHT_H
#define	AMBIENT_LIGHT_H

#include "Compiler.h"
#include "GenericTypeDefs.h"
#include "HardwareProfile.h"
#include "../RTC/rtcc.h"

#ifndef LIGHTCHANNEL
#error "LIGHTCHANNEL needs to be defined in the HardwareProfile"
#endif

void init_light(void);
WORD_VAL read_light(void);

#endif	// AMBIENT_LIGHT_H 

