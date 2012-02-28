#include "ambient_light.h"

void init_light(void)
{
    TRISAbits.TRISA5 = 1;
    ANCON0bits.PCFG4 = 0;
#if defined(LIGHT_PWR)
    TRISBbits.TRISB0 = 0;
    LIGHT_PWR        = 1;
#endif
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

WORD_VAL read_light(void)
{
    WORD_VAL res;
    ADCON0bits.GO = 1;
    while(ADCON0bits.NOT_DONE);
    res.v[0] = ADRESL;
    res.v[1] = ADRESH;
    return res;
}
