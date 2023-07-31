import time
import rp2
from machine import Pin


#from machine import Pin

p1 = Pin(13, Pin.OUT)
p1.value(0)

def process():
    p1.value(1)
    print("*")
    p1.value(0)

p2 = Pin(14, Pin.IN, Pin.PULL_DOWN)
#p2.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_RISING)
#p2.irq(process(), Pin.IRQ_RISING)

# Define the blink program.  It has one GPIO to bind to on the set instruction, which is an output pin.
# Use lots of delays to make the blinking visible by eye.
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)   [31]
    #nop()          [31]
    #nop()          [31]
    #nop()          [31]
    #nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    #nop()          [31]
    wrap()

# Instantiate a state machine with the blink program, at 2000Hz, with set bound to Pin(25) (LED on the Pico board)
sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(15))




# Run the state machine for 3 seconds.  The LED should blink.
sm.active(1)
time.sleep(1)
p2.irq(process(), Pin.IRQ_RISING)
time.sleep(10)
sm.active(0)
