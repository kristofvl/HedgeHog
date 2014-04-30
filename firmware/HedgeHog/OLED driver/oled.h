/*******************************************************************************
 FileName:     	oled.h
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog OLED or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#ifndef OLED_H
#define OLED_H

/******** Include files *******************************************************/
#include "Compiler.h"
#include "GenericTypeDefs.h"
#include "HardwareProfile.h"
#include "delays.h"	
/******************************************************************************/


#define OLEDREG_SETDISPSTART 	0x40
#define OLEDREG_CONTRASTCTRL 	0x81
#define OLEDREG_EDISP_ON    	0xA4
#define OLEDREG_EDISP_OFF    	0xA5
#define OLEDREG_DISPLAY_OFF    	0xAE
#define OLEDREG_DISPLAY_ON    	0xAF
#define OLEDREG_SETVCOMDESL 	0xDB
#define OLEDREG_SETPRECHARGE 	0xD9

// default defines for the SPI configuration (PIC18F devkit):
#define	oledWR			LATEbits.LATE1
#define	oledWR_TRIS		TRISEbits.TRISE1
#define	oledRD			LATEbits.LATE0
#define	oledRD_TRIS		TRISEbits.TRISE0
#define	oledCS			LATEbits.LATE2
#define	oledCS_TRIS		TRISEbits.TRISE2
#define	oledRESET		LATDbits.LATD1
#define	oledRESET_TRIS          TRISDbits.TRISD1
#define	oledD_C			LATBbits.LATB5
#define	oledD_C_TRIS            TRISBbits.TRISB5
#define RST_TRIS_BIT            TRISDbits.TRISD2
#define RST_LAT_BIT             LATDbits.LATD2

//Sets page, lower and higher address pointer of display buffer
#define _setAddr(pge,lAdr,hAdr) {oled_cmd(pge);oled_cmd(lAdr);oled_cmd(hAdr);}
#define IsDeviceBusy()  0
#define OLED_OFFSET	2
#define oled_max_x() (SCREEN_HOR_SIZE-1)
#define oled_max_y() (SCREEN_VER_SIZE-1)

/******************************************************************************/
void oled_init(void);
void oled_reset(void);
void oled_cmd(BYTE cmd);
void oled_write_byte(BYTE data);
BYTE oled_read_byte();
void oled_fill(BYTE data);

void oled_put_pixel(SHORT x, SHORT y);
BYTE oled_get_pixel(SHORT x, SHORT y);
void oled_drawVLine(BYTE a, BYTE b, BYTE x, BYTE y);

void oled_clearRect(BYTE c1, BYTE c2, BYTE x1, BYTE x2);
void oled_put_img(rom BYTE *ptr, BYTE sizex,BYTE sizey,BYTE startx,BYTE starty);

void oled_put_str(char *ptr,BYTE page, BYTE col);
void oled_put_ROMstr(rom char *ptr, BYTE page, BYTE col);

/*********************************************/
extern ROM BYTE g_pucFont[91][5];
/*********************************************/




#endif // OLED_H
