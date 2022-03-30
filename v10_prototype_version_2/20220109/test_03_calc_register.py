#https://forums.raspberrypi.com/viewtopic.php?p=1985859#p1984172
#Changing frequency of SM while running

#https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
# see chapter 4.9.6. List of Registers
#Clock divisor register for state machine N
#Frequency = clock freq / (CLKDIV_INT + CLKDIV_FRAC / 256)

#31:16 INT - Effective frequency is sysclk/(int + frac/256). Value of 0 is interpreted as 65536. If INT is 0, FRAC must also be 0
#15:8 FRAC - Fractional part of clock divisor
#7:0 Reserved

import rp2
from machine import freq, mem32, Pin
from time import sleep

def sm_div_calc(target_f):
    if target_f < 0:
        div = 256
    elif target_f == 0:
        # Special case: set clkdiv to 0.
        div = 0
    else:
        div = freq() * 256 // target_f
        if div <= 256 or div >= 16777216:
            raise ValueError("freq out of range")
    return div << 8

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)

def signal():
    wrap_target()
    nop()
    wrap()

def sm_div_ref(target_f):
    sm0 = rp2.StateMachine(0, signal, freq=target_f, set_base=Pin(26))
    SM0_CLKDIV = 0x50200000 + 0x0c8
    # convert to signed int value to unsigned int value
    if (mem32[SM0_CLKDIV]<0):
        return mem32[SM0_CLKDIV] + 2**32
    else:
        return mem32[SM0_CLKDIV]

print("freq():", freq())

# check if same results for example 2000 are calculated
tf = 2000

#x =  0b10000000_00000000_00000010_00000000
x = sm_div_ref(tf)
im = 0b11111111_11111111_00000000_00000000
fm = 0b00000000_00000000_11111111_00000000

i = (x&im)>>16
f = (x&fm)>>8
cf = freq() / (i + f / 256)
 
print("sm()", type(x), x, bin(x), i, f , cf, tf)

#using horuable's function to calc clock divider

div = sm_div_calc(tf)

i = (div&im)>>16
f = (div&fm)>>8
print("python",type(div), div, bin(div), i, f , cf, tf)



assert sm_div_ref(2000) ^ sm_div_calc(2000) == 0, "register values are different for freq 2000"

for f in [2000, 23413, 213123213, 123123,1000, 12323]:
    try:
        assert sm_div_ref(f) ^ sm_div_calc(f) == 0, "register values are different for freq "+str(f)
    except ValueError as e:
        print(e, "at frequency", str(f))
        

    
