/*******************************************************************************
 FileName:     	oled.c
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog OLED or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

/******** Include files *******************************************************/
#include "GenericTypeDefs.h"
#include "Compiler.h"
#include "HardwareProfile.h"
#include "oled.h"

/******************************************************************************/
void oled_init(void) {
    oledWR_TRIS = 0;
    oledWR = 0;
    oledRD_TRIS = 0;
    oledRD = 0;
    oledCS_TRIS = 0;
    oledCS = 1;
    oledD_C_TRIS = 0;
    oledD_C = 0;
    oledRESET = 0;
    Delay1KTCYx(2);
    oledRESET = 1;
    Delay1KTCYx(2);
    oled_cmd(OLEDREG_DISPLAY_OFF); // turn off the display
    oled_cmd(OLEDREG_EDISP_OFF); // turn off the entire display
}

/******************************************************************************/
void oled_reset(void) {

    oledWR_TRIS = 0;    oledWR = 0;
    oledRD_TRIS = 0;    oledRD = 0;
    oledCS_TRIS = 0;    oledCS = 1;
    oledD_C_TRIS = 0;   oledD_C	= 0;

    //Reset the device
    oledRESET = 0;    Delay1KTCYx(2);
    oledRESET = 1;    Delay1KTCYx(2);
    oled_cmd(OLEDREG_DISPLAY_OFF);	// turn off the display
    oled_cmd(OLEDREG_SETVCOMDESL);	// set VCOMH deselect level
    oled_cmd(0x23);
    // set discharge/precharge period:
    oled_cmd(OLEDREG_SETPRECHARGE);	// set precharge period
    oled_cmd(0x22);			 // POR / 2 DCLK
    // Re-map
    oled_cmd(0xA1);                    // [A0]:column address 0 is map to SEG0
                                       // [A1]:column address 131 is map to SEG0
    // COM Output Scan Direction
    oled_cmd(0xC8);                    // C0 is COM0 to COMn, C8 is COMn to COM0
    // COM Pins Hardware Configuration
    oled_cmd(0xDA);			// set pins hardware configuration
    oled_cmd(0x12);
    // Multiplex Ratio
    oled_cmd(0xA8);			// set multiplex ratio
    oled_cmd(0x3F);			// set to 64 mux
    // Display Clock Divide
    oled_cmd(0xD5);			// set display clock divide
    oled_cmd(0xA0);			// set to 100Hz
    // Contrast Control Register
    oled_cmd(OLEDREG_CONTRASTCTRL);	// Set contrast control
    oled_cmd(0x60);			// display 0 ~ 127; 2C
    // Display OLED_OFFSET
    oled_cmd(0xD3);			// set display OLED_OFFSET
    oled_cmd(0x00);			// no OLED_OFFSET
    //Normal or Inverse Display
    oled_cmd(0xA6);			// Normal display
    oled_cmd(0xAD);			// Set DC-DC
    oled_cmd(0x8B);			// 8B=ON, 8A=OFF
    oled_fill(0x00);			// fill display with black pixels

    // Display ON/OFF
    oled_cmd(OLEDREG_DISPLAY_ON);			// AF=ON, AE=OFF
    Delay10KTCYx(20);	//DelayMs(10);
    // Entire Display ON/OFF
    oled_cmd(OLEDREG_EDISP_ON);

    // Display Start Line
    oled_cmd(OLEDREG_SETDISPSTART);	// Set display start line
    // Lower Column Address
    oled_cmd(0x00+OLED_OFFSET);	// Set lower column address
    // Higher Column Address
    oled_cmd(0x10);			// Set higher column address
}

/******************************************************************************/
// write command to display controller
void oled_cmd(BYTE cmd) {
    TRISD = 0x00; 
    LATD  = cmd;
    oledRD = 1;
    oledWR = 1;
    oledD_C	= 0;
    oledCS = 0;
    oledWR = 0;
    oledWR = 1;
    oledCS = 1;
    TRISD = 0xFF;
}

/******************************************************************************/
// write data to the display controller
void oled_write_byte(BYTE data) {
    TRISD = 0x00;
    LATD  = data;
    oledRD = 1;
    oledWR = 1;
    oledD_C	= 1;
    oledCS = 0;
    oledWR = 0;
    oledWR = 1;
    oledCS = 1;
    TRISD = 0xFF;
}

/******************************************************************************/
// read data to the display controller
BYTE oled_read_byte() {
    BYTE ret;
    TRISD = 0xFF;
    oledRD = 1;
    oledWR = 1;
    oledD_C	= 1;
    oledCS = 0;
    oledRD = 0;
    oledRD = 1;
    ret = PORTD;
    oledCS = 1;
    return ret;
}

/******************************************************************************/
// fill oled display with byte
void oled_fill(BYTE data) {
	unsigned char i,j;

	for(i=0xB0;i<0xB8;i++)		// Go through all 8 pages
	{
		oled_cmd(i);		// Set page
		oled_cmd(OLED_OFFSET);	// Set lower column address
		oled_cmd(0x10);		// Set upper column address
		for(j=0;j<132;j++)	// Write to all 132 bytes
		{
			oled_write_byte(data);
		}
	}
}

/******************************************************************************/
// puts pixel at x,y
void oled_put_pixel(SHORT x, SHORT y) {
    BYTE    page, add, lAddr, hAddr;
    BYTE    mask, display;

    // Assign a page address
    if(y < 8)       page = 0xB0;
    else if(y < 16) page = 0xB1;
    else if(y < 24) page = 0xB2;
    else if(y < 32) page = 0xB3;
    else if(y < 40) page = 0xB4;
    else if(y < 48) page = 0xB5;
    else if(y < 56) page = 0xB6;
    else            page = 0xB7;

    add = x + OLED_OFFSET;
    lAddr = 0x0F & add;        
    hAddr = 0x10 | (add >> 4); 

    // Calculate mask 
    add = y >> 3;                   
    add <<= 3;                      
    add = y - add;                  
    mask = 1 << add;                

    _setAddr(page, lAddr, hAddr); 
    display = oled_read_byte();	
    display = oled_read_byte(); 
    display |= mask;            
    
    _setAddr(page, lAddr, hAddr); 
    oled_write_byte(display);   
}

/******************************************************************************/
// gets pixel color at x,y
BYTE oled_get_pixel(SHORT x, SHORT y) {
    BYTE    page, add, lAddr, hAddr;
    BYTE    mask, temp, display;

    // Assign a page address
    if(y < 8)       page = 0xB0;
    else if(y < 16) page = 0xB1;
    else if(y < 24) page = 0xB2;
    else if(y < 32) page = 0xB3;
    else if(y < 40) page = 0xB4;
    else if(y < 48) page = 0xB5;
    else if(y < 56) page = 0xB6;
    else            page = 0xB7;

    add = x + OLED_OFFSET;
    lAddr = 0x0F & add;             
    hAddr = 0x10 | (add >> 4);

    temp = y >> 3;                  
    temp <<= 3;                     
    temp = y - temp;                
    mask = 1 << temp;               

    _setAddr(page, lAddr, hAddr); 
    display = oled_read_byte();	
    display = oled_read_byte();

    return (display & mask);    	
}

/******************************************************************************/
// draw vertical line
void oled_drawVLine(BYTE a, BYTE b, BYTE x, BYTE y) {
    BYTE j;
    if ((a)>(b))
        for (j=(b)+1;j<=(a);j++)
            oled_put_pixel((x),(y)-j);
    else
        for (j=(a);j<=(b);j++)
            oled_put_pixel((x),(y)-j);
}

/******************************************************************************/
void oled_clearRect(BYTE c1, BYTE c2, BYTE x1, BYTE x2) {
    BYTE i,j;
    for(i=(c1);i<(c2);i++) {
        oled_cmd(i);
        oled_cmd(x1);
        oled_cmd(0x10);
        for(j=0;j<x2;j++)
            oled_write_byte(0x00);
    }
}

/******************************************************************************/
void oled_write_char(char letter, BYTE page, BYTE column)
{
	letter -= ' ';		// Adjust character to table that starts at 0x20
	oled_cmd(page);
	column += OLED_OFFSET;
	oled_cmd(0x00+(column&0x0F));
	oled_cmd(0x10+((column>>4)&0x0F));
	oled_write_byte(g_pucFont[letter][0]);	// Write first column
	oled_write_byte(g_pucFont[letter][1]);	// Write second column
	oled_write_byte(g_pucFont[letter][2]);	// Write third column
	oled_write_byte(g_pucFont[letter][3]);	// Write fourth column
	oled_write_byte(g_pucFont[letter][4]);	// Write fifth column
	oled_write_byte(0x00);	// Write 1 column for buffer to next character
}

/******************************************************************************/
void oled_put_ROMstr(rom char *ptr, BYTE page, BYTE col) {
    BYTE i=col;
    page = page + 0xB0;
    while(*ptr) {
        oled_write_char(*ptr,page,i);
        ptr++;
        i+=6;
    }
}

/******************************************************************************/
void oled_put_str(char *ptr,BYTE page, BYTE col) {
    BYTE i=col;
    page = page + 0xB0;
    while(*ptr) {
        oled_write_char(*ptr,page,i);
        ptr++;
        i+=6;
    }
}

/******************************************************************************/
// write an image to the display
void oled_put_img(rom BYTE *ptr, BYTE sizex,BYTE sizey,BYTE startx,BYTE starty){
    BYTE i,j;
    startx += OLED_OFFSET;
    for(i=0xB0+starty;i<(0xB0+sizey);i++) {
        oled_cmd(i);
        oled_cmd(startx&0x0F);
        oled_cmd(0x10 | ((startx>>4)&0x0F));

        for(j=0;j<sizex;j++)
            oled_write_byte(*ptr++);
    }
}

/******************************************************************************/
ROM BYTE g_pucFont[91][5] =
{
    { 0x00, 0x00, 0x00, 0x00, 0x00 }, // " " 0x20
    { 0x00, 0x00, 0x4f, 0x00, 0x00 }, // !   0x21
    { 0x00, 0x07, 0x00, 0x07, 0x00 }, // "   0x22
    { 0x14, 0x7f, 0x14, 0x7f, 0x14 }, // #   0x23
    { 0x24, 0x2a, 0x7f, 0x2a, 0x12 }, // $   0x24
    { 0x23, 0x13, 0x08, 0x64, 0x62 }, // %   0x25
    { 0x36, 0x49, 0x55, 0x22, 0x50 }, // &   0x26
    { 0x00, 0x05, 0x03, 0x00, 0x00 }, // '   0x27
    { 0x00, 0x1c, 0x22, 0x41, 0x00 }, // (   0x28
    { 0x00, 0x41, 0x22, 0x1c, 0x00 }, // )   0x29
    { 0x14, 0x08, 0x3e, 0x08, 0x14 }, // *   0x2A
    { 0x08, 0x08, 0x3e, 0x08, 0x08 }, // +   0x2B
    { 0x00, 0x50, 0x30, 0x00, 0x00 }, // ,   0x2C
    { 0x08, 0x08, 0x08, 0x08, 0x08 }, // -   0x2D
    { 0x00, 0x60, 0x60, 0x00, 0x00 }, // .   0x2E
    { 0x20, 0x10, 0x08, 0x04, 0x02 }, // /   0x2F
    { 0x3e, 0x51, 0x49, 0x45, 0x3e }, // 0   0x30
    { 0x00, 0x42, 0x7f, 0x40, 0x00 }, // 1   0x31
    { 0x42, 0x61, 0x51, 0x49, 0x46 }, // 2   0x32
    { 0x21, 0x41, 0x45, 0x4b, 0x31 }, // 3   0x33
    { 0x18, 0x14, 0x12, 0x7f, 0x10 }, // 4   0x34
    { 0x27, 0x45, 0x45, 0x45, 0x39 }, // 5   0x35
    { 0x3c, 0x4a, 0x49, 0x49, 0x30 }, // 6   0x36
    { 0x01, 0x71, 0x09, 0x05, 0x03 }, // 7   0x37
    { 0x36, 0x49, 0x49, 0x49, 0x36 }, // 8   0x38
    { 0x06, 0x49, 0x49, 0x29, 0x1e }, // 9   0x39
    { 0x00, 0x36, 0x36, 0x00, 0x00 }, // :   0x3A
    { 0x00, 0x56, 0x36, 0x00, 0x00 }, // ;   0x3B
    { 0x08, 0x14, 0x22, 0x41, 0x00 }, // <   0x3C
    { 0x14, 0x14, 0x14, 0x14, 0x14 }, // =   0x3D
    { 0x00, 0x41, 0x22, 0x14, 0x08 }, // >   0x3E
    { 0x02, 0x01, 0x51, 0x09, 0x06 }, // ?   0x3F
    { 0x32, 0x49, 0x79, 0x41, 0x3e }, // @   0x40
    { 0x7e, 0x11, 0x11, 0x11, 0x7e }, // A   0x41
    { 0x7f, 0x49, 0x49, 0x49, 0x36 }, // B   0x42
    { 0x3e, 0x41, 0x41, 0x41, 0x22 }, // C   0x43
    { 0x7f, 0x41, 0x41, 0x22, 0x1c }, // D   0x44
    { 0x7f, 0x49, 0x49, 0x49, 0x41 }, // E   0x45
    { 0x7f, 0x09, 0x09, 0x09, 0x01 }, // F   0x46
    { 0x3e, 0x41, 0x49, 0x49, 0x7a }, // G   0x47
    { 0x7f, 0x08, 0x08, 0x08, 0x7f }, // H   0x48
    { 0x00, 0x41, 0x7f, 0x41, 0x00 }, // I   0x49
    { 0x20, 0x40, 0x41, 0x3f, 0x01 }, // J   0x4A
    { 0x7f, 0x08, 0x14, 0x22, 0x41 }, // K   0x4B
    { 0x7f, 0x40, 0x40, 0x40, 0x40 }, // L   0x4C
    { 0x7f, 0x02, 0x0c, 0x02, 0x7f }, // M   0x4D
    { 0x7f, 0x04, 0x08, 0x10, 0x7f }, // N   0x4E
    { 0x3e, 0x41, 0x41, 0x41, 0x3e }, // O   0x4F
    { 0x7f, 0x09, 0x09, 0x09, 0x06 }, // P   0X50
    { 0x3e, 0x41, 0x51, 0x21, 0x5e }, // Q   0X51
    { 0x7f, 0x09, 0x19, 0x29, 0x46 }, // R   0X52
    { 0x46, 0x49, 0x49, 0x49, 0x31 }, // S   0X53
    { 0x01, 0x01, 0x7f, 0x01, 0x01 }, // T   0X54
    { 0x3f, 0x40, 0x40, 0x40, 0x3f }, // U   0X55
    { 0x1f, 0x20, 0x40, 0x20, 0x1f }, // V   0X56
    { 0x3f, 0x40, 0x38, 0x40, 0x3f }, // W   0X57
    { 0x63, 0x14, 0x08, 0x14, 0x63 }, // X   0X58
    { 0x07, 0x08, 0x70, 0x08, 0x07 }, // Y   0X59
    { 0x61, 0x51, 0x49, 0x45, 0x43 }, // Z   0X5A
    { 0x00, 0x7f, 0x41, 0x41, 0x00 }, // [   0X5B
    { 0x02, 0x04, 0x08, 0x10, 0x20 }, // "\" 0X5C
    { 0x00, 0x41, 0x41, 0x7f, 0x00 }, // ]   0X5D
    { 0x04, 0x02, 0x01, 0x02, 0x04 }, // ^   0X5E
    { 0x40, 0x40, 0x40, 0x40, 0x40 }, // _   0X5F
    { 0x00, 0x01, 0x02, 0x04, 0x00 }, // `   0X60
    { 0x20, 0x54, 0x54, 0x54, 0x78 }, // a   0X61
    { 0x7f, 0x48, 0x44, 0x44, 0x38 }, // b   0X62
    { 0x38, 0x44, 0x44, 0x44, 0x20 }, // c   0X63
    { 0x38, 0x44, 0x44, 0x48, 0x7f }, // d   0X64
    { 0x38, 0x54, 0x54, 0x54, 0x18 }, // e   0X65
    { 0x08, 0x7e, 0x09, 0x01, 0x02 }, // f   0X66
    { 0x0c, 0x52, 0x52, 0x52, 0x3e }, // g   0X67
    { 0x7f, 0x08, 0x04, 0x04, 0x78 }, // h   0X68
    { 0x00, 0x44, 0x7d, 0x40, 0x00 }, // i   0X69
    { 0x20, 0x40, 0x44, 0x3d, 0x00 }, // j   0X6A
    { 0x7f, 0x10, 0x28, 0x44, 0x00 }, // k   0X6B
    { 0x00, 0x41, 0x7f, 0x40, 0x00 }, // l   0X6C
    { 0x7c, 0x04, 0x18, 0x04, 0x78 }, // m   0X6D
    { 0x7c, 0x08, 0x04, 0x04, 0x78 }, // n   0X6E
    { 0x38, 0x44, 0x44, 0x44, 0x38 }, // o   0X6F
    { 0x7c, 0x14, 0x14, 0x14, 0x08 }, // p   0X70
    { 0x08, 0x14, 0x14, 0x18, 0x7c }, // q   0X71
    { 0x7c, 0x08, 0x04, 0x04, 0x08 }, // r   0X72
    { 0x48, 0x54, 0x54, 0x54, 0x20 }, // s   0X73
    { 0x04, 0x3f, 0x44, 0x40, 0x20 }, // t   0X74
    { 0x3c, 0x40, 0x40, 0x20, 0x7c }, // u   0X75
    { 0x1c, 0x20, 0x40, 0x20, 0x1c }, // v   0X76
    { 0x3c, 0x40, 0x30, 0x40, 0x3c }, // w   0X77
    { 0x44, 0x28, 0x10, 0x28, 0x44 }, // x   0X78
    { 0x0c, 0x50, 0x50, 0x50, 0x3c }, // y   0X79
    { 0x44, 0x64, 0x54, 0x4c, 0x44 }  // z   0X7A
};