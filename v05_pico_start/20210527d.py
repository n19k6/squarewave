from machine import Pin, mem32
from rp2 import PIO, StateMachine, asm_pio
import time
import ure

from array import array
from uctypes import BF_POS, BF_LEN, BFUINT32, UINT32, struct, addressof


SM0_CLKDIV = 0x50200000 + 0x0c8
SM1_CLKDIV = 0x50200000 + 0x0e0
SM2_CLKDIV = 0x50200000 + 0x0f8
SM3_CLKDIV = 0x50200000 + 0x110

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




@asm_pio()
def nop():
    nop()

def f2b(f):
    sm = StateMachine(3, nop, freq=f)
    print(sm.active())
    sm.active(0)
    return mem32[SM3_CLKDIV]

def hz2f(hz):
    #1_000_000 = 15,256 Hz
    return int(float(hz*1_000_000*2)/15.268)

def rps2f(rps):
    # 100_000 entspricht 347.1 Hz
    return int(float(rps*100_000)/347.1)


#print(f2b(12122))
#print(f2b(132122))

@asm_pio(sideset_init=PIO.OUT_LOW)
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
    
@rp2.asm_pio(
    # zuendung, nockewelle, kurbelwelle, debug
    out_init=(rp2.PIO.OUT_HIGH, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=32,
)
def signal():
    wrap_target()
    out(pins, 4)
    #out(pins, 3)
    #out(x, 1)
    wrap()
# minimum frequency is 2500    
#sm = rp2.StateMachine(0, signal, freq=100_000, out_base=Pin(18))

class PIOPWM:
    def __init__(self, sm_id, pin, pwm_prog2, max_count, count_freq):
        self._sm = StateMachine(sm_id, pwm_prog2, freq=2 * count_freq, sideset_base=Pin(pin))
        # Use exec() to load max count into ISR
        self._sm.put(max_count)
        self._sm.exec("pull()")
        self._sm.exec("mov(isr, osr)")
        self._sm.active(1)
        self._max_count = max_count
        self._pin = pin
        
    def set(self, value):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        value = max(value, -1)
        value = min(value, self._max_count)
        #print(value)
        self._sm.put(value)

    def stop(self):
        self._sm.active(0)

print("signal generator v1.01")
print("type help for help")

l1f, l1d = 10, 0.5
l2f, l2d = 100, 0.5
rpm, igf, cs = 10000, -3, 4


pwm1 = PIOPWM(1, 16, pwm_prog, max_count=(1 << 16) - 1, count_freq=int(l1f*65_790))
pwm2 = PIOPWM(2, 17, pwm_prog, max_count=(1 << 16) - 1, count_freq=int(l2f*65_790))

#Pin(16, Pin.OUT).value(0)

mem32[SM1_CLKDIV] = f2b(hz2f(l1f))
mem32[SM2_CLKDIV] = f2b(hz2f(l2f))

print(int((1<<16)*l1d))
print(int((1<<16)*l2d))

pwm1.set(int((1<<16)*l1d))
pwm2.set(int((1<<16)*l2d))

# 100_000 entspricht 347.1 Hz
sm = rp2.StateMachine(0, signal, freq=100_000, out_base=Pin(18))

init_channels()

data = array("I", [0 for _ in range(36)])

#

offset_n = 4
offset_z = 5

def fill_array(n, z, z1=True, z2=True, z3=True, z4=True):
    
    a = array("I", [0 for _ in range(36)])
    #a[0] = a[0] | 1<<31-1

    for i in range(288*4):
        if i%4 == 0 and i%8 == 0: 
            #i = i*4+1
            #j, k = int(i/32), i % 32
            j = int(i/32)
            k = i % 32
            #a[j] = a[j] | 1<<31-k
            
    for i in range(34):
        i = i*4*4+1
        #j, k = int(i/32), i % 32
        j = int(i/32)
        k = i % 32
        a[j] = a[j] | 1<<31-k

    for i in range(34):
        i = 144*4+i*4*4+1
        #j, k = int(i/32), i % 32
        j = int(i/32)
        k = i % 32
        #print(j)
        a[j] = a[j] | 1<<31-k
            
    for i in range(4):
        za=[z1,z2,z3,z4]
        if za[i]:
            i = i*72*4+2+n*4
            i = i % (288*4)
            #j, k = int(i/32), i % 32
            j = int(i/32)
            k = i % 32
            #print(j)
            a[j] = a[j] | 1<<31-k
            
    for i in range(288):
        i = i*4+3
        #j, k = int(i/32), i % 32
        j = int(i/32)
        k = i % 32
        #print(j)
        a[j] = a[j] | 1<<31-k

    for i in range(3):
        i = i*72*4+3+z*4
        #j, k = int(i/32), i % 32
        i = i % (288*4)
        j = int(i/32)
        k = i % 32
        #print(j)
        #a[j] = a[j] & ~(1<<31-k)
        a[j] = a[j] & ~(1<<31-k)
                
    return a


offset_n = 4
offset_z = 5

data = fill_array(offset_n, offset_z)

ar_p = array("I", [0])
ar_p[0] = addressof(data)

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


#sleep(0.1)
print("on")
#Pin(16, Pin.OUT).value(1)
d1.CTRL_TRIG.EN = 1
d0.CTRL_TRIG.EN = 1
# important: start sm after channel
sm.active(1)

mem32[SM0_CLKDIV] = f2b(rps2f(4_000))

loop = True

while loop:
    cmd = input(">")
    error = True
    if ure.match("^exit$", cmd) != None:
        loop = False
        error = False
    if ure.match("^help$", cmd) != None:
        print("you can set the values for the variables: l1f, l1d, l2f, l2d, rpm, igf, cs\nexamples: l1d=55.6 or l1f=1.8\nother commands are 'status' and 'exit'")
        error = False
    if ure.match("^status$", cmd) != None:
        print("(l1f="+str(l1f)+", l1d="+str(l1d)+", l2f="+str(l2f)+", l2d="+str(l2d)+", rpm="+str(rpm)+", igf="+str(igf)+", cs="+str(cs)+")")
        error = False        
        

    if ure.match("^(l1d|l1f|l2d|l2f|rpm|igf|cs)\s*=\s*(\d+\.?(\d+)?)$", cmd) != None:
        v, n, o = ure.match("^(l1d|l1f|l2d|l2f|rpm|igf|cs)\s*=\s*(\d+\.?(\d+)?)$", cmd).groups()
        print(v, n, o)
        if v =="l1d":
            l1d = float(n)
            l1d = max(0, l1d)
            l1d = min(1, l1d)
            #print(int((1<<16)*l1d))
            if l1d == 0:
                pwm1.set(-1)
            if l1d >= 1:
                pwm1.set(0)
            else:
                if l1d > 0:
                    pwm1.set(int((1<<16)*l1d))
        if v =="l1f":
            l1f = float(n)
            #The frequency (which must be between 2000 and 125000000
            l1f = max(0.1, l1f)
            l1f = min(100, l1f)
            mem32[SM1_CLKDIV] = f2b(hz2f(l1f))
        if v =="l2d":
            #1_000_000 = 15,256 Hz
            l2d = float(n)
            l2d = max(0, l2d)
            l2d = min(1, l2d)
            #print(int((1<<16)*l1d))
            if l2d == 0:
                pwm2.set(-1)
            if l2d >= 1:
                pwm2.set(0)
            else:
                if l2d > 0:
                    pwm2.set(int((1<<16)*l2d))
        if v =="l2f":
            l2f = float(n)
            #The frequency (which must be between 2000 and 125000000
            l2f = max(0.1, l2f)
            l2f = min(100, l2f)
            mem32[SM2_CLKDIV] = f2b(hz2f(l2f))
        if v =="rpm":
            rpm = n
        if v =="igf":
            igf = int(float(n))
        if v =="cs":
            cs = int(float(n))
        error = False
        print("(l1f="+str(l1f)+", l1d="+str(l1d)+", l2f="+str(l2f)+", l2d="+str(l2d)+", rpm="+str(rpm)+", igf="+str(igf)+", cs="+str(cs)+")")
    if error:
        print("error parsing string")    

print(pwm1._sm.active())
print(pwm2._sm.active())

pwm1.stop()
pwm2.stop()
sm.active(0)

print(pwm1._sm.active())
print(pwm2._sm.active())

'''
#uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))

#uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
#uart0 = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))

time.sleep(0.2)
print(uart1)
#print(uart1)


# for i in range(100):
#     txData = b'hello world ['+str(i)+']\n\r'
#     #print(i)
#     uart1.write(txData)
#     time.sleep(0.2)
#     rxData = bytes()
#     while uart0.any() > 0:
#         rxData += uart0.read(1)
#     print("rxData: ", end='')
#     print(rxData.decode('utf-8'), end='')

data = bytes()

loop = True
l1f=1
l1d=1
uart1.write(b'\rconnected\r')

while loop:
    time.sleep(0.1)
    while uart1.any() > 0:
        data += uart1.read(1)
    #for _ in data:
        #print(hex(_))
    if len(data) > 0:
        print(data)
        error = True
        if ure.match("^exit\r$", data) != None:
            loop = False
            error = False
        if ure.match("^help\r$", data) != None:
            uart1.write(b'you can set the values for the variables: l1f, l1d, l2f, l2d, rpm, igf, cs\rexamples:\rl1d=55.6 or l1f=1.8\r')
            error = False
        if ure.match("^(l1d|l1f)=(\d+\.?\d+)\r$", data) != None:
            v, n = ure.match("^(l1d|l1f)=(\d+\.?\d+)\r$", data).groups()
            error = False
        if error:
            uart1.write(b'error parsing string\r')
    data = b''
    


#while loop:
#    time.sleep(0.1)
#    
#    a = uart1.readline()
#    if a != None:
#        print(a)
#    if a == b'exit\n\r':
#        loop = False

# while loop:
#     time.sleep(0.1)
#     while uart1.any() > 0:
#         rxData = uart1.read(1)
#         print(hex(rxData[0]))
#         if (rxData[0] == 0x0d):
#             rxData += '\n'
#         if (rxData[0] == 0x78):
#             loop = False
        #fdghfghuart1.write(rxData)

uart1.write(b'\rdisconnected\r')
        
#uart0.deinit()
#uart1.deinit()

'''