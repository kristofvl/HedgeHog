/********************************************************************
 FileName:     	ADXL345.c,     the ADXL345 lib source file
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, or OLED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ********************************************************************/

#include "ADXL345.h"

void adxl345_setmode_fifo() {
    adxl345_write_byte(ADXL345_BWRATE,
        ADXL345_BWRATE_100_HZ | ADXL345_BWRATE_LOWPWR ); // sets low power mode
    Nop();
    adxl345_write_byte(ADXL345_FIFO_CTL,
        ADXL345_FIFOMODE_FIFO | ADXL345_FIFOSAMPLES_32); // FIFOmode, 32 samples
    Nop();
}

void adxl345_setmode_pull() {
    adxl345_write_byte(ADXL345_FIFO_CTL, ADXL345_FIFOMODE_BYPASS);
    Nop();
}

void adxl345_setmode_acti(UINT8 th) {
    adxl345_write_byte(ADXL345_BWRATE, ADXL345_BWRATE_100_HZ);
    Nop();
    adxl345_write_byte(ADXL345_FIFO_CTL, ADXL345_FIFOMODE_BYPASS);
    Nop();
    adxl345_write_byte(ADXL345_ACT_TH,  th);  // set activity threshold
    adxl345_write_byte(ADXL345_ACT_INA, ADXL345_ACTEN_AC | ADXL345_ACTEN_XYZ);
    adxl345_write_byte(ADXL345_INT_EN,  ADXL345_INT_ACBIT);
}

// configure and enable doubletap interrupt
void adxl345_conf_tap(UINT8 axes, UINT8 th, UINT8 dur, UINT8 lat, UINT8 win) {
    adxl345_write_byte(ADXL345_TAP_AXES, axes); // suppress, z
    adxl345_write_byte(ADXL345_TAP_TH,   th);   // tap threshold
    adxl345_write_byte(ADXL345_TAP_DUR,  dur);  // tap duration
    adxl345_write_byte(ADXL345_TAP_LAT,  lat);  // tap latency
    adxl345_write_byte(ADXL345_TAP_WIN,  win);  // tap window
    adxl345_write_byte(ADXL345_INT_EN,   ADXL345_INT_DTBIT);
}

UINT8 adxl345_getint() {
    return adxl345_read_byte(ADXL345_INT_SRC);
}

void adxl345_write_byte(BYTE address, BYTE data) {
    ACC_CS = 0;
    SD_CS = 1;
    Nop();
    Nop();
    Nop();

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = address;
    while (!SPI_INTERRUPT_FLAG);

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = data;
    while (!SPI_INTERRUPT_FLAG);

    ACC_CS = 1;
}

BYTE adxl345_read_byte(BYTE address) {
    ACC_CS = 0;
    SD_CS = 1;
    Nop();
    Nop();
    Nop();

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = ADXL345_READ | address;
    while (!SPI_INTERRUPT_FLAG);

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);

    ACC_CS = 1;
    return SPIBUF;
}

void adxl345_get_xyz(PACC_XYZ adxl345) {
    ACC_CS = 0;
    SD_CS = 1;
    Nop();
    Nop();
    Nop();

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0xF2; // do a multiread of all 6 bytes
    while (!SPI_INTERRUPT_FLAG);

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);
    adxl345->x = SPIBUF;
    adxl345->x ^= 0x80;

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);
    adxl345->y = SPIBUF;
    adxl345->y ^= 0x80;

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);
    adxl345->z = SPIBUF;
    adxl345->z ^= 0x80;

    ACC_CS = 1;
}

void adxl345_write_str(PACC_XYZ adxl345, char* acc_buff) {
    adxl345_get_xyz(adxl345);
    acc_buff[0] = 48 + (adxl345->x / 100);
    acc_buff[1] = 48 + (adxl345->x / 10) - 10 * (adxl345->x / 100);
    acc_buff[2] = 48 + (adxl345->x % 10);
    acc_buff[3] = ',';
    acc_buff[4] = 48 + (adxl345->y / 100);
    acc_buff[5] = 48 + (adxl345->y / 10) - 10 * (adxl345->y / 100);
    acc_buff[6] = 48 + (adxl345->y % 10);
    acc_buff[7] = ',';
    acc_buff[8] = 48 + (adxl345->z / 100);
    acc_buff[9] = 48 + (adxl345->z / 10) - 10 * (adxl345->z / 100);
    acc_buff[10] = 48 + (adxl345->z % 10);
    acc_buff[11] = 0;
}


void adxl345_init(hhg_conf_accs_t cnf, UINT32* initmsg) {
    UINT8 range, bw;
    
    SD_CS = 1;
#if defined(oledSC)
    oledCS = 1;
#endif

    // configure SPI:
    SPISTAT = 0x0000; // power on state
    SPICON1bits.WCOL = 1;
    SPICON1bits.SSPOV = 0;
    SPICON1bits.SSPEN = 0;
    SPICON1bits.CKP = 0;
    SPICON1bits.SSPM3 = 0; // SPI Master mode, FOSC/4
    SPICON1bits.SSPM2 = 0;
    SPICON1bits.SSPM1 = 0;
    SPICON1bits.SSPM0 = 0;
    SPISTATbits.CKE = 0;
    SPICLOCK = 0;
    SPIOUT = OUTPUT_PIN; // define SDO1 as output (master or slave)
    SPIIN = INPUT_PIN; // define SDI1 as input (master or slave)
    ACC_CS_TRIS = OUTPUT_PIN; // define the Chip Select pin as output
    SPICON1bits.CKP = 1; // set clock polarity
    SPIENABLE = 1; // enable synchronous serial port

    // configure interrupts:
    // for the HedgeHOG, RP5 (B2) has been mapped to INT1 (see HardwareProfile)
    ACC_INT_TRIS = INPUT_PIN; // set interrupt pin to input
    INTCON3bits.INT1IP = 1; // high priority int1
    INTCON3bits.INT1IF = 0;
    INTCON3bits.INT1IE = 1;

    // go into power mode:
    adxl345_write_byte(ADXL345_POWR_CTL,
            ADXL345_POW_MEASURE | ADXL345_POW_LINK);
    Nop();
    *initmsg = adxl345_read_byte(ADXL345_POWR_CTL);
    *initmsg<<8;

    range = cnf.f.range;
    switch (range) {
        case '0': range = ADXL345_FORM_2G;  break;
        case '1': range = ADXL345_FORM_4G;  break;
        case '2': range = ADXL345_FORM_8G;  break;
        case '3': range = ADXL345_FORM_16G; break;
        default:  range = ADXL345_FORM_4G;  break;
    }
    bw = cnf.f.bw;
    switch (bw) {
        case '0': bw = ADXL345_BWRATE_0_10HZ; break;
        case '1': bw = ADXL345_BWRATE_6_25HZ; break;
        case '2': bw = ADXL345_BWRATE_12_5HZ; break;
        case '3': bw = ADXL345_BWRATE_25_0HZ; break;
        case '4': bw = ADXL345_BWRATE_50_0HZ; break;
        case '5': bw = ADXL345_BWRATE_100_HZ; break;
        case '6': bw = ADXL345_BWRATE_200_HZ; break;
        case '7': bw = ADXL345_BWRATE_400_HZ; break;
        case '8': bw = ADXL345_BWRATE_800_HZ; break;
        case '9': bw = ADXL345_BWRATE_1600HZ; break;
        default:  bw = ADXL345_BWRATE_100_HZ; break;
    }

    // set right data format:
    adxl345_write_byte(ADXL345_DATA_FMT, range | ADXL345_FORM_LFTJUST );
    Nop();
    adxl345_write_byte(ADXL345_BWRATE, bw ); // sets low power mode by default
    Nop();
    adxl345_write_byte(ADXL345_FIFO_CTL, ADXL345_FIFOMODE_BYPASS);
    Nop();

    *initmsg |= adxl345_read_byte(ADXL345_DATA_FMT);
    *initmsg<<8;

    adxl345_conf_tap(0x09, 0xA0, 0x72, 0x30, 0xFF); // configure double tap

    *initmsg |= adxl345_read_byte(ADXL345_CHIP_ID);
    *initmsg<<8;
}
