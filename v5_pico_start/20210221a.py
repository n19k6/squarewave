import time
import rp2
from machine import Pin

# Define the blink program.  It has one GPIO to bind to on the set instruction, which is an output pin.
# Use lots of delays to make the blinking visible by eye.
@rp2.asm_pio(sideset_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW))
def blink():
    wrap_target()
    nop().side(0x3)
    nop().side(0x0) [2]
    nop().side(0x1)
    nop().side(0x0) [2]
    set(y, 31) #32 loops
    label("loop")
    nop().side(0x1)
    nop().side(0x0) [1]
    jmp(y_dec, "loop")
    nop() [3]
    nop() [3]
    wrap()
   

# Instantiate a state machine with the blink program, at 1000Hz, with set bound to Pin(25) (LED on the rp2 board)

# The frequency (which must be between 2000 and 125000000)
sm = rp2.StateMachine(0, blink, freq=48_310, sideset_base=Pin(1,0))
#sm = rp2.StateMachine(0, blink, freq=1250000, sideset_base=Pin(1,0))
#sm = rp2.StateMachine(0, blink, sideset_base=Pin(0,1,2))
# Run the state machine for 3 seconds.  The LED should blink.
sm.active(1)
time.sleep(10)
sm.active(0)