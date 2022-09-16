#  Raspberry Pico Pinout, e.g. https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf
#
#                                            +-----+
#     +--------------------------------------| USB |--------------------------------------+
#     | [01] GPO                             +-----+                            VBUS [40] |
#     | [02] GP1                                                                VSYS [39] |
#     | [03] GND                                                                 GND [38] |
#     | [04] GP2 SPI0_SCK                                                     3V3_EN [37] |
#     | [05] GP3 SPI0_TX                                                     3V3_OUT [36] |
#     | [06] GP4 SPI0_RX                                                    ADC_VREF [35] |
#     | [07] GP5 SPI0_CS                                                        GP28 [34] |
#     | [08] GND                                                                 GND [33] |
#     | [09] GP6 CRANKSHAFT 34-2                                                GP27 [32] |
#     | [10] GP7 IGF 4                                                          GP26 [31] |
#     | [11] GP8 CAMSHAFT 3-1                                                    RUN [30] |
#     | [12] GP9 DEBUG                                                          GP22 [29] |
#     | [13] GND                                                                 GND [28] |
#     | [14] GP10                                                               GP21 [26] |
#     | [15] GP11                                                               GP20 [26] |
#     | [16] GP12                                                               GP19 [25] |
#     | [17] GP13                                                  CODE         GP18 [24] |
#     | [18] GND                                                                 GND [23] |
#     | [19] GP14 OX1                                              RXCK_CLK     GP17 [22] |
#     | [20] GP15 OX2                                              TXCT_TRIGGER GP16 [21] |
#     +--------------------------------------|--|--|--------------------------------------+
#                                            |  |  |
#                                            S  G  S
#                                            W  N  W
#                                            D  D  D
#                                            C     I
#                                            L     O
#                                            K      
#

#https://github.com/hoihu/projects/blob/master/pico/dma.py


# 20.000 U/min = 333 U/s ~ 3 ms
# 
from rp2 import PIO, StateMachine, asm_pio
from machine import Pin, mem32
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
#def memcopy(ch, dest, src, size, enable=1):
#    ch.CTRL_TRIG.EN = 0
#    ch.WRITE_ADDR = addressof(dest)
#    ch.READ_ADDR = addressof(src)
#    ch.TRANS_COUNT = size // (1 << ch.CTRL_TRIG.DATA_SIZE)
#    ch.CTRL_TRIG.EN = enable


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

# 960*8/32 = 240, 960 is number of samples
data = array("I", [0 for _ in range(240)])

#


print(addressof(data))

print(bin(data[0]))


# documentation:

#             ___ streamed to pin9 (GP9): msb
#            /
#            |        ___ streamed to pin2 (GP2): lsb
#            |       /
#            |       |
#data[0] = 0b1000_0000_0100_0000_1000_0000_0100_0000



#data[0] = 0b10000000_01000000_00100000_00010000
#data[1] = 0b00001000_00000100_00000010_00000001
#data[2] = 0b00000001_00000010_00000100_00001000
#data[3] = 0b00010000_00100000_01000000_10000000

for i in range(240):
    if i % 4 == 0:
        data[i] = 0b00000001_10000001_00000011_10000011
    if i % 4 == 1:
        data[i] = 0b00000111_10000111_00001111_10001111
    if i % 4 == 2:
        data[i] = 0b00000000_10000000_00000000_10000000
    if i % 4 == 3:
        data[i] = 0b00000000_10000000_00000000_10000000

#data[0] = 0b10000000_01000000_00100000_00010000

ar_p = array("I", [0])
ar_p[0] = addressof(data)


@rp2.asm_pio(
    # zuendung, nockewelle, kurbelwelle, debug gggdfdf
    #out_init=(rp2.PIO.OUT_HIGH, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    # todo: sent out value representing 0V
    out_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    #out_init=(rp2.PIO.OUT_LOW),
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=32,
)
def signal():
    wrap_target()
    #out(x, 3)
    #out(pins, 3)
    #out(x, 1)
    #out(x, 1)
    out(pins, 8)
    wrap()
# minimum frequency is 2500    


# requirements: 300 U/s - 10_000 U/s ~ 0.3 kHz - 10 kHz

# freq=2000 ~ 2.083 Hz
# freq=200_000 ~ 208.3 Hz
# freq=288_046
# freq=9_601_536

sm = rp2.StateMachine(0, signal, freq=9_601_536, out_base=Pin(2))


print(sm)



#while True:
#    sleep(1)

# for i in range(3000):
#     print(i)
#     sleep(0.1)
#     put_data()
#     sleep(0.1)
     

# Start the StateMachine, it will wait for data on its FIFO.


d0=CHANNELS[0]
d0.CTRL_TRIG.EN = 0
d0.TRANS_COUNT = 240
d0.READ_ADDR = addressof(data)
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


sleep(0.1)
print("on")
#Pin(16, Pin.OUT).value(1)
d1.CTRL_TRIG.EN = 0
d0.CTRL_TRIG.EN = 0
# important: start sm after channel

sleep(3)
print("L0: starting sm")
sm.active(1)

sleep(6)
print("L1: starting dma channels")
d1.CTRL_TRIG.EN = 1
d0.CTRL_TRIG.EN = 1

sleep(10)
print("L2: stopping sm")
sm.active(0)

