#                  +-----+
#     +------------| USB |----+
#     + [01] 
#
#
#
#
#
#
#


# todos: raphael
# - pinout ascii
# - drei signale als 244 length string angeben und mit phasen verschiebung
# - min und max von kurbelwellen signal: 2 Hz, 140 Hz

# https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
# https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf
# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf

# https://github.com/hoihu/projects/blob/master/pico/dma.py
# https://www.ashleysheridan.co.uk/blog/Getting+Discrete+Values+from+a+Potentiometer

PIN_SPI_ONE_SCK=2
PIN_SPI_ONE_MOSI=3
PIN_SPI_ONE_MISO=4
PIN_SPI_ONE_CS=5

from uctypes import BF_POS, BF_LEN, BFUINT32, UINT32, struct, addressof
from machine import Pin, SPI, mem32
from time import sleep, sleep_ms, ticks_ms, ticks_diff
from array import array
#from mcp3008 import MCP3008

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
#CHANNELS = [struct(0x50000000 + i * 0x40, DMA_LAYOUT) for i in range(0,12)]
CHANNELS = [struct(0x50000000 + i * 0x40, DMA_LAYOUT) for i in range(0,2)]

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

def fill_array(n, z, z1=True, z2=True, z3=True, z4=True):
    
    a = array("I", [0 for _ in range(36)])
    a[0] = a[0] | 1<<31
    #a[17] = a[17] | 1<<31
    a[18] = a[18] | 1<<31

    for i in range(288*4):
        if i%4 == 0 and i%8 == 0: 
            #i = i*4+1
            #j, k = int(i/32), i % 32
            j = int(i/32)
            k = i % 32
            #a[j] = a[j] | 1<<31-k
            
    for i in range(34):
        i = i*4*4+3
        #j, k = int(i/32), i % 32
        j = int(i/32)
        k = i % 32
        a[j] = a[j] | 1<<31-k

    for i in range(34):
        i = 144*4+i*4*4+3
        #j, k = int(i/32), i % 32  ggg
        j = int(i/32)
        k = i % 32
        #print(j)
        a[j] = a[j] | 1<<31-k
        
# -----

    for i in range(34):
        i = i*4*4+3+4
        #j, k = int(i/32), i % 32
        j = int(i/32)
        k = i % 32
        a[j] = a[j] | 1<<31-k

    for i in range(34):
        i = 144*4+i*4*4+3+4
        #j, k = int(i/32), i % 32  ggg
        j = int(i/32)
        k = i % 32
        #print(j)
        a[j] = a[j] | 1<<31-k

# -----

    for i in range(288):
        i = i*4+2
        #j, k = int(i/32), i % 32
        j = int(i/32)
        k = i % 32
        a[j] = a[j] | 1<<31-k
        

    for i in range(4):
        za=[z1,z2,z3,z4]
        if za[i]:
            i = i*72*4+2+z*4
            i = i % (288*4)
            #j, k = int(i/32), i % 32
            j = int(i/32)
            k = i % 32
            #print(j)
            #a[j] = a[j] | 1<<31-k
            a[j] = a[j] & ~(1<<31-k)
            
    for i in range(288):
        i = i*4+1
        #j, k = int(i/32), i % 32
        j = int(i/32)
        k = i % 32
        #printdef fill_array(n, z, z1=True, z2=True, z3=True, z4=True):
        #a[j] = a[j] | 1<<31-k

    for i in range(3):
        i = i*72*4+1+n*4
        #j, k = int(i/32), i % 32
        i = i % (288*4)
        j = int(i/32)
        k = i % 32
        #print(j)
        #a[j] = a[j] & ~(1<<31-k)
        #a[j] = a[j] & ~(1<<31-k)
        a[j] = a[j] | 1<<31-k

    # 32 bit laenge invertiere signale
    for i in range(36):
        # 3-er signal
        #a[i] = a[i] ^ 0b0100_0100_0100_0100_0100_0100_0100_0100
        # 4-er signal
        a[i] = a[i] ^ 0b0010_0010_0010_0010_0010_0010_0010_0010        
        # invert 34-er signal
        #a[i] = a[i] ^ 0b0001_0001_0001_0001_0001_0001_0001_0001
        
    return a


class MCP3008:

    def __init__(self, spi, cs, ref_voltage=3.3):
        """
        Create MCP3008 instance

        Args:
            spi: configured SPI bus
            cs:  pin to use for chip select
            ref_voltage: r
        """
        self.cs = cs
        self.cs.value(1) # ncs on
        self._spi = spi
        self._out_buf = bytearray(3)
        self._out_buf[0] = 0x01
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

    def reference_voltage(self) -> float:
        """Returns the MCP3xxx's reference voltage as a float."""
        return self._ref_voltage

    def read(self, pin, is_differential=False):
        """
        read a voltage or voltage difference using the MCP3008.

        Args:
            pin: the pin to use
            is_differential: if true, return the potential difference between two pins,


        Returns:
            voltage in range [0, 1023] where 1023 = VREF (3V3)

        """

        self.cs.value(0) # select
        self._out_buf[1] = ((not is_differential) << 7) | (pin << 4)
        self._spi.write_readinto(self._out_buf, self._in_buf)
        self.cs.value(1) # turn off
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]

spi = SPI(0, sck=Pin(PIN_SPI_ONE_SCK), mosi=Pin(PIN_SPI_ONE_MOSI), miso=Pin(PIN_SPI_ONE_MISO), baudrate=10000)
cs = Pin(PIN_SPI_ONE_CS, Pin.OUT)
cs.value(1) # disable chip at start

#led = Pin(25, Pin.OUT)
#led.off()

chip = MCP3008(spi, cs)

state = True

offset_n = 0
offset_z = 0

t0 = ticks_ms()

data = fill_array(offset_n, offset_z, True, True, True, True)
ar_p = array("I", [0])
ar_p[0] = addressof(data)

t1 = ticks_ms()
print(ticks_diff(t1, t0))

@rp2.asm_pio(
    # zuendung, nockewelle, kurbelwelle, debug gggdfdf
    out_init=(rp2.PIO.OUT_HIGH, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    #out_init=(rp2.PIO.OUT_HIGH, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
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
    #out(pins, 3)
    out(pins, 4) [8]
    wrap()

#sm = rp2.StateMachine(0, signal, freq=3_000, out_base=Pin(6))
sm = rp2.StateMachine(0, signal, freq=173_725, out_base=Pin(6))




d0=CHANNELS[0]
d0.CTRL_TRIG.EN = 0
d0.TRANS_COUNT = 36
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

d1.CTRL_TRIG.EN = 1
d0.CTRL_TRIG.EN = 1
# important: start sm after channel
sm.active(1)


l=[0,0,0,0,0,0,0,0]

i = 0
while True:
    a=[chip.read(7),chip.read(6),chip.read(5),chip.read(4),chip.read(8),chip.read(1),chip.read(2),chip.read(3)]
    d=max(abs(l[0]-a[0]),abs(l[1]-a[1]),abs(l[2]-a[2]),abs(l[3]-a[3]),abs(l[4]-a[4]),abs(l[5]-a[5]),abs(l[6]-a[6]),abs(l[7]-a[7]))
    d=max(abs(l[0]-a[0]),abs(l[1]-a[1]))
    if (d>20):
        l=a
        #print(d)
        m=[l[0]//16,l[1]//16,l[2]//16,l[3]//16,l[4]//16,l[5]//16,l[6]//16,l[7]//16]
        m=[l[0]//16,l[1]//16]
        
        print(i, end=" ")
        i = i+1
        print(m)
        
        offset_n, offset_z = l[0]//16, l[1]//16
        data = fill_array(offset_n, offset_z, True, True, True, True)
        ar_p = array("I", [0])
        ar_p[0] = addressof(data)
        d0.READ_ADDR = addressof(data)
        d1.READ_ADDR = addressof(ar_p)
        #if (m[0]>=32 and led.value()==0):
        #    led.on()
        #if (m[0]<32 and led.value()==1):
        #    led.off()
    sleep(0.1)