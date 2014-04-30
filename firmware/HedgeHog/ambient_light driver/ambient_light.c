#include "ambient_light.h"

void light_init(void)
{
#if defined(HEDGEHOG_BASIC_417) || defined(HEDGEHOG_BASIC_418)
	TRISEbits.TRISE1 = 1;       // light sensor data input (INPUT  = 1)
	TRISEbits.TRISE0 = 0;       // light sensor power pin  (OUTPUT = 0)
	LIGHT_PWR        = 1;       // pull power pin up
#elif defined(HEDGEHOG_OLED_513)
	TRISAbits.TRISA5 = 1;       // light sensor data input (INPUT  = 1)
	TRISAbits.TRISA3 = 0;       // light sensor power pin  (OUTPUT = 0)
	LIGHT_PWR        = 1;       // pull power pin up
#else	/* HEDGEHOG_BASIC, HEDGEHOG_OLED, TESTBED*/
	TRISAbits.TRISA5 = 1;
	#if defined(LIGHT_PWR)
		TRISBbits.TRISB0 = 0;
		LIGHT_PWR        = 1;
	#endif
#endif
	ANCON0bits.PCFG4 = 0;
	ADCON1bits.ADFM  = 1;
	ADCON1bits.ADCAL = 0;
	ADCON1bits.ACQT  = 1;
	ADCON1bits.ADCS  = 2;
	ANCON1bits.VBGEN = 1;
	ADCON0bits.VCFG0 = 0;
	ADCON0bits.VCFG1 = 0;
	ADCON0bits.CHS   = LIGHTCHANNEL;
	ADCON0bits.ADON  = 1;
}

WORD_VAL light_read(void)
{
	WORD_VAL res;
	ADCON0bits.GO = 1;
	while(ADCON0bits.NOT_DONE);
	res.v[0] = ADRESL;
	res.v[1] = ADRESH;
	return res;
}
