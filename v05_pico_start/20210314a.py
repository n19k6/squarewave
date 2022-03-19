# 20210314a.py

# https://www.instructables.com/Arbitrary-Wave-Generator-With-the-Raspberry-Pi-Pic/
# https://github.com/Wren6991/PicoDVI
# http://www.breakintoprogram.co.uk/projects/pico/composite-video-on-the-raspberry-pi-pico

# https://www.youtube.com/watch?v=yYnQYF_Xa8g
# https://www.youtube.com/watch?v=LXAwW2IYT7o

# DMA PIO PICO

#from time import sleep, sleep_ms
#from machine import Pin, Timer
#import rp2

#pin_20 = Pin(20, Pin.OUT)

import array, utime
from machine import Pin
from time import sleep
import rp2
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 =5
    T3 = 3
    label("bitloop")
    out(x, 1).side(0) [T3-1]
    jmp(not_x, "do_zero").side(1) [T1-1]
    jmp("bitloop").side(1) [T2-1]
    label("do_zero")
    nop().side(0) [T2-1]
    
@asm_pio(set_init=PIO.OUT_LOW)
def led_quarter_brightness():
    set(pins, 0) [2]
    set(pins, 1)
    
    
#sm = StateMachine(0, ws2812, freq=2000, sideset_base=Pin(20))
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(20))
sm.active(1)

sm1 = StateMachine(1, led_quarter_brightness, freq=2000, set_base=Pin(19))
sm1.active(1)

NUM_LEDS = 2
ar = array.array("I", [0 for _ in range(NUM_LEDS)])



print("blue")
for j in range(0, 255):
    #print(j)
    for i in range(NUM_LEDS):
        #print(i,j)
        ar[i] = j
        #sm.put(ar,8)
        #utime.sleep_ms(10)

print("a")
sleep(10)
sm.active(0)



