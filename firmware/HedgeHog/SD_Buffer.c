/*******************************************************************************
 FileName:     	SD_Buffer.c,     the HedgeHog's SD buffer structure and tasks
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED, or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/

#include "SD_Buffer.h"


/******************************************************************************/
void sdbuf_init_buffer(void) {
    sdbuffer_i = 0;
    sd_buffer.f.acc[0].t = 0;
}

void sdbuf_set_full(void) {
    sdbuffer_i = SD_BUF_MAX_RAW_SAMPLES_PER_PAGE;
}

BYTE sdbuf_full(void) {
    return (sdbuffer_i == SD_BUF_MAX_RAW_SAMPLES_PER_PAGE);
}

BYTE sdbuf_notfull(void) {
    return (sdbuffer_i < SD_BUF_MAX_RAW_SAMPLES_PER_PAGE);
}

void sdbuf_set_onhold(void) {
    sdbuffer_i = 0xFFF;
}

BYTE sdbuf_is_onhold(void) {
    return (sdbuffer_i == 0xFFF);
}

BYTE sdbuf_deltaT_full(void) {
    return (sd_buffer.f.acc[sdbuffer_i].t == 255);
}

void sdbuf_goto_next_accslot(void) {
    sdbuffer_i++; // go to next slot
    if (sdbuf_notfull())
        sd_buffer.f.acc[sdbuffer_i].t = 0; // zero next slot's deltaT
}

BYTE sdbuf_is_new_accslot(void) {
    return (sd_buffer.f.acc[sdbuffer_i].t == 0);
}

void sdbuf_add_acc(PACC_XYZ accval) {
    sd_buffer.f.acc[sdbuffer_i].t++; // incr delta T
    sd_buffer.f.acc[sdbuffer_i].xyz = *accval; // acc XYZ
}

BYTE sdbuf_page(void) {
    return (sdbuffer_p-512);
}

/******************************************************************************/
BYTE sdbuf_check_rle(PACC_XYZ accval, BYTE rle_th) {
    return ( (ABSDIF(accval->x, sd_buffer.f.acc[sdbuffer_i].xyz.x) +
              ABSDIF(accval->y, sd_buffer.f.acc[sdbuffer_i].xyz.y) +
              ABSDIF(accval->z, sd_buffer.f.acc[sdbuffer_i].xyz.z)) > rle_th );
}

/******************************************************************************/
void sdbuf_init(void) {
    /* sdbuffer_p points to the sector (also called 'page' in our project)
     * where the data is written. The actual value of SD_BUF_START_SECTOR
     * should correspond to the start of the log000 file in the root table.
     *
     * see the definition of SD_BUF_START_SECTOR for some other relevant details
     */
    sdbuffer_p = SD_BUF_START_SECTOR; // start at this sector
    sdbuffer_i = 0xFFF;
    MDD_SDSPI_InitIO();
    MDD_SDSPI_MediaInitialize(); // init SD SPI settings
}

BYTE sdbuf_write(void) {
    if (MDD_SDSPI_SectorWrite(sdbuffer_p, sd_buffer.bytes, FALSE)) {
        sdbuffer_p++;
        sdbuffer_i = 0xFFF;
    }
    return 0;
}
/******************************************************************************/
