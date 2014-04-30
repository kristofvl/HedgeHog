#ifndef EMSWAB_H
#define EMSWAB_H

#ifdef CONTIKI
#include "contiki-net.h"
#else
#include "GenericTypeDefs.h"
#define uint8_t UINT8
#define int8_t INT8
#define uint16_t UINT16
#define int16_t INT16
#define UINT16_MAX 0xFFFF
#endif

// slope sign change macro
#define ssgn(v1,v2)             (((v1)<(v2))?1:(((v1)>(v2))?-1:0))

#define abs(x)                  (((x)<0)?-(x):x)
#define absdist(x,y)    (((x)<(y))?(y)-(x):(x)-(y))
#define sign(x)                 (((x)==0)?0:(((x)>0)?1:-1))

#define BS 20
#define MT 15

// maximum size of sensor values to be buffered for approximation
#define DATABUFSIZE 4

#define SEGBUFSIZE 2
typedef union
{
       uint8_t bytes[SEGBUFSIZE];      // byte access, or:
       struct {                                        // via the field f
               uint8_t deltaT;                 //  - delta t
               uint8_t val;                    //  - sensor value
       }f[SEGBUFSIZE/2];
} SegBuffer_t;                                  // type definition of the

SegBuffer_t SegBuffer;                  // the actual union object

/** global variables for emswab */

static uint8_t  bs;						// mswab buffer size (initially = BS)
static uint8_t  l_bound;				// swab buffer lower bound
static uint8_t  h_bound;                // swab buffer upper bound
static uint8_t  mt;						// merging threshold for bottom-up
static uint8_t  size;                   // number of segments produced by bottom-up
static uint8_t  init1;                  // initiall fill swab buffer
static uint8_t  do_approx;              // flag: do approx or not?
static int8_t   slope;                  // variables for slope sign change detection

static uint8_t  ac[DATABUFSIZE];		// current data buffer
static int16_t  lastvalpos;				// position last value has been stored to

static uint16_t inds[BS*2];             // bu-segments indices
static uint8_t  vals[BS*2];             // bu-segments values
static uint16_t costs[BS*2-2];  // costs array (used in the bu step)
static uint16_t costs_len;              // costs array length (used in the bu step)

static uint16_t costs_buffer[BS*2-2];   // ring buffer for bottom-up costs
static uint16_t costs_buffer_len = BS*2-2;      // initial length, will be updated


/** prototype definitions */

static int16_t  get_mincost(uint16_t c[], uint16_t l);
static uint16_t busegs( uint8_t acc[], uint16_t len, uint8_t mt );
static void             calc_bu_error( uint8_t ac[], int16_t inds[], uint8_t vals[], uint16_t costs[], uint16_t i );

void                    emswab_init(uint8_t bs, uint8_t mt);
uint8_t                 emswab( uint8_t newval, SegBuffer_t *buf, uint16_t index );

#endif // EMSWAB_H
