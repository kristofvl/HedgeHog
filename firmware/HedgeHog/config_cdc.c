/*******************************************************************************
 FileName:     	config_cdc.c
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#include "config_cdc.h"

/******************************************************************************/
const rom char msg_ok[]    = "ok";
const rom char msg_eol[]   = "\r\n";
const rom char msg_help[]  = "Available commands: {t,r,s,v,?,f,d,i,u,w}";
const rom char msg_refat[] = "Restoring FAT...";
const rom char msg_log[]   = "Logging mode - byebye";

/******************************************************************************/
static char USB_Buffer[62] = {0};


void config_cdc_init(void) {
    config_cycle = config_mode = 0;
}

void up_cdc_cycle(void) {
    if (config_cycle)       // if we're in a configuration cycle, move on
        config_cycle--;
    else config_mode = 0;   // else make sure we return to the main menu
}

BYTE cdc_config_cmd(BYTE c) {
    if (config_mode==c) return 1;
    else                return 0;
}

void cdc_main_menu( rom char* name_str, rom char* ver_str)
{
    char uart_c;
    if (mUSBUSARTIsTxTrfReady()) {
        if (getsUSBUSART(&uart_c, 1) != 0) {
            switch (uart_c) {
                case 't': cdc_start_set_time(); break;
                case 'T': cdc_start_stop_time(); break;
                case 'r': cdc_start_read(); break;
                case 's': cdc_start_log(); break;
                case 'v': cdc_print_ver(name_str,  ver_str); break;
                case '?': cdc_print_help(); break;
                case 'f': cdc_start_format(); break;
                case 'i': cdc_start_init(); break;
                case 'u': cdc_start_conf_read(); break;
                case 'w': cdc_start_conf_write(); break;
            } // switch
        } // if numBytesRead!=0
    } // if (mUSBUSARTIsTxTrfReady)
}

/******************************************************************************/
void cdc_print_ver(rom char* name_str, rom char* ver_str)
{
    char i;
    for (i = 0; i < 8; i++)
        USB_Buffer[i] = name_str[i];
    USB_Buffer[8] = ' ';
    for (i = 9; i < 16; i++)
        USB_Buffer[i] = ver_str[i - 9];
    putUSBUSART(USB_Buffer, 16); 
}

/******************************************************************************/
void cdc_print_help(void)
{
    putrsUSBUSART( msg_help );
}

/******************************************************************************/
void cdc_print_init(UINT32_VAL msg)
{
    sprintf(USB_Buffer, "init: %02x %02x %02x",
                        (msg.v[0]), (msg.v[1]), (msg.v[2]));
    USB_Buffer[14] = 0;
    putUSBUSART(USB_Buffer, 15);
}

/******************************************************************************/
void cdc_print_all(BYTE x,BYTE y,BYTE z,UINT16 l,BYTE t,char* dstr,char* tstr)
{
    sprintf(USB_Buffer,"acc[%03d,%03d,%03d] lgt[%04u] tmp[%03d] clk[%s,%s]",
            x, y, z, l, t, dstr, tstr);
    USB_Buffer[61] = 0;
    putUSBUSART(USB_Buffer, 62);
}

/******************************************************************************/
void cdc_write_ok(void) {
    putrsUSBUSART(msg_ok);
}

/******************************************************************************/
void cdc_eol(void) {
    putrsUSBUSART(msg_eol);
}

/******************************************************************************/
void cdc_write_refat(void) {
    putrsUSBUSART(msg_refat); 
}

/******************************************************************************/
void cdc_write_log(void) {
    putrsUSBUSART(msg_log); 
}

/******************************************************************************/
void cdc_write_conf(char* cstr) {
    putsUSBUSART(cstr);
    config_cycle = 0;
}

/******************************************************************************/
BYTE cdc_get_conf(char *confstr, BYTE conflen)
{
    char uart_c;
    if (mUSBUSARTIsTxTrfReady()) {
        if (getsUSBUSART(&uart_c, 1) != 0) {
            if ((config_cycle>0) && (config_cycle<=conflen)) {
                confstr[conflen-config_cycle] = uart_c;
            }
            config_cycle--; // advance to next state
            if (config_cycle == 0)
                return 1; // do more after this function returns..
        } // if numBytesRead
    }
    config_cycle++; // correct for inactive cdc loops in up_cdc_cycle();
    return 0;
}

/******************************************************************************/