# https://github.com/raspberrypi/pico-micropython-examples/

import time
import rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_HIGH, sideset_init=(rp2.PIO.OUT_HIGH))
def wait_pin_low():
    set(pins,1).side(0x1) # set both signals to HIGH 
    
    wrap_target()
    wait(0, pin, 0)
    
    #nop().side(0x0)
    set(y, 15).side(0x0) [1] # 16 loops = 17 downs, 2 pc
    label("loop_1")
    nop().side(0x1) [1]
    nop().side(0x0)
    jmp(y_dec, "loop_1") # 1 pc
    
    nop().side(0x1) [1]
    set(y, 3).side(0x0) # 4 loops = 5 downs, 1 pc
    set(pins,0)
    label("loop_2")
    nop().side(0x1) [1]
    nop().side(0x0)
    jmp(y_dec, "loop_2") # 1 pc
    
    nop().side(0x1) [1]
    set(y, 5).side(0x0)
    set(pins,1)
    label("loop_3")
    nop().side(0x1) [1]
    nop().side(0x0)
    jmp(y_dec, "loop_3") # 1 pc
    
    nop().side(0x1) [1]
    nop().side(0x0)
    set(pins,0)
    nop().side(0x1) [1]
    nop().side(0x0)
    set(pins,1)
    nop().side(0x1) [1]
    nop().side(0x0)
    set(pins,0)   
    nop().side(0x1) [1]
    nop().side(0x0) [1]
    nop().side(0x1) [1]
    #nop().side(0x0)
    
    set(pins,1)

    wait(1, pin, 0)
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_HIGH, sideset_init=(rp2.PIO.OUT_HIGH))
def send_key():
    set(pins,1).side(0x1) # set both signals to HIGH 
    
    wrap_target()
    wait(0, pin, 0)
    
    #nop().side(0x0)
    set(y, 15).side(0x0) [1] # 16 loops = 17 downs, 2 pc
    label("loop_1")
    nop().side(0x1) [1]
    nop().side(0x0)
    jmp(y_dec, "loop_1") # 1 pc
    
    nop().side(0x1) [1]
    set(y, 3).side(0x0) # 4 loops = 5 downs, 1 pc
    set(pins,0)
    label("loop_2")
    nop().side(0x1) [1]
    nop().side(0x0)
    jmp(y_dec, "loop_2") # 1 pc
    
    nop().side(0x1) [1]
    set(y, 5).side(0x0)
    set(pins,1)
    label("loop_3")
    nop().side(0x1) [1]
    nop().side(0x0)
    jmp(y_dec, "loop_3") # 1 pc
    
    nop().side(0x1) [1]
    nop().side(0x0)
    set(pins,0)
    nop().side(0x1) [1]
    nop().side(0x0)
    set(pins,1)
    nop().side(0x1) [1]
    nop().side(0x0)
    set(pins,0)   
    nop().side(0x1) [1]
    nop().side(0x0) [1]
    nop().side(0x1) [1]
    #nop().side(0x0)
    
    set(pins,1)

    wait(1, pin, 0)
    wrap()

receiver = Pin(13, Pin.IN, Pin.PULL_UP)

# The frequency (which must be between 2000 and 125000000)
# frequency of arduino sketch of clock is approx. 80us, 12500

sm = rp2.StateMachine(0, send_key, freq=25000, sideset_base=Pin(10), set_base=Pin(11), in_base=receiver)

trigger = Pin(12, Pin.OUT)
trigger.value(1)

sm.active(1)

for i in range(5):
    time.sleep(0.5)
    trigger.value(1)
    time.sleep(0.5)
    trigger.value(0)    
 
sm.active(0)

    