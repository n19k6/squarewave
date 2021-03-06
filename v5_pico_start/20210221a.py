import time
import rp2
from machine import Pin

@rp2.asm_pio(sideset_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW))
def blink():
    wrap_target()
    nop().side(0x3)
    nop().side(0x0) [2]
    nop().side(0x1)
    nop().side(0x0) [1]
    set(y, 31) #32 loops
    label("loop")
    nop().side(0x1)
    nop().side(0x0) [1]
    jmp(y_dec, "loop")
    nop() [3]
    nop() [3]
    wrap()
   

# The frequency (which must be between 2000 and 125000000)
#sm = rp2.StateMachine(0, blink, freq=48_310, sideset_base=Pin(1,0))
sm = rp2.StateMachine(0, blink, freq=100_000, sideset_base=Pin(1,0))

sm.active(1)
time.sleep(10)
sm.active(0)