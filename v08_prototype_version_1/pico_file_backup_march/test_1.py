# http://people.ece.cornell.edu/land/courses/ece4760/RP2040/index_rp2040_testing.html

# https://vha3.github.io/


import time

from machine import Pin, Timer
led=Pin(25,Pin.OUT)
tim=Timer()

def tick(timer):
    led.toggle()

tim.init(freq=22.5,mode=Timer.PERIODIC,callback=tick)
time.sleep(0.2)
tim.deinit()

import array
# test assembler and
# implement 'addressof'
a=array.array('i',[ 1, 2, 3])
# invoke assembler
@micropython.asm_thumb
# passing an array name to the assembler
# actually passes in the address
def addressof(r0):
    # r0 is the output register, so address beomes output
    mov(r0, r0)
# now use the assembler routine  
addr_a = addressof(a)
print(addr_a)
print(machine.mem32[addressof(a)+4]) # returns '3'
print(machine.mem32[addressof(a)+8]) # returns '3'

# 52554  us -> 1221  us
@micropython.viper
def loop_viper():
    c = 0
    while c<10000:
        c += 1

def measure_time():
    t0 = time.ticks_us()
    #led.toggle()
    loop_viper()
    t1 = time.ticks_us()
    print(t1-t0, ' us')
    
measure_time()

import uasyncio
print(uasyncio.__version__)