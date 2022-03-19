import time
import rp2
from machine import Pin, mem32

# Define the blink program.  It has one GPIO to bind to on the set instruction, which is an output pin.
# Use lots of delays to make the blinking visible by eye.
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)
    set(pins, 0)
    wrap()

# Instantiate a state machine with the blink program, at 2000Hz, with set bound to Pin(25) (LED on the rp2 board)
sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(16))


# Run the state machine for 3 seconds.  The LED should blink.
SM0_CLKDIV = 0x50200000 + 0x0c8


# Description
# Clock divisor register for state machine N
# Frequency = clock freq / (CLKDIV_INT + CLKDIV_FRAC / 256)

# Bits Name Description Type Reset
# 31:16 INT Effective frequency is sysclk/(int + frac/256). Value of 0 is interpreted as 65536. If INT is 0, FRAC must also be 0.RW 0x0001
# 15:8 FRAC Fractional part of clock divisor RW 0x00
# 7:0 Reserved. - - -

word = mem32[SM0_CLKDIV]
#if word < 0:
#    word += 2**32
#word = 0b11111111_00000000_00000000_10101010
print("  ", end='')
for i in range(32):
    print(min(word & 1<<31-i,1), end='')
print()    

#print(mem32[SM0_CLKDIV])
if word < 0:
    print("negative")
    word = word+2**32
else:
    print("positive")

print(bin(word))

clkdiv_int = word & (0b1111_1111_1111_1111_0000_0000_0000_0000)
clkdiv_int = clkdiv_int >> 16
print(clkdiv_int)

sm.active(1)
time.sleep(1)
sm.active(0)

print("--")

for i in [3000,4000,6000,200_000]:
    print(i)
    sm = rp2.StateMachine(0, blink, freq=i, set_base=Pin(16))
    time.sleep(1)
    word = mem32[SM0_CLKDIV]
    print(bin(word))
    time.sleep(1)