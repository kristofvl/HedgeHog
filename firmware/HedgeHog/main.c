/*******************************************************************************
 FileName:     	main.h,     the HedgeHog Operating System
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

rom char HH_NAME_STR[9] = {'H', 'e', 'd', 'g', 'e', 'H', 'o', 'g', 0};
rom char HH_VER_STR[8]  = {'v', '.', '1', '.', '1', '9', '0', 0};

/******************************************************************************/
char is_logging; // needs to be defined before SD-SPI.h -> GetInstructionClock

/** INCLUDES ******************************************************************/

#include "USB/usb.h"				// USB stack, USB_INTERRUPT
#include "HardwareProfile.h"			// Hardware design wrapper
#include "sensor_wrapper.h"			// all sensors 
#include "USB/usb_function_msd.h"		// Mass storage over USB
#include "SD_Buffer.h"
#include "SD_FAT.h"				// SD card FAT tables
#include "RTC/rtcc.h"				// RTC functions
#include "osc.h"
#include "delays.h"
#include "HHG_conf.h"
#include "config_cdc.h"
// timeouts (eg logstart)
// Soft Start Circuit:
#if defined(SOFTSTART_ENABLED)
#include "./Soft Start/soft_start.h"            // controls soft start
#endif
// OLED driver:
#if defined(DISPLAY_ENABLED)
#include "display_config.h"			// OLED display defines
#endif

/** CONFIGURATION *************************************************************/
#pragma config WDTEN = OFF          //WDT disabled
#pragma config PLLDIV = 3           //Divide by 3 (12 MHz)
#pragma config STVREN = ON          //Stack over/underflow reset
#pragma config XINST = OFF          //Extended instruction set 
#pragma config CPUDIV = OSC1        //No CPU system clock divide
#pragma config CP0 = OFF            //Program not code-protected
#pragma config OSC = HSPLL          //HS oscillator, PLL, 
#pragma config FCMEN = OFF          //Fail-Safe Clock Monitor 
#pragma config IESO = OFF           //Two-Speed Start-up
#pragma config WDTPS = 32768        //1:32768
#pragma config DSWDTOSC = INTOSCREF //DSWDT clock
#pragma config RTCOSC = T1OSCREF    //RTCC clock <- 32kH crystal
#pragma config DSBOREN = OFF        //Deep Sleep Zero-Power BOR
#pragma config DSWDTEN = OFF        //Disabled
#pragma config DSWDTPS = 8192       //1:8,192 (8.5 seconds)
#pragma config IOL1WAY = OFF        //IOLOCK can be set/cleared
#pragma config MSSP7B_EN = MSK7     //7 Bit address masking
#pragma config WPFP = PAGE_1        //Write Protect Program 
#pragma config WPEND = PAGE_0       //Start protection 
#pragma config WPCFG = OFF          //Write/Erase last page 
#pragma config WPDIS = OFF          //no WPFP[5:0],WPEND,WPCFG
#pragma config T1DIG = ON           //Sec Osc clock source
#pragma config LPT1OSC = OFF        //no high power Timer1

/** VARIABLES *****************************************************************/
#pragma udata

sd_buffer_t sd_buffer;

hhg_conf_t hhg_conf;

// time variables
rtccTimeDate tm; // variable holding time info
char date_str[11];
char time_str[9];

// sensor variables:
WORD_VAL light;
UINT8 thermo = 21;
ACC_XYZ accval; // variable for current acceleration readings
char acc_str[12];
char lt_str[4];
char tmp_str[4];

// config variables:
UINT16 config_cycle = 0;

/** CONSTANTS *****************************************************************/
/* Standard Response to INQUIRY command stored in ROM 	*/
const ROM InquiryResponse inq_resp = {
    0x00, // peripheral device connected, direct access block
    0x80, // removable
    0x04, // version = 04 => SPC-2
    0x02, // response is in format specified by SPC-2
    0x20, // n-4 = 36-4=32= 0x20
    0x00, // sccs etc.
    0x00, // other device -> using 00
    0x00, // 00 obsolete, 0x80 for basic task queueing
    {'E','S','S',' ','T','U','D','.'},
    {'M','a','s','s',' ','S','t','o','r','a','g','e',' ',' ',' ',' '},
    {'0', '0', '0', '1'}
};

/** PRIVATE PROTOTYPES ********************************************************/
#include "USBCallbacks.c"                   // USB bus comms implementations
void high_priority_ISR(void);               // interrupt service routines
void low_priority_ISR(void);
static void init_system(void);
void process_IO(void);
void update_display(void);
void user_init(void);
void log_process(void);
void config_process(void);

/** VECTOR REMAPPING **********************************************************/
#pragma code REMAPPED_HIGH_INTERRUPT_VECTOR = 0x08
void remapped_high_ISR(void) {
    _asm goto high_priority_ISR _endasm
}
#pragma code REMAPPED_LOW_INTERRUPT_VECTOR = 0x18
void remapped_low_ISR(void) {
    _asm goto low_priority_ISR _endasm
}
#pragma code	
//These are the actual interrupt handling routines.
#pragma interrupt high_priority_ISR
void high_priority_ISR() {
    if (PIE1bits.TMR1IE && PIR1bits.TMR1IF) { // timer1 int?
        PIE1bits.TMR1IE = 0;
        PIR1bits.TMR1IF = 0;
        T1CONbits.TMR1ON = 0; // turn timer 1 off
    } else {
        USBDeviceTasks();
    }
} //return is a "retfie fast", since this is in a #pragma interrupt section
#pragma interruptlow low_priority_ISR
void low_priority_ISR() {
    //Check which interrupt flag caused the interrupt, Service & Clear
} // return is a "retfie", since this is in a #pragma interruptlow section


/** DECLARATIONS **************************************************************/
#pragma code

/*******************************************************************************
 * Function:        void main(void)
 *
 * Overview:        Main program entry point.
 ******************************************************************************/
void main(void) {
    init_system();
    USBDeviceAttach();
    while (1) {
        process_IO(); // Application tasks: logging, configuring
    }
}

/*******************************************************************************
 * Function:        static void init_system(void)
 *
 * Overview:        InitializeSystem is a centralized initialization
 *                  routine. All required USB initialization routines
 *                  and user init routines are called from here.
 ******************************************************************************/
static void init_system(void) {
    set_osc_48Mhz();

    //Configure all I/O pins to use digital input buffers.
    ANCON0 = ANCON1 = 0xFF; // Default all pins to digital
    
    //Configure interrupts:
    RCONbits.IPEN = 1; // Enable Interrupt Priority levels
    INTCONbits.GIEH = 1; // Enable High-priority Interrupts
    INTCONbits.GIEL = 0; // Disable Low-priority Interrupts

#if defined(USE_USB_BUS_SENSE_IO)
    tris_usb_bus_sense = INPUT_PIN; // See HardwareProfile.h
#endif

#if defined(USE_SELF_POWER_SENSE_IO)
    tris_self_power = INPUT_PIN; // See HardwareProfile.h
#endif

    remap_pins();           // remap IO and INT pins
    USBDeviceInit();        // usb_device.c

    #if defined(DISPLAY_ENABLED)
    oled_init();
    #endif

    INTCON2bits.RBPU = 0; // enable a pull-up on PortB
    MDD_SDSPI_InitIO(); // SD-SPI.c

    user_init(); // Our init routines come last
}

/*******************************************************************************
 * Function:        void user_init(void)
 *
 * Overview:        This routine should take care of all of the 
 *                  application's code initialization.
 ******************************************************************************/
void user_init(void) {
    UINT16 i;

    // turn on the led to signify booting:
    #if defined(led_pin)
    led_init();
    led_on();
    #endif

    // wait a bit till all systems are powered
    Delay10KTCYx(250); Delay10KTCYx(250);
    Delay10KTCYx(250); Delay10KTCYx(250);

    // get the configuration:
    read_HHG_conf(&hhg_conf);

    rtcc_init(); // Set clock to:
    rtcc_write(&tm); // update time
    rtcc_writestr(&tm, date_str, time_str); // write time

    init_env(); // set up environment sensors (light, temp, ...)

    // Setup accelerometer interrupt
    //INTCON3bits.INT1IP = 1; // high priority int1
    //INTCON3bits.INT1IF = 0;
    //INTCON3bits.INT1IE = 1;

    #if defined(DISPLAY_ENABLED)
    disp_init();
    #endif

    SD_CS_TRIS = OUTPUT_PIN; // un-select SD-card
    LATCbits.LATC6 = 1;
    SD_CS = 1;

    ACC_CS_TRIS = OUTPUT_PIN; // un-select accelerometer
    ACC_CS = 1;
    PORTCbits.RC7 = 1;

    // By default, start in configuration mode:
    is_logging = 0;

    // initialize configuration state variables:
    config_cdc_init();

    // initialize the constant symbols in the display strings:
    time_str[2] = time_str[5] = ':'; time_str[8] = 0;
    date_str[2] = date_str[5] = '/'; date_str[6] = '2'; date_str[7] = '0';
    date_str[10] = 0;

    // turn off the led: done booting:
    #if defined(led_pin)
    led_off();
    #endif
}

/*******************************************************************************
 * Function:        void ProcessIO(void)
 *
 * Overview:        This function runs all basic application tasks
 ******************************************************************************/
void process_IO(void) {
    #if defined(SOFTSTART_ENABLED)
    if (AppPowerReady() == FALSE) return; // Soft Start APP_VDD
    #endif

    update_display(); // Update routine for the display

    if (is_logging)
        log_process(); // go to the logging process
    else {
        if ((USBDeviceState < CONFIGURED_STATE) || (USBSuspendControl == 1))
            return;
        CDCTxService();     // CDC transimssion tasks
        MSDTasks();         // mass storage device tasks
        config_process();   // CDC configuration tasks
    }
}

/*******************************************************************************
 * Function:        void update_display(void)
 *
 * Overview:        Handles screen update commands and refreshes,
 *                  using the disp_cmd, disp_mode, and disp_cycle variables
 ******************************************************************************/
void update_display(void) {
#if defined(DISPLAY_ENABLED)
    up_dispcycle(); 
    if (is_logging) { // in logging mode:
        // user interaction? => switch mode:
        if (button_pressed) {
            button_clear();
            disp_user_log_toggle();
        }
        if (disp_update_log_time()) // refresh display:
            rtcc_writestr(&tm, date_str, time_str);
    } else { // in config mode:
        // user interaction? => switch mode:
        if (button_pressed) {
            button_clear();
            disp_user_conf_toggle();
        }
        // prepare to refresh display:
        if (disp_update_time()) {
            rtcc_writestr(&tm, date_str, time_str);
        }
        else if (disp_update_env()) {
            read_env(light, thermo);
            write2str(light.Val, lt_str);
            write2str(((thermo/2)-30), tmp_str);
        }
        else if (disp_update_accl()) {
            acc_write_string(&accval, acc_str);
        }
        else if (disp_update_init()) {
            acc_init(hhg_conf.cs.acc_s,&(hhg_conf.cs.acc));
        }
    }
    // execute possible commands to the display update routine:
    if (disp_refresh()==DISP_CMD_ACCUP)
        disp_acc_update(&accval, acc_str);
    else if (disp_refresh()==DISP_CMD_LGTMP)
        disp_env_update( (BYTE)(((light.Val>950)?950:light.Val)>>5),
                lt_str, tmp_str);
    else if (disp_refresh()==DISP_CMD_CLOCK)
        disp_time_update(date_str, time_str);
    else if (disp_refresh()==DISP_CMD_INTRO)
        disp_init_intro(HH_NAME_STR, HH_VER_STR);
#endif // DISPLAY_ENABLED
}

/*******************************************************************************
 * Function:        void log_process(void)
 *
 * Overview:        Does the logging to SD card per page
 *                  no matter what type of logging, the first 8 bytes per page
 *                  are header, the other 504 are data increments
 ******************************************************************************/
void log_process() {
    static BOOL startup = 0; // startup after a while
    if (startup == 0) { // to init light sensors, accelerometer & SD card
        USBSoftDetach();    // detach usb module
        Delay10KTCYx(250);
        set_osc_8Mhz();
        startup = TRUE;
        init_env();
        acc_init(hhg_conf.cs.acc_s,&(hhg_conf.cs.acc));
        #if defined(DISPLAY_ENABLED)
        disp_start_log();
        #endif
        sdbuf_init();
        return;
    }
    if (sdbuf_is_onhold()) { // log time stamp and env data in first 8 bytes
        read_env(light, thermo); // read time stamp and light (env) value
        sd_buffer.f.envdata  = ((light.Val>>3)<<8) | (thermo);
        rtcc_read(&tm);
        sd_buffer.f.timestmp = rtcc_2uint32(&tm);
        sdbuf_init_buffer();
        return;
    }
    if (sdbuf_notfull()) { // log acc data (RLE)
        acc_getxyz(&accval);
        if (!sdbuf_is_new_accslot()) {         // if we are not in a new slot,
            if (sdbuf_check_rle(&accval, 2)) { // and if different acc values
                sdbuf_goto_next_accslot();     // then go to the next slot
            }
        }
        if (sdbuf_notfull()) {
            sdbuf_add_acc(&accval); // add/overwrite the new sensor values
            set_osc_sleep_t1(37);   // go to sleep for timeout of 8ms
        }
        if (sdbuf_deltaT_full())
            sdbuf_goto_next_accslot();
    }
    if (sdbuf_full()) { // write log to page
        #if defined(DISPLAY_ENABLED)
        disp_log_subdue();  // switch off the display if it is on
        #endif
        sdbuf_write(); // write to SD card and update counters
        #if defined(DISPLAY_ENABLED)
        disp_log_revive();
        #endif
        return; // return to IOProcess
    }
}

/*******************************************************************************
 * Function:        void config_process(void)
 *
 * Overview:        Setting the HedgeHog's configuration via serial
 ******************************************************************************/
void config_process(void) {
    char uart_c;
    UINT16 file_i, clustp; // used in writing the FAT root table

    if (cdc_config_cmd(0))  cdc_main_menu( HH_NAME_STR, HH_VER_STR );
    else if (cdc_config_cmd('i')) {
        switch (config_cycle) {
            case 100: rtcc_init(); break;
            #if defined(DISPLAY_ENABLED)
            case 90: disp_start_usb(); break;
            #endif
            case 80:  acc_init(hhg_conf.cs.acc_s, &(hhg_conf.cs.acc)); break;
            case 50:  cdc_print_init(hhg_conf.cs.acc); break;
            case 10:  cdc_eol(); break;
        }
    }
    else if (cdc_config_cmd('t')) { // read time from host
        if (cdc_get_conf((char*)tm.b,6)) {
            tm.b[7]=tm.b[4]; tm.b[6]=tm.b[5]; tm.b[4]=tm.b[3]; tm.b[3]=tm.b[1]; 
            rtcc_write(&tm);
            rtcc_writestr(&tm,date_str,time_str);
            cdc_write_ok();
        }
    }
    else if (cdc_config_cmd('r')) {
        switch (config_cycle) {
            case 100: acc_getxyz(&accval);  env_on();  break;
            case 80: light = read_light();  env_off(); break;
            case 70: rtcc_writestr(&tm,date_str,time_str); break;
            case 50: cdc_print_all( accval.x, accval.y, accval.z,
                light.Val,thermo,(char*)date_str,(char*)time_str);
                break;
            case 10: cdc_eol(); break;
        }
    }
    else if (cdc_config_cmd('s')) {
        switch (config_cycle) {
            case 10: cdc_write_log(); break;
            case 5: // USBSoftDetach();
                #if defined(DISPLAY_ENABLED)
                disp_cmd = DISP_CMD_LOGNG;
                #endif
                break;
            case 1: is_logging = 1; break;
        }
    }
    else if (cdc_config_cmd('f')) {
        if ((config_cycle>70)&&(config_cycle<170)) {
            if (config_cycle%10==0) {
                write_FAT(&sd_buffer,(config_cycle/10)-8);
                write_SD( config_cycle/10, sd_buffer.bytes);
            }
        }
        switch (config_cycle) {
            case 230: write_MBR(&sd_buffer); break; // (sector 1)
            case 220: MDD_SDSPI_SectorWrite(0, sd_buffer.bytes, 1); break;
            case 210: write_root_table(&sd_buffer);    break; 
            case 200: write_SD(480, sd_buffer.bytes);  break; 
            case 15:  write_FAT(&sd_buffer,9); close_FAT(&sd_buffer); break;
            case 10:  write_SD(17, sd_buffer.bytes);  break;
            case 1:   cdc_write_ok(); break;
        }
    }
    else if (cdc_config_cmd('u')) {
        read_HHG_conf(&hhg_conf);
        cdc_write_conf(hhg_conf.cstr);
    }
    else if (cdc_config_cmd('w')) { // read configuration from cdc
        if (cdc_get_conf(hhg_conf.cstr,20)) {
            hhg_conf.cstr[20] = 0;
            write_HHG_conf(hhg_conf);
            cdc_write_ok();
        }
    }
    up_cdc_cycle();
}
/******************************************************************************/
