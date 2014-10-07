/*******************************************************************************
 FileName:     	SD_Buffer.h,     the HedgeHog's SD buffer structure and tasks
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/
#include <GenericTypeDefs.h>    // for UINT8 and UINT16
#include "acc3D_wrapper.h"      // for ACC_XYZ
#include "MDD File System/SD-SPI.h" // for storing the buffer to SD
#include "SD_FAT.h" // for sector start address (SECTOR_LG)

#ifndef SD_BUFFER__H
#define SD_BUFFER__H

#define SD_BUF_MAX_RAW_SAMPLES_PER_PAGE 126 // 4-bytes per sample = 504/4 = 126
#define ABSDIF(x,y) ((x)>(y))?((x)-(y)):((y)-(x))

/******************************************************************************/
// SD Card Buffer variables:


typedef union {
            UINT32 u32;
            struct {
                UINT8 range;
                UINT8 bw;
                UINT8 mode; // operating mode fifo, rle, etc.
                UINT8 power; // low power options
            } f;
        } hhg_conf_accs_t;
        
typedef union {

    BYTE   bytes[512]; // byte access,
    WORD   wrd[256];   // word access,

    struct {                // for incremental high-speed logging:
        UINT32 timestmp;    // time stamp
        UINT32 envdata;     // environment data
        struct {            // acceleration packet:
            UINT8 t;        //  - delta t
            ACC_XYZ xyz;    //  - 3d acceleration
        } acc[SD_BUF_MAX_RAW_SAMPLES_PER_PAGE];
    } f;

    struct {                // for low-speed logging:
        UINT32 id1;         // unique ID
        UINT32 id2;         // unique ID (no timestamp)
        struct {            // 12-byte mean/variance packet:
            UINT32 ts;      // - timestamp
            UINT8 mx, vx, my, vy, mz, vz; // - mean and variance per axis
            UINT16 l;       // - light (env)
        } acc[42];
    } mvf;

    struct {                            // config structure:
        UINT32 ID;        //0           // identifier
        UINT32 time;      //4              // time stamp
        UINT32_VAL acc;   //8              // accelerometer configuration
        hhg_conf_accs_t acc_s;	//12          // accelerometer sensitivity
        UINT32_VAL logg;		//16              // logging & processing setup
        UINT8 rle_delta;		//20          // RLE Delta
        UINT8 separator_1[3];	//21
        UINT8 name[8];			//24
        UINT8 separator_2[3];	//32
        UINT8 ver[7];			//35
        UINT8 separator_3[3];	//42
        ACC_XYZ init_acc;		//45
        UINT8 separator_4[3];
        WORD_VAL init_light;	//51
        UINT8 separator_5[3];
        UINT8 init_thermo;		//56
        UINT8 separator_6[3];
        BYTE  systime[8];		//60
        UINT8 separator_7[3];
        BYTE  stptime[8];		//71
        UINT8 separator_8[418];
        UINT16 sdbuf_iter;		//497
        UINT8 separator_11[3];	//501
        UINT16 sdbuf_pointer;	//502
        UINT8 separator_9[3];		//504
        UINT8 sdbuf_flag;		//507
        UINT8 separator_10[3];	//508
        UINT8 flag;				//511
    } conf;

} sd_buffer_t;

/******************************************************************************/
extern sd_buffer_t sd_buffer;
extern UINT16 sdbuffer_p;
static UINT16 sdbuffer_i;


/******************************************************************************/
void sdbuf_init_buffer(void);
void sdbuf_set_full(void);
BYTE sdbuf_full(void);
BYTE sdbuf_notfull(void);
void sdbuf_set_onhold(void);
BYTE sdbuf_is_onhold(void);
BYTE sdbuf_deltaT_full(void);
void sdbuf_goto_next_accslot(void);
BYTE sdbuf_is_new_accslot(void);
void sdbuf_add_acc(PACC_XYZ accval);
BYTE sdbuf_page(void);

/******************************************************************************/
BYTE sdbuf_check_rle(PACC_XYZ accval, BYTE rle_th);

/******************************************************************************/
void sdbuf_init(void);
BYTE sdbuf_write(void);
/******************************************************************************/

#endif // ifndef SD_BUFFER__H
