#ifndef AMBIENT_LIGHT_H
#define	AMBIENT_LIGHT_H

#include "Compiler.h"
#include "GenericTypeDefs.h"
#include "HardwareProfile.h"

#ifndef LIGHTCHANNEL
#error "LIGHTCHANNEL needs to be defined in the HardwareProfile"
#endif

void light_init(void);
WORD_VAL light_read(void);

#endif	// AMBIENT_LIGHT_H 

