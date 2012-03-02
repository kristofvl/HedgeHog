/********************************************************************
 FileName:     	osc.c,     the HedgeHog's oscillator lib source code
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#include "osc.h"

void set_osc_8Mhz(void) {
    OSCCONbits.IRCF2 = 1; // set internal OSC to 8 Mhz
    OSCCONbits.IRCF1 = 1; //
    OSCCONbits.IRCF0 = 1; //
    OSCCONbits.SCS0 = 1; // use postscaled internal clock
    OSCCONbits.SCS1 = 1; //  (RC_RUN)
    OSCTUNEbits.PLLEN = 0; // disable PLL
}

void set_osc_48Mhz(void) {
    // 18F46j50 needs to set OSCTUNE<PLLEN> bit to power PLL:
    unsigned int pll_startup_counter = 600; // timeout 2+ms
    OSCTUNEbits.PLLEN = 1; // enable PLL
    while (pll_startup_counter--); // wait til PLL locks
    OSCCONbits.SCS0 = 0; // use primary clock source
    OSCCONbits.SCS1 = 0;
}

void set_osc_sleep_t1(unsigned char to) {
    T1GCONbits.TMR1GE = 0; // timer1 counts regardless of t1 gate
    T1CONbits.TMR1CS1 = 1; // timer1 clock is 32khz clock
    T1CONbits.TMR1CS0 = 0;
    T1CONbits.T1CKPS1 = 1; // clock prescaler is 1:8
    T1CONbits.T1CKPS0 = 1;
    T1CONbits.T1OSCEN = 1; // Power up the Timer1 crystal driver and supply the Timer1 clock from the crystal output
    T1CONbits.T1SYNC = 1; // Do not synchronize external clock input
    IPR1bits.TMR1IP = 1; // set high priority interrupt
    PIE1bits.TMR1IE = 1; // Timer1 overflow interrupt enable
    T1CONbits.TMR1ON = 1; // turn timer1 on
    T1CONbits.RD16 = 0;
    TMR1H = 0xFF;
    TMR1L = 0xFF - to; //37 leads to a 10ms sampling (verified by oscilloscope)
    OSCCONbits.IDLEN = 0; // sleep starts sleep mode (not idle)
    LATBbits.LATB7 = 1;
    Sleep(); // Zzzzzz....
    LATBbits.LATB7 = 0;
}

void set_osc_sleep_int1() {
    OSCCONbits.IDLEN = 0; // sleep starts sleep mode (not idle)
    LATBbits.LATB7 = 1;
    Sleep(); // Zzzzzz....
    LATBbits.LATB7 = 0;
}

void set_osc_deep_sleep() {
    // see section 4.6 Deep Sleep Mode in the PIC 18F46j50 data sheet
    WDTCONbits.REGSLP = 1;
    OSCCONbits.IDLEN = 0; // sleep starts sleep mode (not idle)
    INTCONbits.GIE = 0;
    DSCONHbits.DSEN = 1; // deep sleep enable
    Sleep();
}