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

# Requirements:
# - min und max von kurbelwellen signal: 2 Hz, 140 Hz

# Some useful links:
# https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
# https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf
# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf

# https://github.com/hoihu/projects/blob/master/pico/dma.py
# https://www.ashleysheridan.co.uk/blog/Getting+Discrete+Values+from+a+Potentiometer


import helper
import config

from uctypes import BF_POS, BF_LEN, BFUINT32, UINT32, struct, addressof
from machine import Pin, SPI, mem32
from time import sleep, sleep_ms, ticks_ms, ticks_diff
from array import array
from sys import exit

# hack begin

Pin(18, Pin.OUT).value(1)
Pin(19, Pin.OUT).value(1)


@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_HIGH,
    out_init=rp2.PIO.OUT_HIGH,
    set_init=rp2.PIO.OUT_HIGH,
    out_shiftdir=rp2.PIO.SHIFT_RIGHT,
    autopull=True,
    #pull_thresh=32,
    #pull_thresh=4,
    #fifo_join=rp2.PIO.JOIN_TX
)
def send_data():
    #wrap_target()
    #out(pins, 1)
    label("start")
    out(x, 1)
    #nop().side(0)
    jmp(x, "a").side(0) [1]
    nop()
    set(pins, 1) [2]
    nop().side(1) [3]
    jmp("start")
    #wrap()
    label("a")
    nop()
    set(pins, 0) [2]
    nop().side(1)  [3]  
    jmp("start")
    #wrap()


sm4 = rp2.StateMachine(4, send_data, freq=100_000, sideset_base=Pin(17), out_base=Pin(18), set_base=Pin(18))

def put_data2(x):
    #print("uuuu");
    sm4.put(0b10000000011111100000000000000000);
    sm4.put(0b00000000000001010000000000010110);
    sm4.put(0b10110010000000000000000000000000);
    sm4.put(0b00000000000000000111111000000000);

p2 = Pin(16, Pin.IN, Pin.PULL_UP)
p2.irq(put_data2, Pin.IRQ_FALLING)


#print(sm.tx_fifo())
sm4.active(1)

# hack end



clk_freq_list = config.clk_freq_list
clk_div_list = config.clk_div_list
clk_rpm_list = config.clk_rpm_list

pwm_freq_list = config.pwm_freq_list
pwm_div_list = config.pwm_div_list

PIN_SPI_ONE_SCK=2
PIN_SPI_ONE_MOSI=3
PIN_SPI_ONE_MISO=4
PIN_SPI_ONE_CS=5

PIN_OX1=14
PIN_OX2=15

PIN_IGF_1 = 19
PIN_IGF_2 = 20
PIN_IGF_3 = 21
PIN_IGF_4 = 22

signal_1a = "1100"*34+"0000"+"0000"
#signal_2a = "1100"+"0000"*17+"1100"+"0000"*17
signal_2a = "0011"+"1111"*17+"0011"+"1111"*17
signal_3a = "1000"+"0000"*17+"1000"+"0000"*17
signal_4a = "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


signal_1b = "1100"*34+"0000"+"0000"
#signal_2b = "1100"+"0000"*17+"0000"+"0000"*17
signal_2b = "0011"+"1111"*17+"1111"+"1111"*17
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
        i = s*4+3 
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_1[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
            
    for s in range(len(signal_2_shifted)):   
        i = s*4+1
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_2_shifted[s] == "1":
            mem_slot_1[j] = mem_slot_1[j] | 1<<31-k
            
    for s in range(len(signal_3_shifted)):   
        i = s*4+2
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
        i = s*4+3
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_1[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
            
    for s in range(len(signal_2_shifted)):   
        i = s*4+1
        j, k = int(i/32), i % 32 #calculate j (junk), k (position)
        if signal_2_shifted[s] == "1":
            mem_slot_2[j] = mem_slot_2[j] | 1<<31-k
            
    for s in range(len(signal_3_shifted)):   
        i = s*4+2
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

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def pwm_prog():
    #pull(noblock) .side(0)
    pull(noblock)
    mov(x, osr) # Keep most recent pull data stashed in X, for recycling by noblock
    mov(y, isr) # ISR must be preloaded with PWM count max
    jmp(not_x, "continue")
    #jmp("continue")
    #label("null")
    nop().side(0)
    label("continue")
    label("pwmloop")
    jmp(x_not_y, "skip")
    nop()         .side(1)
    label("skip")
    jmp(y_dec, "pwmloop")
    
class PIOPWM:
    def __init__(self, sm_id, pin, count_freq, max_count=(1 << 16) - 1):
        #print(pin)
        self._sm = rp2.StateMachine(sm_id, pwm_prog, freq=2 * count_freq, sideset_base=Pin(pin))
        # Use exec() to load max count into ISR
        self._sm.put(max_count)
        self._sm.exec("pull()")
        self._sm.exec("mov(isr, osr)")
        self._sm.active(1)
        self._max_count = max_count
        self._pin = pin

    def _set(self, value):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        if value>self._max_count:
            self._sm.active(0)
            #print("off: ", value)
            Pin(self._pin, Pin.OUT).value(1)
        else:
            if not(self._sm.active()):
                self._sm.put(self._max_count)
                self._sm.exec("pull()")
                self._sm.exec("mov(isr, osr)")
                self._sm.active(1)
                #print("on: ", value)
            value = max(value, -1)
            value = min(value, self._max_count)
            self._sm.put(value)
        
    def set(self, value):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        value = max(value, -1)
        value = min(value, self._max_count)
        #print(value)
        self._sm.put(value)

spi = SPI(0, sck=Pin(PIN_SPI_ONE_SCK), mosi=Pin(PIN_SPI_ONE_MOSI), miso=Pin(PIN_SPI_ONE_MISO), baudrate=10000)
cs = Pin(PIN_SPI_ONE_CS, Pin.OUT)
cs.value(1) # disable chip at start

igf_1 = Pin(PIN_IGF_1, Pin.IN)
igf_2 = Pin(PIN_IGF_2, Pin.IN)
igf_3 = Pin(PIN_IGF_3, Pin.IN)
igf_4 = Pin(PIN_IGF_4, Pin.IN)



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
    # GP6, GP7, GP8, GP9 = kurbelwelle, zuendung, nockewelle, debug
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

pwm1 = PIOPWM(1, PIN_OX1, 10_000, 10000)
pwm2 = PIOPWM(2, PIN_OX2, 10_000, 10000)


#pwm1._set(11000)
#pwm2._set(-1)
#pwm1._set(1000)
#pwm2._set(2000)


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
last_gpio = [1, 1, 1, 1]

sm_active = True
i = 0
while True:
    # rpm, offset_igf, offset_cs, lambda1_freq, lambda1_duty, lambda2_freq, lambda2_duty
    actual_poti = [chip.read(8), chip.read(2), chip.read(1), chip.read(3), chip.read(4), chip.read(5), chip.read(6), chip.read(7)]
    # hack
    actual_gpio = [igf_1.value(), igf_2.value(), igf_3.value(), igf_4.value()]
    #print(actual_gpio,"-", last_gpio)
    #print(actual_poti)
    difference_poti = max(
        abs(last_poti[0]-actual_poti[0]),
        abs(last_poti[1]-actual_poti[1]),
        abs(last_poti[2]-actual_poti[2]),
        abs(last_poti[3]-actual_poti[3]),
        abs(last_poti[4]-actual_poti[4]),
        abs(last_poti[5]-actual_poti[5]),
        abs(last_poti[6]-actual_poti[6]),
        abs(last_poti[7]-actual_poti[7]))
    
    if (difference_poti>20 or actual_gpio != last_gpio): 
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
        
        if (actual_poti[0]//16 != last_poti[0]//16):
            #freq = frequencies[actual_poti[2]//16]    
            #print("=> "+str([actual_poti[0]//16, clk_freq_list[actual_poti[0]//16]]), end=" ")
            #todo: register ueberschreiben fuer frequenz
            SM0_CLKDIV = 0x50200000 + 0x0c8
            mem32[SM0_CLKDIV] = clk_div_list[actual_poti[0]//16]
            if (actual_poti[0]//16 == 0 and sm_active):
                sm.active(0)
                sm_active = False
            if (actual_poti[0]//16 != 0 and not sm_active):
                sm.active(1)
                sm_active = True
            print("=> "+str([sm_active, actual_poti[0]//16, clk_freq_list[actual_poti[0]//16], clk_rpm_list[actual_poti[0]//16]]), end=" ")
        
        if (actual_poti[1]//16 != last_poti[1]//16 or actual_poti[2]//16 != last_poti[2]//16 or actual_gpio != last_gpio):
            offset_n, offset_z = actual_poti[2]//16-32, actual_poti[1]//16-32
            print("=> "+str([offset_n, offset_z]), end=" ")
            fill_mem_slot(offset_n, offset_z, actual_gpio[0], actual_gpio[1], actual_gpio[2], actual_gpio[3])
            
        if (actual_poti[4]//16 != last_poti[4]//16):
            duty_ox1 = (actual_poti[4]-2)*10 # [0-1023] -> [-2-1021]
            duty_ox1 = min(11_000, duty_ox1)
            duty_ox1 = max(-1, duty_ox1)
            duty_ox1_text = str(100*duty_ox1/10_000)+"%"
            if duty_ox1 <= 10:
                duty_ox1 = -1
                duty_ox1_text = "0 %"
            if duty_ox1 >= 10_000:
                duty_ox1_text = "100 %"                
            print("=> "+str(["duty_ox1", duty_ox1, duty_ox1_text]), end=" ")
            pwm1._set(duty_ox1)
            

        if (actual_poti[3]//16 != last_poti[3]//16):
            #freq = frequencies[actual_poti[2]//16]
            #todo: bug clk_freq_list is wrong
            print("=> "+str(["freq_ox1", actual_poti[3]//16, pwm_freq_list[actual_poti[3]//16]]), end=" ")
            #todo: register ueberschreiben fuer frequenz
            SM1_CLKDIV = 0x50200000 + 0x0e0
            # page 399, rp2040-datasheet.pdf
            #0x0c8, 0x0e0, 0x0f8, 0x110
            mem32[SM1_CLKDIV] = pwm_div_list[actual_poti[3]//16]
            
        if (actual_poti[6]//16 != last_poti[6]//16):
            duty_ox2 = (actual_poti[6]-2)*10 # [0-1023] -> [-2-1021]
            duty_ox2 = min(11_000, duty_ox2)
            duty_ox2 = max(-1, duty_ox2)
            duty_ox2_text = str(100*duty_ox2/10_000)+"%"
            if duty_ox2 <= 10:
                duty_ox2 = -1
                duty_ox2_text = "0 %"
            if duty_ox2 >= 10_000:
                duty_ox2_text = "100 %"                
            print("=> "+str(["duty_ox2", duty_ox2, duty_ox2_text]), end=" ")
            pwm2._set(duty_ox2)       
            
        if (actual_poti[5]//16 != last_poti[5]//16):
            #freq = frequencies[actual_poti[2]//16]    
            print("=> "+str(["freq_ox2", actual_poti[5]//16, pwm_freq_list[actual_poti[5]//16]]), end=" ")
            #todo: register ueberschreiben fuer frequenz
            SM2_CLKDIV = 0x50200000 + 0x0f8
            # page 399, rp2040-datasheet.pdf
            #0x0c8, 0x0e0, 0x0f8, 0x110
            mem32[SM2_CLKDIV] = pwm_div_list[actual_poti[5]//16]
            
        print("")
        
        #print(actual_gpio, actual_gpio != last_gpio)
        #print("A", actual_gpio)
        #last_gpio = actual_gpio
        #print("B", last_gpio)
        last_poti = actual_poti
    
    last_gpio = actual_gpio
    
    sleep(0.1)