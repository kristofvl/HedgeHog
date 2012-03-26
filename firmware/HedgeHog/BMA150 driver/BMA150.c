#include "BMA150.h"


void bma150_init(hhg_conf_accs_t cnf, UINT32* initmsg)
{
    WORD i;
    BMA150_REG reg;
    BYTE range, bw;
    
    bma150_SPI_init();
	
    reg.val = bma150_read_byte(BMA150_CHIP_ID);
    Nop();

    if(reg.chip_id != 0x2)
    {
        Nop();
    }
    
    range = cnf.f.range;
    switch (range) {
        case '0': range = BMA150_RANGE_2G; break;
        case '1': range = BMA150_RANGE_4G; break;
        case '2': range = BMA150_RANGE_8G; break;
        case '3': range = BMA150_RANGE_8G; break;
        default:  range = BMA150_RANGE_8G; break;
    }
    bw = cnf.f.bw;
    switch (bw) {
        case '3': bw = BMA150_BW_25; break;
        case '4': bw = BMA150_BW_50; break;
        case '5': bw = BMA150_BW_100; break;
        case '6': bw = BMA150_BW_190; break;
        case '7': bw = BMA150_BW_375; break;
        case '8': bw = BMA150_BW_750; break;
        case '9': bw = BMA150_BW_1500; break;
        default:  bw = BMA150_BW_100; break;
    }

    bma150_set_conf(range, bw);

    i = bma150_read_byte(BMA150_VERSION);
    Nop()
            
    i = bma150_read_byte(BMA150_ADDR11);
    Nop();

    bma150_write_byte(BMA150_ADDR11, 0x00);
    Nop();

    i = bma150_read_byte(BMA150_ADDR11);
    Nop();

    reg.val = bma150_read_byte(BMA150_ADDR14);
    *initmsg = reg.range;
    *initmsg<<8;
    *initmsg |= reg.bandwidth;
    *initmsg<<8;
    *initmsg = reg.range;
    *initmsg<<8;
    *initmsg |= reg.bandwidth;
}

void bma150_SPI_init(void)
{
    SPISTAT = 0x0000;          // power on state
    SPICON1bits.WCOL = 1;
    SPICON1bits.SSPOV = 0;
    SPICON1bits.SSPEN = 0;
    SPICON1bits.CKP = 0;
    SPICON1bits.SSPM3 = 0;		// SPI Master mode, FOSC/4
    SPICON1bits.SSPM2 = 0;
    SPICON1bits.SSPM1 = 0;
    SPICON1bits.SSPM0 = 0;
    SPISTATbits.CKE = 0;
    SPICLOCK = 0;
    SPIOUT = 0;                // define SDO1 as output (master or slave)
    SPIIN = 1;                 // define SDI1 as input (master or slave)
    ACC_CS_TRIS = OUTPUT_PIN; // define the Chip Select pin as output
    SPICON1bits.CKP = 1;
    SPIENABLE = 1;             // enable synchronous serial port
}

void bma150_write_byte(BYTE address, BYTE data)
{
    BYTE storage;

    //See Important Notes section on page 10 note 1 of the v1.5 datasheet
    storage = 0x00;
    if(address == 0x14 || address == 0x34)
    {
        storage = bma150_read_byte(0x14) & 0xE0;
    }

    ACC_CS = 0;
    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = address;
    while (!SPI_INTERRUPT_FLAG);

    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();

    SPI_INTERRUPT_FLAG = 0;

    //See Important Notes section on page 10 note 2 of the v1.5 datasheet
    if(address == 0x0A)
    {
        SPIBUF = data & 0x7F;
    }
    else
    {
        SPIBUF = data | storage;
    }

    while (!SPI_INTERRUPT_FLAG);
    ACC_CS = 1;
}


BYTE bma150_read_byte(BYTE address)
{
    ACC_CS = 0;
    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = BMA150_READ | address;
    while (!SPI_INTERRUPT_FLAG);

    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();
    Nop();Nop();Nop();Nop();Nop();Nop();Nop();Nop();

    SPI_INTERRUPT_FLAG = 0;
    SPIBUF = 0x00;
    while (!SPI_INTERRUPT_FLAG);
    ACC_CS = 1;

    return SPIBUF;
}

void bma150_getXYZ(PACC_XYZ bma150_xyz)
{
    SD_CS = 1; // unselect SD card
    bma150_xyz->x = ((WORD)(bma150_read_byte(BMA150_ACC_X_LSB)) |
                     ((WORD)(bma150_read_byte(BMA150_ACC_X_MSB) ) << 8) )>>6;
    bma150_xyz->y = ((WORD)(bma150_read_byte(BMA150_ACC_Y_LSB)) |
                     ((WORD)(bma150_read_byte(BMA150_ACC_Y_MSB) ) << 8) )>>6;
    bma150_xyz->z = ((WORD)(bma150_read_byte(BMA150_ACC_Z_LSB)) |
                     ((WORD)(bma150_read_byte(BMA150_ACC_Z_MSB) ) << 8) )>>6;
    bma150_xyz->x += 127; if (bma150_xyz->x>255) bma150_xyz->x -= 255;
    bma150_xyz->y += 127; if (bma150_xyz->y>255) bma150_xyz->y -= 255;
    bma150_xyz->z += 127; if (bma150_xyz->z>255) bma150_xyz->z -= 255;
}

void bma150_set_conf(BYTE range, BYTE bw)
{
    /* Bits 5, 6 and 7 of register addresses 14h, 34h contain critical data
    it is highly recommended to read-out the complete byte, perform bit-
    slicing and write back the complete byte with unchanged bits 5, 6 and 7. */
    BMA150_REG reg;
    reg.val = bma150_read_byte(BMA150_ADDR14);
    reg.range = range; // e.g., BMA150_RANGE_4G
    reg.bandwidth = bw; // e.g., BMA150_BW_50;
    bma150_write_byte(BMA150_ADDR14,reg.val);
}

void bma150_write_str(PACC_XYZ bma150, char* acc_buff)
{
    bma150_getXYZ(bma150);
    acc_buff[0] = 48+(bma150->x/100);
    acc_buff[1] = 48+(bma150->x/10)-10*(bma150->x/100);
    acc_buff[2] = 48+(bma150->x%10);
    acc_buff[3] = ',';
    acc_buff[4] = 48+(bma150->y/100);
    acc_buff[5] = 48+(bma150->y/10)-10*(bma150->y/100);
    acc_buff[6] = 48+(bma150->y%10);
    acc_buff[7] = ',';
    acc_buff[8] = 48+(bma150->z/100);
    acc_buff[9] = 48+(bma150->z/10)-10*(bma150->z/100);
    acc_buff[10] = 48+(bma150->z%10);
    acc_buff[11] = 0;
}