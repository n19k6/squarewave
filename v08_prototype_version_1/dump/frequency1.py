# rp2040-datasheet.pdf
# section 3.7 Registers
# SMx_CLKDIV
# Frequency = clock freq / (CLKDIV_INT + CLKDIV_FRAC / 256)
# 32bit 16-bit INT + 8-bit FRAC + 8-bit reserved


import time
import rp2
from machine import Pin, mem32

# Dump frequency of system clock. Default is 125 MHz
print("system clock frequency is:")
print(machine.freq())

# Define the blink program.  It has one GPIO to bind to on the set instruction, which is an output pin.
# Use lots of delays to make the blinking visible by eye.
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()

# Instantiate a state machine with the blink program, at 2000Hz, with set bound to Pin(25) (LED on the rp2 board)
# There are eight statemachines numbered from 0 to 7. Minimum frequency is 1908.
frequency=87654
sm = rp2.StateMachine(0, blink, freq=frequency, set_base=Pin(25))

# Run the state machine for 1 second.  The LED should blink.
sm.active(1)
time.sleep(0.5)
SM0_CLKDIV = 0x50200000 + 0x0c8
print(bin(mem32[SM0_CLKDIV] & 2**32-1))
print(bin((mem32[SM0_CLKDIV] >> 16) & 2**16-1))
print(bin((mem32[SM0_CLKDIV] >> 8) & 2**8-1))
print(int((mem32[SM0_CLKDIV] >> 16) & 2**16-1))
print(int((mem32[SM0_CLKDIV] >> 8) & 2**8-1))
#clock freq / (CLKDIV_INT + CLKDIV_FRAC / 256)
CLKDIV_INT = int((mem32[SM0_CLKDIV] >> 16) & 2**16-1)
CLKDIV_FRAC = int((mem32[SM0_CLKDIV] >> 8) & 2**8-1)
print(machine.freq()/(CLKDIV_INT+CLKDIV_FRAC/256))
sm.active(0)

freq = frequency
div = int(machine.freq()*256/freq)
div_int = int(div / 256)
div_frac = div & 0xff
print("%.2f" % freq)
print(div)
print(div_int)
print(div_frac)
print("%.2f" % (machine.freq()/(div_int+div_frac/256)))
print("-"*32)
print(bin(mem32[SM0_CLKDIV] & 2**32-1))
print(bin(div_int << 16 | div_frac << 8 & 2**32-1))


led = Pin(25, Pin.OUT)
led.off()