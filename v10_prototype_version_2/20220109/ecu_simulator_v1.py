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
#     | [09] GP6                                                                GP27 [32] |
#     | [10] GP7                                                                GP26 [31] |
#     | [11] GP8                                                                 RUN [30] |
#     | [12] GP9                                                                GP22 [29] |
#     | [13] GND                                                                 GND [28] |
#     | [14] GP10                                                               GP21 [26] |
#     | [15] GP11                                                               GP20 [26] |
#     | [16] GP12                                                               GP19 [25] |
#     | [17] GP13                                                               GP18 [24] |
#     | [18] GND                                                                 GND [23] |
#     | [19] GP14                                                               GP17 [22] |
#     | [20] GP15                                                               GP16 [21] |
#     +--------------------------------------|--|--|--------------------------------------+
#                                            |  |  |
#                                            S  G  S
#                                            W  N  W
#                                            D  D  D
#                                            C     I
#                                            L     O
#                                            K      
#

# Requirements:
# - min und max von kurbelwellen signal: 2 Hz, 140 Hz

# Some useful links:
# https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
# https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf
# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf

# https://github.com/hoihu/projects/blob/master/pico/dma.py
# https://www.ashleysheridan.co.uk/blog/Getting+Discrete+Values+from+a+Potentiometer


import helper
from uctypes import BF_POS, BF_LEN, BFUINT32, UINT32, struct, addressof
from machine import Pin, SPI, mem32
from time import sleep, sleep_ms, ticks_ms, ticks_diff
from array import array
from sys import exit



clk_freq_list = [
    "2 Hz",
    "4 Hz",
    "6 Hz",
    "8 Hz",
    "10 Hz",
    "13 Hz",
    "15 Hz",
    "17 Hz",
    "19 Hz",
    "21 Hz",
    "24 Hz",
    "26 Hz",
    "28 Hz",
    "30 Hz",
    "32 Hz",
    "35 Hz",
    "37 Hz",
    "39 Hz",
    "41 Hz",
    "43 Hz",
    "45 Hz",
    "48 Hz",
    "50 Hz",
    "52 Hz",
    "54 Hz",
    "56 Hz",
    "59 Hz",
    "61 Hz",
    "63 Hz",
    "65 Hz",
    "67 Hz",
    "70 Hz",
    "72 Hz",
    "74 Hz",
    "76 Hz",
    "78 Hz",
    "80 Hz",
    "83 Hz",
    "85 Hz",
    "87 Hz",
    "89 Hz",
    "91 Hz",
    "94 Hz",
    "96 Hz",
    "98 Hz",
    "100 Hz",
    "102 Hz",
    "105 Hz",
    "107 Hz",
    "109 Hz",
    "111 Hz",
    "113 Hz",
    "115 Hz",
    "118 Hz",
    "120 Hz",
    "122 Hz",
    "124 Hz",
    "126 Hz",
    "129 Hz",
    "131 Hz",
    "133 Hz",
    "135 Hz",
    "137 Hz",
    "140 Hz"
]

clk_div_list = array("I", [0 for _ in range(64)])

clk_div_list[0] = -0b101100000100101000100000000000
clk_div_list[1] = 0b1101001111101101011110000000000
clk_div_list[2] = 0b1000110101001000111110100000000
clk_div_list[3] = 0b110100111110110101111000000000
clk_div_list[4] = 0b101010011000101011000100000000
clk_div_list[5] = 0b100000100110101011000000000000
clk_div_list[6] = 0b11100010000011100101100000000
clk_div_list[7] = 0b11000111011101100001000000000
clk_div_list[8] = 0b10110010011101110010000000000
clk_div_list[9] = 0b10100001011101111111100000000
clk_div_list[10] = 0b10001101010010001111100000000
clk_div_list[11] = 0b10000010011010101100000000000
clk_div_list[12] = 0b1111001000110011111100000000
clk_div_list[13] = 0b1110001000001110010100000000
clk_div_list[14] = 0b1101001111101101011100000000
clk_div_list[15] = 0b1100000111000011001000000000
clk_div_list[16] = 0b1011011101001001111000000000
clk_div_list[17] = 0b1010110111100011101000000000
clk_div_list[18] = 0b1010010101101000001000000000
clk_div_list[19] = 0b1001110110110110101000000000
clk_div_list[20] = 0b1001011010110100001100000000
clk_div_list[21] = 0b1000110101001000010100000000
clk_div_list[22] = 0b1000011110100001100100000000
clk_div_list[23] = 0b1000001001101010001100000000
clk_div_list[24] = 0b111110110010101101100000000
clk_div_list[25] = 0b111100100011001100000000000
clk_div_list[26] = 0b111001011110001001000000000
clk_div_list[27] = 0b110111100101100011000000000
clk_div_list[28] = 0b110101110100100111100000000
clk_div_list[29] = 0b110100001010101000000000000
clk_div_list[30] = 0b110010100110111110000000000
clk_div_list[31] = 0b110000011100001010000000000
clk_div_list[32] = 0b101111000110000010100000000
clk_div_list[33] = 0b101101110100100101000000000
clk_div_list[34] = 0b101100100111011010000000000
clk_div_list[35] = 0b101011011110001100100000000
clk_div_list[36] = 0b101010011000101001000000000
clk_div_list[37] = 0b101000110110100110000000000
clk_div_list[38] = 0b100111111001000101000000000
clk_div_list[39] = 0b100110111110011000100000000
clk_div_list[40] = 0b100110000110010101000000000
clk_div_list[41] = 0b100101010000101111100000000
clk_div_list[42] = 0b100100000100100111000000000
clk_div_list[43] = 0b100011010100100001000000000
clk_div_list[44] = 0b100010100110011000100000000
clk_div_list[45] = 0b100001111010000110000000000
clk_div_list[46] = 0b100001001111100011000000000
clk_div_list[47] = 0b100000010010110000100000000
clk_div_list[48] = 0b11111101100001000100000000
clk_div_list[49] = 0b11111000110111010100000000
clk_div_list[50] = 0b11110100011000011000000000
clk_div_list[51] = 0b11110000000011100100000000
clk_div_list[52] = 0b11101011111000011000000000
clk_div_list[53] = 0b11100101111000100100000000
clk_div_list[54] = 0b11100010000011011000000000
clk_div_list[55] = 0b11011110010110001100000000
clk_div_list[56] = 0b11011010110000101100000000
clk_div_list[57] = 0b11010111010010011100000000
clk_div_list[58] = 0b11010010010010000000000000
clk_div_list[59] = 0b11001111000100100100000000
clk_div_list[60] = 0b11001011111101010000000000
clk_div_list[61] = 0b11001000111011111000000000
clk_div_list[62] = 0b11000110000000001000000000
clk_div_list[63] = 0b11000001110000100100000000

PIN_SPI_ONE_SCK=2
PIN_SPI_ONE_MOSI=3
PIN_SPI_ONE_MISO=4
PIN_SPI_ONE_CS=5

signal_1a = "1100"*34+"0000"+"0000"
signal_2a = "1100"+"0000"*17+"1100"+"0000"*17
signal_3a = "1000"+"0000"*17+"1000"+"0000"*17
signal_4a = "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


signal_1b = "1100"*34+"0000"+"0000"
signal_2b = "1100"+"0000"*17+"0000"+"0000"*17
signal_3b = "1000"+"0000"*17+"1000"+"0000"*17
signal_4b = "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

signals = [signal_1a, signal_2a, signal_3a, signal_4a, signal_1b, signal_2b, signal_3b, signal_4b]

for signal in signals:
    if (not helper.junk(signal)):
        print("E: signal \""+signal+"\" is not a valid string")
        exit(1)

signal_1 = signal_1a+signal_1b
signal_2 = signal_2a+signal_2b
signal_3 = signal_3a+signal_3b
signal_4 = signal_4a+signal_4b

if helper.peaks(signal_1) != 34*2:
        print("E: number of peaks in signal \""+signal_1+"\" is not 34*2")
        exit(1)

if helper.peaks(signal_2) != 3:
        print("E: number of peaks in signal \""+signal_2+"\" is not 3")
        exit(1)
        
if helper.peaks(signal_3) != 4:
        print("E: number of peaks in signal \""+signal_3+"\" is not 4")
        exit(1)

if helper.peaks(signal_4) != 2:
        print("E: number of peaks in signal \""+signal_4+"\" is not 2")
        exit(1)
    


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

CHANNELS = [struct(0x50000000 + i * 0x40, DMA_LAYOUT) for i in range(0,2)]

# init dma channels to some default values
def init_channels():
    for i, ch in enumerate(CHANNELS):
        # no wraparound, sniff=0, swap_byte=0, irq_quiet=1
        # unpaced transfers (=0x3f). high prio=0, data_size=word, incr_r/w = true
        ch.CTRL_TRIG_RAW = 0x3f8030
        # set chain to itself, to disable chaining
        ch.CTRL_TRIG.CHAIN_TO = i

init_channels()

d0=CHANNELS[0]
d1=CHANNELS[1]
ar_p = array("I", [0])
mem_slot_1 = array("I", [0 for _ in range(36)])
mem_slot_2 = array("I", [0 for _ in range(36)])
mem_slot_1_active = False

def fill_mem_slot(n, z, p1=True, p2=True, p3=True, p4=True):
    global d0
    global ar_p
    global mem_slot_1_active
    global mem_slot_1
    global mem_slot_2
    
    if not mem_slot_1_active:
        fill_mem_slot_1(n, z, p1, p2, p3, p4)
        d0.READ_ADDR = addressof(mem_slot_1)
        ar_p[0] = addressof(mem_slot_1)
        mem_slot_1_active = True
    else:
        fill_mem_slot_2(n, z, p1, p2, p3, p4)
        d0.READ_ADDR = addressof(mem_slot_2)
        ar_p[0] = addressof(mem_slot_2)
        mem_slot_1_active = False       

def fill_mem_slot_1(n, z, p1=True, p2=True, p3=True, p4=True):
    global mem_slot_1

    for i in range(36):
        mem_slot_1[i] = 0b0000_0000_0000_0000_0000_0000_0000_0000
    
    signal_2_shifted = helper.shift(signal_2, n)
    signal_3_suppressed = helper.suppress(signal_3, p1, p2, p3, p4)
    signal_3_shifted = helper.shift(signal_3_suppressed, z)
    
    for s in range(len(signal_1)):   
        i = s*4+1
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_1[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
            
    for s in range(len(signal_2_shifted)):   
        i = s*4+2
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_2_shifted[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
            
    for s in range(len(signal_3_shifted)):   
        i = s*4+3
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_3_shifted[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
            
    for s in range(len(signal_4)):   
        i = s*4
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_4[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k    

def fill_mem_slot_2(n, z, p1=True, p2=True, p3=True, p4=True):
    global mem_slot_2

    for i in range(36):
        mem_slot_2[i] = 0b0000_0000_0000_0000_0000_0000_0000_0000
    
    signal_2_shifted = helper.shift(signal_2, n)
    signal_3_suppressed = helper.suppress(signal_3, p1, p2, p3, p4)
    signal_3_shifted = helper.shift(signal_3_suppressed, z)
    
    for s in range(len(signal_1)):   
        i = s*4+1
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_1[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
            
    for s in range(len(signal_2_shifted)):   
        i = s*4+2
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_2_shifted[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
            
    for s in range(len(signal_3_shifted)):   
        i = s*4+3
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_3_shifted[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
            
    for s in range(len(signal_4)):   
        i = s*4
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_4[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k    


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


chip = MCP3008(spi, cs)

state = True

offset_n = 0
offset_z = 0

t0 = ticks_ms()

fill_mem_slot(offset_n, offset_z)
#fill_mem_slot_1(offset_n, offset_z)
#d0.READ_ADDR = addressof(mem_slot_1)
#ar_p[0] = addressof(mem_slot_1)

t1 = ticks_ms()
print(ticks_diff(t1, t0))


@rp2.asm_pio(
    # zuendung, nockewelle, kurbelwelle, debug
    out_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    #out_init=(rp2.PIO.OUT_HIGH, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    #out_init=(rp2.PIO.OUT_LOW),
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=32,
)
def signal():
    wrap_target()
    #out(x, 1)
    #out(pins, 3)
    out(pins, 4) [7]
    wrap()

#sm = rp2.StateMachine(0, signal, freq=3_000, out_base=Pin(6))
sm = rp2.StateMachine(0, signal, freq=173_725, out_base=Pin(6))




#d0=CHANNELS[0]
d0.CTRL_TRIG.EN = 0
# attention: value has to be the array size 288/8 = 36
d0.TRANS_COUNT = 36
d0.READ_ADDR = addressof(mem_slot_1)
d0.WRITE_ADDR = PIO0_BASE_TXF0
d0.CTRL_TRIG.INCR_WRITE = 0
d0.CTRL_TRIG.INCR_READ = 1
d0.CTRL_TRIG.DATA_SIZE = 2

d0.CTRL_TRIG.TREQ_SEL = 0
d0.CTRL_TRIG.CHAIN_TO = 1
#d0.CTRL_TRIG.RING_SEL = 0
#d0.CTRL_TRIG.RING_SIZE = 2

#d1=CHANNELS[1]
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

#sleep(1)
#print(1)
#sleep(1)
#print(2)
#sleep(1)
#print(3)
#fill_mem_slot(-1, 1, True, True, False, True)
#sleep(1)
#print(4)
#sleep(1)
#print(5)
#sleep(4)
#print("leaving")
#exit(1)


last_poti = [0, 0, 0, 0, 0, 0, 0, 0]
last_gpio = [0, 0, 0, 0]

i = 0
while True:
    actual_poti = [chip.read(7), chip.read(6), chip.read(5), chip.read(4), chip.read(8), chip.read(1), chip.read(2), chip.read(3)]
    difference_poti = max(
        abs(last_poti[0]-actual_poti[0]),
        abs(last_poti[1]-actual_poti[1]),
        abs(last_poti[2]-actual_poti[2]),
        abs(last_poti[3]-actual_poti[3]),
        abs(last_poti[4]-actual_poti[4]),
        abs(last_poti[5]-actual_poti[5]),
        abs(last_poti[6]-actual_poti[6]),
        abs(last_poti[7]-actual_poti[7]))
    
    if (difference_poti>20): 
        #print(d)
        #m=[l[0]//16,l[1]//16,l[2]//16,l[3]//16,l[4]//16,l[5]//16,l[6]//16,l[7]//16]
        #m=[l[0]//16,l[1]//16]
        m = [
            actual_poti[0]//16,
            actual_poti[1]//16,
            actual_poti[2]//16,
            actual_poti[3]//16,
            actual_poti[4]//16,
            actual_poti[5]//16,
            actual_poti[6]//16,
            actual_poti[7]//16]
        
        print(i, end=" ")
        i = i+1
        print(m, end=" ")
        
        if (actual_poti[2]//16 != last_poti[2]//16):
            #freq = frequencies[actual_poti[2]//16]    
            print("=> "+str([actual_poti[2]//16, clk_freq_list[actual_poti[2]//16]]), end=" ")
            #todo: register ueberschreiben fuer frequenz
            SM0_CLKDIV = 0x50200000 + 0x0c8
            mem32[SM0_CLKDIV] = clk_div_list[actual_poti[2]//16]
            
        if (actual_poti[0]//16 != last_poti[0]//16 or actual_poti[1]//16 != last_poti[1]//16):
            offset_n, offset_z = actual_poti[0]//16-32, actual_poti[1]//16-32    
            print("=> "+str([offset_n, offset_z]), end=" ")
            fill_mem_slot(offset_n, offset_z)
            
        print("")
        
        last_poti = actual_poti
        
    sleep(0.1)