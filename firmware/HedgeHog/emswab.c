#include "emswab.h"

void
emswab_init(uint8_t mswabbufsize, uint8_t mergethr)
{
       bs              = BS;           // mswab buffer size
       l_bound = BS/2;         // swab buffer lower bound
       h_bound = BS*2;         // swab buffer upper bound

       mt              = mergethr;     // merge threshold used in the bottom-up approximation

       do_approx = 0;          // indicates whether to run an approximation or not

       init1 = 1;                      // flag for intial filling of the swab buffer
       slope = 0;                      // variables for slope sign change detection

       lastvalpos = 0;         // position last data value has been stored to
       costs_len = 0;          // length of the costs array (used in the bu step)

       return;
}


uint8_t
emswab( uint8_t newval, SegBuffer_t *buf, uint16_t index )
{
       uint16_t k              = 0;            // loop counter & slope sign
       ac[lastvalpos] = newval;        // store the new data point

       // initially -> fill up the buffer!
       if(init1 && lastvalpos>=bs)
       {
               init1 = 0;
               costs_buffer_len = 0;
       }

       do_approx = 0;
       // check if there is enough data
       if( !init1 && lastvalpos>=l_bound )
       {
               // if sign has changed or buffered data exceeds higher bound -> do approximation
               if( ssgn(ac[lastvalpos-1],ac[lastvalpos])!=slope || lastvalpos>=h_bound )
               {
                       do_approx = 1;

                       // 3. update buffer size and right buffer window position
                       // if new buffer size exceeds higher bound, override
                       if(lastvalpos>=h_bound)
                               bs = h_bound;
                       else
                               bs = lastvalpos;
               }
       }
       else
       {
               // not enough data in the buffer yet... get slope sign
               slope = ssgn(ac[lastvalpos-1],ac[lastvalpos]);
       }

       // do approximation?
       if( do_approx )
       {
               // prepare vals array; init inds array; update costs array;
               for(k=0; k<bs; k++)
               {
                       inds[k] = k;                    // init inds
                       vals[k] = ac[k];                // copy vals

                       if(k<costs_buffer_len)  // copy existing costs
                               costs[k] = costs_buffer[k];
               }

               // compute and add costs for new data points
               for(k=costs_buffer_len; k<bs-2; k++)
               {
                       calc_bu_error( ac, inds, vals, costs_buffer, k );
                       costs[k] = costs_buffer[k];
               }

               costs_buffer_len = bs-2;

               // run bottom-up approximation on the swabbuf NOW
               size = busegs(vals, bs, mt);

               // add the leftmost segment to the message buf
               buf->f[index].deltaT = inds[1];         // delta_t
               buf->f[index].val        = vals[1];             // right point of segment

               // compute the slope for last two data points
               slope = ssgn(ac[lastvalpos-1],ac[lastvalpos]);

               // shift buffered raw values to the left ... (kick out left most segment)
               for(k=inds[1]; k<=lastvalpos; k++)
               {
                       ac[k-inds[1]] = ac[k];          // kick out leftmost segment
                       if(k<costs_buffer_len)          // shift buffered costs
                               costs_buffer[k-inds[1]] = costs_buffer[k];
               }

               // ... and correct the position pointers
               lastvalpos -= inds[1];
               bs -= inds[1];
               costs_buffer_len -=inds[1];
       }

       // update last value position
       lastvalpos++;

       return do_approx;
}



/* calculates interpolation error (approximation cost for merging two adjacent segments) */
/* NOTE: we have an impicit typecast from uint16_t to int16_t for the inds[] array! */
void
calc_bu_error( uint8_t accel[], int16_t inds[], uint8_t vals[], uint16_t costs[], uint16_t i )
{
       // interpolation slope and cost
       int16_t intpk = 0;
       int16_t iv_sv = (vals[i+2]-vals[i])<<7;
       int16_t iv_si = inds[i+2]-inds[i];
       int16_t k;

       costs[i] = 0;
       for( k=inds[i]+1; k<inds[i+2]; k++ )
       {
               intpk = (vals[i]<<7) + (k-inds[i])*iv_sv/iv_si;
               costs[i] += absdist(intpk,(accel[k]<<7)) >>7;
       }
       return;
}

/* find the minimum cost in the costs array and return the position */
int16_t
get_mincost(uint16_t c[], uint16_t l)
{
       uint16_t min = UINT16_MAX;
       int16_t coord = -1;
       uint16_t i;

       for( i=0; i<l; i++ )
       {
               if( c[i]<min )
               {
                       min = c[i];
                       coord = i;

                       // a shortcut
                       if( min==0 )
                               break;
               }
       }

       return coord;
}


/* compute the bottom up approximation on a given buffer of raw data */
uint16_t
busegs( uint8_t vals[], uint16_t len, uint8_t mt )
{
       uint16_t i = 0;                 // loop counter
       int16_t coord = 0;              // position of the lowest merging cost in the array

       costs_len = len-2;

       // merge cheapest pairs of segments
       while( 1 )
       {
               // get the coordinate for the cheapest pair of segments
               coord = get_mincost(costs, costs_len);

               // if bad coordinate or costs exceed threshold -> break the while loop
               if( coord < 0 || costs[coord] >= mt )
                       break;

               // merge segments by shifting val/ind/costs[i+1:end] one space to the left
               for( i=coord+1; i<len; i++ )
               {
                       inds[i] = inds[i+1];
                       vals[i] = vals[i+1];
                       if( i<costs_len )
                               costs[i-1] = costs[i];
               }

               len--;                  // decrease actual lengh of data array
               costs_len--;    // ... and the costs array

               // update costs array now: costs for ( coord | coord+1 )
               //      -> will be skipped if the last two segments in the array have been merged (coord<coord_len)
               if( coord<costs_len )
                       calc_bu_error( ac, inds, vals, costs, coord );

               // update costs array now: costs for ( coord-1 | coord )
               //      -> will be skipped if the first two segments in the array have been merged (coord=0)
               if( coord>0 )
                       calc_bu_error( ac, inds, vals, costs, coord-1 );
       }

       return len;
}