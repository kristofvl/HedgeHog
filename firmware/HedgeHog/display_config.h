/*******************************************************************************
 FileName:     	display_config.c
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog OLED or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#ifndef DISP_CONF_H
#define DISP_CONF_H

#include "porclogo.h"				// the logo bitmap
#include "porc_watchfont.h"			// the watch bitmap
#include "OLED driver/oled.h"			// OLED driver
#include "acc3D_wrapper.h"

#define PORCWF_X  28
#define PORCPIC_X 51

// the possible display modes:
typedef enum {
    DISP_MODE_INIT = 0x00,
    DISP_MODE_USBC = 0x03,
    DISP_MODE_ACCL = 0xA0,
    DISP_MODE_LGHT = 0xA1,
    DISP_MODE_TIME = 0xA2,
    DISP_MODE_LOGG = 0xA3
} DISP_MODE;

// current status of the display:
typedef enum {
    DISP_CMD_INTRO = 0x01,
    DISP_CMD_LOGNG = 0x02,
    DISP_CMD_ERRLG = 0x05,
    DISP_CMD_CLOCK = 0x17,
    DISP_CMD_LGTMP = 0x18,
    DISP_CMD_ACCUP = 0x19,
    DISP_CMD_IUSBC = 0x71
} DISP_CMD;


// cycle variables for display:
#define MAX_DISPCYCLE 9000
#define DISP_CYCLE_1STICKS 100

static DISP_MODE disp_mode = 0;
static DISP_CMD disp_cmd = 0; 
static UINT16 disp_cycle;

#define DISP_PLOTWINSIZE 60
static ACC_XYZ abuf[DISP_PLOTWINSIZE];
static BYTE    lbuf[DISP_PLOTWINSIZE];

#define _oledw(s,x,y) oled_put_ROMstr((rom char*)s,x,y)
#define _oleds(s,x,y) oled_put_str(s,x,y)
#define _oledi(i,xx,x,y) oled_put_img(i, xx, x, y, 0)

/******************************************************************************/
void up_dispcycle(void);
void disp_init(void);
void disp_acc_init(void);
void disp_time_init(void);
void disp_env_init(void);
void disp_USB_init(void);
void disp_init_intro(rom char* n, rom char* v);
void disp_acc_update(PACC_XYZ accval, char* acc_str);
void disp_env_update(BYTE lgt_val, char* l_str, char* t_str);
void disp_time_update(char* dstr, char* tstr);
BYTE disp_update_time(void);
BYTE disp_update_env(void);
BYTE disp_update_accl(void);
BYTE disp_update_init(void);
BYTE disp_update_log_time(void);
void disp_user_conf_toggle(void);
void disp_user_log_toggle(void);
DISP_CMD disp_refresh(void);

void disp_start_log(void);
void disp_start_usb(void);

void disp_log_subdue(void);
void disp_log_revive(void);
/******************************************************************************/


/******************************************************************************/
extern rom BYTE porcpic[408];
extern rom BYTE bmp[10][140];
/******************************************************************************/

#endif // DISP_CONF_H
