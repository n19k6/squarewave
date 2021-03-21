# https://github.com/raspberrypi/pico-micropython-examples/

import time
import rp2
from machine import Pin, Timer

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
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_HIGH, sideset_init=(rp2.PIO.OUT_HIGH))
def wait_pin_low():
    wrap_target()
    nop().side(0x1)
    wait(0, pin, 0)
    nop().side(0x0) [0]
    nop().side(0x1) [0]
    #set(pins, 0).side(0x0) [7]
    #set(pins,1).side(0x1)
    set(y, 31) #32 loops
    label("loop")
    nop().side(0x1)
    nop().side(0x0) [1]
    jmp(y_dec, "loop")
    #nop().side(0x1)
    #nop().side(0x0) [1]
    #set(y, 31) #32 loops
    #label("loop")
    #nop().side(0x1)
    #nop().side(0x0) [1]
    #jmp(y_dec, "loop")
    #nop() [3]
    #nop() [3]
    nop().side(0x1)
    wait(1, pin, 0)
    wrap()

@rp2.asm_pio(sideset_init=(rp2.PIO.OUT_HIGH))
def square():
    wrap_target()
    #nop().side(0x1)
    wait(0, pin, 0)
    #nop().side(0x0) [0]
    #nop().side(0x1) [0]
    #set(pins, 0).side(0x0) [7]
    #set(pins,1).side(0x1)
    set(y, 31) #32 loops
    label("loop")
    nop().side(0x1)
    nop().side(0x0) [1]
    jmp(y_dec, "loop")
    #nop().side(0x1)
    #nop().side(0x0) [1]
    #set(y, 31) #32 loops
    #label("loop")
    #nop().side(0x1)
    #nop().side(0x0) [1]
    #jmp(y_dec, "loop")
    #nop() [3]
    #nop() [3]
    nop().side(0x1)
    wait(1, pin, 0)
    wrap()

receiver = Pin(13, Pin.IN, Pin.PULL_UP)
# easy eda
# The frequency (which must be between 2000 and 125000000)
#sm = rp2.StateMachine(0, blink, freq=48_310, sideset_base=Pin(1,0))
#                                    125000000
#sm = rp2.StateMachine(0, wait_pin_low, freq=2000, sideset_base=Pin(10), set_base=Pin(11), in_base=receiver)

sm = rp2.StateMachine(0, square, freq=2000, sideset_base=Pin(10), in_base=receiver)
sm_2 = rp2.StateMachine(1, square, freq=2000, sideset_base=Pin(11), in_base=receiver)

#sm.active(1)
#time.sleep(1)
#sm.active(0)

#sm = rp2.StateMachine(0, blink, freq=3200, sideset_base=Pin(12,13))
#sm.active(1)
#time.sleep(1)
#sm.active(0)

#Pin(10, Pin.OUT).value(1)




trigger = Pin(12, Pin.OUT)
trigger.value(1)



#def tick():
    #trigger.value(1)
    #print("tick")
    #sm.active(1)
    #time.sleep(0.05)
    #trigger.value(0)


#tim = Timer()

#tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

sm.active(1)
sm_2.active(1)
#time.sleep(5)
#sm.active(0)

#while True:
#    time.sleep(1)
#    tick()

for i in range(5):
    time.sleep(0.5)
    trigger.value(1)
    time.sleep(0.5)
    trigger.value(0)    
 
sm.active(0)
sm_2.active(0)

# result: fail signals are not in sync
    