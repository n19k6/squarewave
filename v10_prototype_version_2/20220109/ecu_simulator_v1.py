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
from re import match
from sys import exit

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

# "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
# "0"*144
# "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
# "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


#signal_1a = "1110"*36
#signal_2a = "1000"+"0000"*35
#signal_3a = "1000"+"0000"*35
#signal_4a = "1000"+"0000"*35

#signal_1b = "1110"*36
#signal_2b = "0000"*36
#signal_3b = "0000"*36
#signal_4b = "0000"*36

signal_1a = "1100"*34+"0000"+"0000"
signal_2a = "1100"+"0000"*17+"1100"+"0000"*17
#signal_2a = "110000000000000000000000000000000000000000000000000000000000000000000000"+"110000000000000000000000000000000000000000000000000000000000000000000000"
#signal_2a = "110000000000000000000000000000000000000000000000000000000000000000000000011000000000000000000000000000000000000000000000000000000000000000000000"
signal_3a = "1000"+"0000"*17+"1000"+"0000"*17
#signal_3a = "100000000000000000000000000000000000000000000000000000000000000000000000"+"100000000000000000000000000000000000000000000000000000000000000000000000"
signal_4a = "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


signal_1b = "1100"*34+"0000"+"0000"
signal_2b = "1100"+"0000"*17+"0000"+"0000"*17
#signal_2b = "110000000000000000000000000000000000000000000000000000000000000000000000"+"000000000000000000000000000000000000000000000000000000000000000000000000"
#signal_2b = "110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
signal_3b = "1000"+"0000"*17+"1000"+"0000"*17
#todo: anzahl
#signal_3b = "100000000000000000000000000000000000000000000000000000000000000000000000"+"100000000000000000000000000000000000000000000000000000000000000000000000"
signal_4b = "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

#signal_2a = "0000"*36
#signal_3a = "0000"*36

#signal_2b = "0000"*36
#signal_3b = "0000"*36

#signal_2a = signal_4a
#signal_3a = signal_4a

#signal_2b = signal_4b
#signal_3b = signal_4b

# check format of signals

#https://docs.micropython.org/en/latest/library/re.html -> counted repetitions ({m,n}) are not supported in micropython

signals = [signal_1a, signal_2a, signal_3a, signal_4a, signal_1b, signal_2b, signal_3b, signal_4b]

#if (not re.match("^[01]+$", signal_1) or len(signal_1) != 34):
# print("E: signal_1 is not a valid string")
# sys.exit(1)

for signal in signals:
    if (not match("^[01]+$", signal) or len(signal) != 144):
        print("E: signal \""+signal+"\" is not a valid string")
        exit(1)

signal_1 = signal_1a+signal_1b
signal_2 = signal_2a+signal_2b
signal_3 = signal_3a+signal_3b
signal_4 = signal_4a+signal_4b

mem_slot_1 = array("I", [0 for _ in range(36)])
mem_slot_2 = array("I", [0 for _ in range(36)])


def bad_fill_mem_slot_1(n, z):
    global mem_slot_1
    #mem_slot_1[0] = 0b00001011
    #signal_1 = "1100111100001111"
    print("a")
    for s in range(len(signal_1)):
        #calculate j (junk), k (position)
        i = s*4+1
        j, k = int(i/32), i % 32
        if signal_1[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
        else:
            mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)

    for s in range(len(signal_2)):
        #calculate j (junk), k (position)
        i = ((s*4+n*4)+2) % 288
        j, k = int(i/32), i % 32

        if signal_1[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
        else:
            mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)

    for s in range(len(signal_3)):
        #calculate j (junk), k (position)
        i = ((s*4+z*4)+3) % 288
        j, k = int(i/32), i % 32
        if signal_1[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
        else:
            mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)

    for s in range(len(signal_4)):
        #calculate j (junk), k (position)
        i = s*4
        j, k = int(i/32), i % 32
        if signal_4[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
            print("b")
        else:
            mem_slot_1[j] = mem_slot_1[j] & ~(1<<31-k)


def fill_mem_slot_2(n, z):
    global mem_slot_2
    #mem_slot_2[0] = 0b00001011
    #signal_1 = "1100111100001111"
    print("a")
    
    for i in range(36):
        mem_slot_2[i] = 0b0000_0000_0000_0000_0000_0000_0000_0000
    
    for s in range(len(signal_1)):
        #calculate j (junk), k (position)
        i = s*4+1
        j, k = int(i/32), i % 32
        if signal_1[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
        else:
            mem_slot_2[j] = mem_slot_2[j] #& ~(1<<31-k)

    for s in range(len(signal_2)):
        #calculate j (junk), k (position)
        #i = ((s*4+n*4)+2) % 288
        #bug 
        i = ((s*4+n*4)+2)
        if i>=288:
            i = i-288
        j, k = int(i/32), i % 32

        if signal_2[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
        else:
            mem_slot_2[j] = mem_slot_2[j] #& ~(1<<31-k)

    for s in range(len(signal_3)):
        #calculate j (junk), k (position)
        #i = ((s*4+z*4)+3) % 288
        i = ((s*4+z*4)+3)
        if i>=288:
            i = i-288
        j, k = int(i/32), i % 32
        if signal_3[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
        else:
            mem_slot_2[j] = mem_slot_2[j] #& ~(1<<31-k)

    for s in range(len(signal_4)):
        #calculate j (junk), k (position)
        i = s*4
        j, k = int(i/32), i % 32
        if signal_4[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
        else:
            mem_slot_2[j] = mem_slot_2[j] #& ~(1<<31-k)

    #for i in range(36):
    #    mem_slot_2[i] = 0b1000_0100_1000_0100_1000_0100_1000_0100

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

#data = fill_array(offset_n, offset_z, True, True, True, True)
#ar_p = array("I", [0])
#ar_p[0] = addressof(data)

#mem_slot_1
#fill_mem_slot_1(0, 0)
#ar_p = array("I", [0])
#ar_p[0] = addressof(mem_slot_1)

#mem_slot_2 = array("I", [0 for _ in range(4)])

0b1000_0000_1000_0000_1000_0000_1000_0000
0b1000_1000_1000_1000_1000_1000_1000_1000

0b0000_0000_0000_0000_0000_0000_0000_0000
0b1000_0000_1000_0000_1000_0000_1000_0000
0b1000_0100_1000_0100_1000_0100_1000_0100

#mem_slot_2[0] = 0b1000_0100_1000_0100_1000_0100_1000_0100
#mem_slot_2[1] = 0b1000_0100_1000_0100_1000_0100_1000_0100
#mem_slot_2[2] = 0b1000_0100_1000_0100_1000_0100_1000_0100
#mem_slot_2[3] = 0b1000_0100_1000_0100_1000_0100_1000_0100

#mem_slot_2[0] = 0b1000_1000_1000_1000_1000_1000_1000_1000
#mem_slot_2[1] = 0b1000_1000_1000_1000_1000_1000_1000_1000
#mem_slot_2[2] = 0b1000_1000_1000_1000_1000_1000_1000_1000
#mem_slot_2[3] = 0b1000_1000_1000_1000_1000_1000_1000_1000

# todo: bug -2 does not work
#fill_mem_slot_2(289, -2)

fill_mem_slot_2(4, 2)


ar_p = array("I", [0])
ar_p[0] = addressof(mem_slot_2)


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
# attention: value has to be the array size 288/8 = 36
d0.TRANS_COUNT = 36
d0.READ_ADDR = addressof(mem_slot_2)
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

sleep(1)
print(1)
sleep(1)
print(2)
sleep(1)
print(3)
sleep(1)
print(4)
sleep(1)
print(5)
sleep(4)
print("leaving")
exit(1)


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
        #data = fill_array(offset_n, offset_z, True, True, True, True)
        #ar_p = array("I", [0])
        #ar_p[0] = addressof(data)
        #d0.READ_ADDR = addressof(data)
        #d1.READ_ADDR = addressof(ar_p)
        
        #if (m[0]>=32 and led.value()==0):
        #    led.on()
        #if (m[0]<32 and led.value()==1):
        #    led.off()
    sleep(0.1)