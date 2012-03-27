/*******************************************************************************
 FileName:     	SD_Buffer.h,     the HedgeHog's SD buffer structure and tasks
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#ifndef SD_BUFFER__H
#define SD_BUFFER__H


#include <GenericTypeDefs.h>    // for UINT8 and UINT16
#include "acc3D_wrapper.h"      // for ACC_XYZ
#include "MDD File System/SD-SPI.h" // for storing the buffer to SD

#define SD_BUF_MAX_RAW_SAMPLES_PER_PAGE 126 // 4-bytes per sample = 504/4 = 126
#define ABSDIF(x,y) ((x)>(y))?((x)-(y)):((y)-(x))

/******************************************************************************/
// SD Card Buffer variables:
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
} sd_buffer_t;

/******************************************************************************/
extern sd_buffer_t sd_buffer;
static UINT16 sdbuffer_p;
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
