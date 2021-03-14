# Arbitrary waveform generator for Rasberry Pi Pico
# Requires 8-bit R2R DAC on pins 0-7. Works for R=1kOhm
# Achieves 125Msps when running 125MHz clock
# Rolf Oldeman, 7/2/2021. CC BY-NC-SA 4.0 licence
from machine import Pin,mem32
from rp2 import PIO, StateMachine, asm_pio
from array import array
from utime import sleep
from math import sin,pi

DMA_BASE=0x50000000
CH0_READ_ADDR  =DMA_BASE+0x000
CH0_WRITE_ADDR =DMA_BASE+0x004
CH0_TRANS_COUNT=DMA_BASE+0x008
CH0_CTRL_TRIG  =DMA_BASE+0x00c
CH0_AL1_CTRL   =DMA_BASE+0x010
CH1_READ_ADDR  =DMA_BASE+0x040
CH1_WRITE_ADDR =DMA_BASE+0x044
CH1_TRANS_COUNT=DMA_BASE+0x048
CH1_CTRL_TRIG  =DMA_BASE+0x04c

PIO0_BASE     =0x50200000
PIO0_BASE_TXF0=PIO0_BASE+0x10

#state machine that just pushes bytes to the pins
#@asm_pio(out_init=(PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH),
#         out_shiftdir=PIO.SHIFT_RIGHT, autopull=True, pull_thresh=32)
@asm_pio(out_init=(PIO.OUT_LOW,PIO.OUT_LOW,PIO.OUT_LOW),
         out_shiftdir=PIO.SHIFT_RIGHT, autopull=True, pull_thresh=32)
def stream():
    out(pins,3)

#sm = StateMachine(0, stream, freq=125000000, out_base=Pin(0))


#2-channel chained DMA. channel 0 does the transfer, channel 1 reconfigures
p_ar=array('I',[0]) #global 1-element array 
@micropython.viper
def startDMA(ar,nword):
    p=ptr32(ar)
    mem32[CH0_READ_ADDR]=p
    mem32[CH0_WRITE_ADDR]=PIO0_BASE_TXF0
    mem32[CH0_TRANS_COUNT]=nword
    IRQ_QUIET=0x1 #do not generate an interrupt
    TREQ_SEL=0x00 #wait for PIO0_TX0
    CHAIN_TO=1    #start channel 1 when done
    RING_SEL=0
    RING_SIZE=0   #no wrapping
    INCR_WRITE=0  #for write to array
    INCR_READ=1   #for read from array
    DATA_SIZE=2   #32-bit word transfer
    HIGH_PRIORITY=1
    EN=1
    CTRL0=(IRQ_QUIET<<21)|(TREQ_SEL<<15)|(CHAIN_TO<<11)|(RING_SEL<<10)|(RING_SIZE<<9)|(INCR_WRITE<<5)|(INCR_READ<<4)|(DATA_SIZE<<2)|(HIGH_PRIORITY<<1)|(EN<<0)
    mem32[CH0_AL1_CTRL]=CTRL0
    
    p_ar[0]=p
    mem32[CH1_READ_ADDR]=ptr(p_ar)
    mem32[CH1_WRITE_ADDR]=CH0_READ_ADDR
    mem32[CH1_TRANS_COUNT]=1
    IRQ_QUIET=0x1 #do not generate an interrupt
    TREQ_SEL=0x3f #no pacing
    CHAIN_TO=0    #start channel 0 when done
    RING_SEL=0
    RING_SIZE=0   #no wrapping
    INCR_WRITE=0  #single write
    INCR_READ=0   #single read
    DATA_SIZE=2   #32-bit word transfer
    HIGH_PRIORITY=1
    EN=1
    CTRL1=(IRQ_QUIET<<21)|(TREQ_SEL<<15)|(CHAIN_TO<<11)|(RING_SEL<<10)|(RING_SIZE<<9)|(INCR_WRITE<<5)|(INCR_READ<<4)|(DATA_SIZE<<2)|(HIGH_PRIORITY<<1)|(EN<<0)
    mem32[CH1_CTRL_TRIG]=CTRL1

#setup waveform. frequency is 125MHz/nsamp  
nsamp=100 #must be a multiple of 4
wave=array("I",[0]*nsamp)
for isamp in range(nsamp):
    val=128+127*sin((isamp+0.5)*2*pi/nsamp) #sine wave
    #val=isamp*255/nsamp                     #sawtooth
    #val=abs(255-isamp*510/nsamp)            #triangle
    #val=int(isamp/20)*20*255/nsamp            #stairs
    
    wave[int(isamp/4)]+=(int(val)<<((isamp%4)*8)) 

#start



sm = StateMachine(0, stream, freq=1250000, out_base=Pin(10))
sm.active(1)

startDMA(wave,int(nsamp/4))
sleep(3)
sm.active(0)
sm = StateMachine(1, stream, freq=125000, out_base=Pin(10))
sleep(0.5)
sm.active(1)
sleep(1)
sm.active(0)
#sm = StateMachine(0, stream, freq=12500000, out_base=Pin(10))
#sm.active(1)
#sleep(1)
#sm.active(0)
#processor free to do anything else
