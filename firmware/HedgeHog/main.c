/*******************************************************************************
 FileName:     	main.h,     the HedgeHog Operating System
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

rom char HH_NAME_STR[9] = {'H', 'e', 'd', 'g', 'e', 'H', 'o', 'g', 0};
rom char HH_VER_STR[8]  = {'v', '.', '1', '.', '2', '0', '0', 0};

/******************************************************************************/
char is_logging; // needs to be defined before SD-SPI.h -> GetInstructionClock

/** INCLUDES ******************************************************************/
#include "USB/usb.h"				// USB stack, USB_INTERRUPT
#include "HardwareProfile.h"			// Hardware design wrapper
#include "dsleep_alarm.h"
#include "sensor_wrapper.h"			// all sensors 
#include "USB/usb_function_msd.h"		// Mass storage over USB
#include "SD_Buffer.h"
#include "SD_FAT.h"				// SD card FAT tables
#include "RTC/rtc.h"				// RTC functions
#include "osc.h"
#include "delays.h"
#include "HHG_conf.h"
#include "config_cdc.h"

#if defined(SOFTSTART_ENABLED)
#include "./Soft Start/soft_start.h"            // controls soft start
#endif
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
rtc_timedate tm; //  holding time info for current time
char date_str[11] = "01/01/2012";
char time_str[9] = "00:00:00";
UINT32 tm_stop;

// sensor variables:
WORD_VAL light;
UINT8 thermo = 21;
ACC_XYZ accval; // variable for current acceleration readings
char acc_str[12];
char lt_str[4];
char tmp_str[4];
BOOL usbp_int;

// config variables:
UINT16 config_cycle = 0;
UINT8 rle_delta = 0;

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
// interrupt handling routines:
#pragma interrupt high_priority_ISR
void high_priority_ISR() {
    if (PIE1bits.TMR1IE && PIR1bits.TMR1IF) { // handle timer1 interrupts
        PIE1bits.TMR1IE = 0;  // turn interrupt t1 off
        PIR1bits.TMR1IF = 0;
        T1CONbits.TMR1ON = 0; // turn timer 1 off
    } else
    #if defined(ADXL345_ENABLED)
    if (INTCON3bits.INT1IE && INTCON3bits.INT1IF) { // handle INT1 interrupts
        INTCON3bits.INT1IE = 0; // turn interrupt in1 off
    } else
    #endif
    {
        USBDeviceTasks();
    }
}
#pragma interruptlow low_priority_ISR
void low_priority_ISR() {
}

/** DECLARATIONS **************************************************************/
#pragma code

/*******************************************************************************
 * Function:        void main(void)
 *
 * Overview:        Main program entry point.
 ******************************************************************************/
void main(void) {
    wakeup_check(&tm, 2); // wake up and check every 2 seconds for USB presence
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

    ANCON0 = ANCON1 = 0xFF; // Default all pins to digital
    set_unused_pins_to_output();
    
    //Configure interrupts:
    RCONbits.IPEN   = 1;    // Enable  Interrupt Priority levels
    INTCONbits.GIEH = 1;    // Enable  High-priority Interrupts
    INTCONbits.GIEL = 0;    // Disable Low-priority Interrupts

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

    // wait 5,000,000 ticks till SD card is powered
    Delay10KTCYx(250); Delay10KTCYx(250);
    sdbuf_init();

    user_init(); // Our other init routines come last
}

/*******************************************************************************
 * Function:        void user_init(void)
 *
 * Overview:        This routine should take care of all of the 
 *                  application's code initialization.
 ******************************************************************************/
void user_init(void) {
    
    // By default, start in configuration mode
    is_logging = 0;

    // read HedgeHog configuration structure
    read_HHG_conf(&hhg_conf);

    // wait 5,000,000 ticks till system is powered
    Delay10KTCYx(250); Delay10KTCYx(250);
    
    rtc_init();         // init clock
    acc_deep_sleep();   // put accelerometer to sleep for now
    env_init();         // set up environment sensors (light, temp, ...)
    
    #if defined(DISPLAY_ENABLED)
    Delay10KTCYx(250);Delay10KTCYx(250);
    disp_init();
    #endif

    config_cdc_init();          // init configuration state variables (counters)
    rtc_set_timeout_s(&tm, 5);  // set alarm after 5 seconds (to check USB)
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

    update_display();       // Update routine for the display

    if (is_logging)
        log_process();      // go to the logging process
    else {
        if ((USBDeviceState < CONFIGURED_STATE) || (USBSuspendControl == 1))
            if (!rtc_alrm())
               goto_deep_sleep(&tm, 3); // sleep for a while (3 seconds)
            else
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
        if (button_pressed) { // user interaction? => switch mode:
            button_clear();
            disp_user_log_toggle();
        }
        if (disp_update_log_time()) // refresh display:
            rtc_writestr(&tm, date_str, time_str);
    } else { // in config mode:
        // user interaction? => switch mode:
        if (button_pressed) {
            button_clear();
            disp_user_conf_toggle();
        }
        // prepare to refresh display:
        if (disp_update_time()) {
            rtc_writestr(&tm, date_str, time_str);
        }
        else if (disp_update_env()) {
            env_read(light, thermo);
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
        Delay10KTCYx(250);
        set_osc_8Mhz();
        startup = TRUE;
        TRISB=TRISC=TRISD=0; // default all pins to digital output
        usbp_int = 0;
        #if defined(ADXL345_ENABLED)
        ACC_INT = 0; // pull down B2
        USBP_INT_TRIS = INPUT_PIN; // set USB Power interrupt pin 
        usbp_int = !(USBP_INT);
        #endif
        sdbuf_init(); 
        read_HHG_conf(&hhg_conf); // read HedgeHog configuration structure
        rle_delta = hhg_conf.cs.acc.v[0] - 48; // extract from config string
        env_init();                                     //
        acc_init(hhg_conf.cs.acc_s,&(hhg_conf.cs.acc)); //- init all sensors
        #if defined(DISPLAY_ENABLED)
        disp_start_log();
        #endif
        #if defined(HEDGEHOG_OLED)
        adxl345_conf_tap(0x09, 0xA0, 0x72, 0x30, 0xFF); // configure double tap
        #endif
        return;
    }
    if (sdbuf_is_onhold()) { // log time stamp and env data in first 8 bytes
        if (usbp_int) {
            if (sdbuf_page()>5) {   // we assume here that the user needs a
                #if defined(USBP_INT)
                if (USBP_INT==0)    // while (5 page writes) to plug usb back in
                    goto_deep_sleep(&tm, 1); // go for a second in deep sleep
                #endif
            }
        }
        env_on(); // pull down power pin for light, do something else:
        rtc_read(&tm);
        sd_buffer.f.timestmp = rtc_2uint32(&tm);
        env_read(light, thermo); // read time stamp and light (env) value
        sd_buffer.f.envdata  = ((light.Val>>3)<<8) | (thermo); 
        sdbuf_init_buffer();
        if (sd_buffer.f.timestmp > tm_stop) { // go into shutdown mode
            Reset();
        }
        return;
    }
    if (sdbuf_notfull()) { // log the main data
        #if defined(ADXL345_ENABLED)
        if (HHG_CONF_IN_FIFOMODE) { // in FIFO logging mode?
            while ( ((adxl345_read_byte(ADXL345_FIFO_ST)&0b00011111)>0) ||
                    (ACC_INT==1) ) { // while FIFO not empty & interrupt high:
                acc_getxyz(&accval);
                if (!sdbuf_is_new_accslot()) {         // if not in fresh slot,
                    if (sdbuf_check_rle(&accval, rle_delta)) // and different 
                        sdbuf_goto_next_accslot();     // then go to next slot
                }
                if (sdbuf_notfull())
                    sdbuf_add_acc(&accval); // add/overwrite new sensor values
                if (sdbuf_deltaT_full())
                    sdbuf_goto_next_accslot();
                if (sdbuf_full())
                    return;
            }
            set_osc_sleep_int1();   // sleep till watermark is reached
        } else
        #endif // ADXL345_ENABLED
        { // pull new accelerometer samples each 10 ms by default:
            acc_getxyz(&accval);
            if (!sdbuf_is_new_accslot()) {         // if not in fresh new slot,
                if (sdbuf_check_rle(&accval, rle_delta)) // and different 
                    sdbuf_goto_next_accslot();     // then go to the next slot
            }
            if (sdbuf_notfull()) {
                sdbuf_add_acc(&accval); // add/overwrite the new sensor values
                set_osc_sleep_t1(36);   // go to sleep for timeout of ~9.5ms
            }
            if (sdbuf_deltaT_full())
                sdbuf_goto_next_accslot();
        }
    }
    if (sdbuf_full()) { // write log to page
        #if defined(DISPLAY_ENABLED)
        disp_log_subdue();  // switch off the display if it is on
        #endif
        sdbuf_write(); // write to SD card and update counters (~8.5ms)
        #if defined(DISPLAY_ENABLED)
        disp_log_revive();
        #endif
        return; // return to IOProcess, buffer is now on_hold
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
            case 100: rtc_init(); break;
            #if defined(DISPLAY_ENABLED)
            case 90: disp_start_usb(); break;
            #endif
            case 80:  acc_init(hhg_conf.cs.acc_s, &(hhg_conf.cs.acc)); break;
            case 50:  cdc_print_init(hhg_conf.cs.acc); break;
            case 10:  cdc_eol(); break;
        }
    }
    else if (cdc_config_cmd('t')) { // read time from host
        if (cdc_get_conf((char*)tm.b,6)) { // b[7]=min, b[6]=sec, ..., b[3]=mnth
            tm.b[7]=tm.b[4]; tm.b[6]=tm.b[5]; tm.b[4]=tm.b[3]; tm.b[3]=tm.b[1]; 
            rtc_write(&tm);
            rtc_writestr(&tm,date_str,time_str);
            cdc_write_ok();
        }
    }
    else if (cdc_config_cmd('T')) { // read stop-logging time from host
        if (cdc_get_conf((char*)tm.b,6)) { // b[7]=min, b[6]=sec, ..., b[3]=mnth
            tm.b[7]=tm.b[4]; tm.b[6]=tm.b[5]; tm.b[4]=tm.b[3]; tm.b[3]=tm.b[1];
            tm_stop = rtc_2uint32(&tm);
            cdc_write_ok();
        }
    }
    else if (cdc_config_cmd('r')) {
        switch (config_cycle) {
            case 100: acc_getxyz(&accval); env_on(); break;
            case 80: env_read(light, thermo); break;
            case 70: rtc_writestr(&tm,date_str,time_str); break;
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
            case 1: USBSoftDetach();  is_logging = 1; break;
        }
    }
    else if (cdc_config_cmd('f')) {
        //UINT16 format_i = 0;
        if((config_cycle>=60) && (config_cycle <= 210))
        {
            write_FAT(&sd_buffer, config_cycle - 60);
            write_SD(config_cycle - 52, sd_buffer.bytes);
        }

        switch (config_cycle) {
            case 230: write_MBR(&sd_buffer); break; // (sector 1)
            case 220: MDD_SDSPI_SectorWrite(0, sd_buffer.bytes, 1); break;
            case 50: write_root_table(&sd_buffer);    break;
            case 40: write_SD(244, sd_buffer.bytes);  break;    // Root directory at sector 244
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
