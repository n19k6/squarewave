#https://github.com/hoihu/projects/blob/master/pico/dma.py

from machine import Pin
from time import sleep
from array import array

from uctypes import BF_POS, BF_LEN, BFUINT32, UINT32, struct, addressof

PIO0_BASE = 0x50200000
PIO0_BASE_TXF0 = PIO0_BASE+0x10
CH0_READ_ADDR = 0x50000000+0x00

DMA_CTRL_REG = {
        "AHB_ERROR": 31     << BF_POS | 1 << BF_LEN | BFUINT32,
        "READ_ERR": 30      << BF_POS | 1 << BF_LEN | BFUINT32,
        "WRITE_ERR": 29     << BF_POS | 1 << BF_LEN | BFUINT32,
        "Reserved": 25      << BF_POS | 4 << BF_LEN | BFUINT32,
        "BUSY": 24          << BF_POS | 1 << BF_LEN | BFUINT32,
        "SNIFF_EN": 23      << BF_POS | 1 << BF_LEN | BFUINT32,
        "BSWAP": 22         << BF_POS | 1 << BF_LEN | BFUINT32,
        "IRQ_QUIET": 21     << BF_POS | 1 << BF_LEN | BFUINT32,
        "TREQ_SEL": 15      << BF_POS | 6 << BF_LEN | BFUINT32,
        "CHAIN_TO": 11      << BF_POS | 4 << BF_LEN | BFUINT32,
        "RING_SEL": 10      << BF_POS | 1 << BF_LEN | BFUINT32,
        "RING_SIZE": 6      << BF_POS | 4 << BF_LEN | BFUINT32,
        "INCR_WRITE": 5     << BF_POS | 1 << BF_LEN | BFUINT32,
        "INCR_READ": 4      << BF_POS | 1 << BF_LEN | BFUINT32,
        "DATA_SIZE": 2      << BF_POS | 2 << BF_LEN | BFUINT32,
        "HIGH_PRIO": 1      << BF_POS | 1 << BF_LEN | BFUINT32,
        "EN": 0             << BF_POS | 1 << BF_LEN | BFUINT32,
}

DMA_LAYOUT = {
    "READ_ADDR": 0   | UINT32,
    "WRITE_ADDR": 4  | UINT32,
    "TRANS_COUNT": 8 | UINT32,
    "CTRL_TRIG": (12,  DMA_CTRL_REG),
    "CTRL_TRIG_RAW": 12 | UINT32, # for single update of all fields
    "AL1_CTRL": 16   | UINT32,
    "ABORT": 1092 | UINT32,
}

# create the DMA channel structs (0-11)
CHANNELS = [struct(0x50000000 + i * 0x40, DMA_LAYOUT) for i in range(0,12)]

# init dma channels to some default values
def init_channels():
    for i, ch in enumerate(CHANNELS):
        # no wraparound, sniff=0, swap_byte=0, irq_quiet=1
        # unpaced transfers (=0x3f). high prio=0, data_size=word, incr_r/w = true
        ch.CTRL_TRIG_RAW = 0x3f8030
        # set chain to itself, to disable chaining
        ch.CTRL_TRIG.CHAIN_TO = i

# example function to show mem->mem transfer
# dest, src can be bytearrays, size in bytes
def memcopy(ch, dest, src, size, enable=1):
    ch.CTRL_TRIG.EN = 0
    ch.WRITE_ADDR = addressof(dest)
    ch.READ_ADDR = addressof(src)
    ch.TRANS_COUNT = size // (1 << ch.CTRL_TRIG.DATA_SIZE)
    ch.CTRL_TRIG.EN = enable


init_channels()

'''
a = bytearray(100)
b = bytearray(100)

print("Before: b={}".format(b))
# copy some stuff to a
for i in range(0,100):
    a[i] = i

# copy a -> b using dma channel 0
memcopy(CHANNELS[0], b, a, 100)

print("After: b={}".format(b))
'''


#print(bin(8 | UINT32))

ar = array("I", [0 for _ in range(10)])
#ar[0] = 0b100_010_001_000_111_000_000_000_000_000_00
ar[0] = 0b1000_0100_0010_0000_1110_0000_1110_1110
ar[1] = 0x00000000
ar[2] = 0b1000_0100_0010_0000_1110_0000_1110_1110
ar[3] = 0x00000000
ar[4] = 0x00000000
ar[5] = 0x00000000
ar[6] = 0x00000000
ar[7] = 0x00000000
ar[8] = 0x00000000
ar[9] = 0b0000_0000_0000_0000_1110_0000_1110_0000
#ar[2] = 0xaa00aa00

ar_p = array("I", [0])
ar_p[0] = addressof(ar)

ar2 = array("I", [0 for _ in range(10)])
#ar[0] = 0b100_010_001_000_111_000_000_000_000_000_00
ar2[0] = 0b0010_0100_1000_0000_1110_0000_1110_1110
ar2[1] = 0x00000000
ar2[2] = 0b0010_0100_1000_0000_1110_0000_1110_1110
ar2[3] = 0x00000000
ar2[4] = 0x00000000
ar2[5] = 0x00000000
ar2[6] = 0x00000000
ar2[7] = 0x00000000
ar2[8] = 0x00000000
ar2[9] = 0b0000_0000_0000_0000_1110_0000_1110_0000

@rp2.asm_pio(
    out_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=32,
)
def signal():
    wrap_target()
    out(pins, 3)
    out(x, 1)
    wrap()
    
sm = rp2.StateMachine(0, signal, freq=80_000, out_base=Pin(17))

print(sm)

# Start the StateMachine, it will wait for data on its FIFO.


d0=CHANNELS[0]
d0.CTRL_TRIG.EN = 0
d0.TRANS_COUNT = 10
d0.READ_ADDR = addressof(ar)
d0.WRITE_ADDR = PIO0_BASE_TXF0
d0.CTRL_TRIG.INCR_WRITE = 0
d0.CTRL_TRIG.INCR_READ = 1
d0.CTRL_TRIG.DATA_SIZE = 2

d0.CTRL_TRIG.TREQ_SEL = 0
d0.CTRL_TRIG.CHAIN_TO = 1
#d0.CTRL_TRIG.RING_SEL = 0
#d0.CTRL_TRIG.RING_SIZE = 2

d1=CHANNELS[1]
d1.CTRL_TRIG.EN = 0
d1.TRANS_COUNT = 1
d1.READ_ADDR = addressof(ar_p)
d1.WRITE_ADDR = CH0_READ_ADDR
d1.CTRL_TRIG.INCR_WRITE = 0
d1.CTRL_TRIG.INCR_READ = 0
d1.CTRL_TRIG.DATA_SIZE = 2
d1.CTRL_TRIG.CHAIN_TO = 0

sm.active(1)
sleep(0.1)
print("on")
Pin(16, Pin.OUT).value(1)
d1.CTRL_TRIG.EN = 1
d0.CTRL_TRIG.EN = 1

sleep(0.5)
#d0.CTRL_TRIG.EN = 0
d1.CTRL_TRIG.EN = 0
Pin(16, Pin.OUT).value(0)
Pin(16, Pin.OUT).value(1)
sleep(0.5)
#d0.READ_ADDR = addressof(ar)
#d0.TRANS_COUNT = 10
d1.CTRL_TRIG.EN = 1
Pin(16, Pin.OUT).value(0)
Pin(16, Pin.OUT).value(1)
sleep(0.5)

#d0.CTRL_TRIG.EN = 0
sm.active(0)
print("off")
Pin(16, Pin.OUT).value(0)
