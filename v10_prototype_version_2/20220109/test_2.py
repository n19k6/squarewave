
from machine import Pin, mem32
import rp2
from time import sleep


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)

def signal():
    wrap_target()
    #out(x, 1)
    #out(pins, 3)
    #out(pins, 4) [8]
    set(pins, 1) [7] 
    set(pins, 0) [23] # 3 wartetakte (1+23 = 1+7+8+8)
    set(x, 16) [7]
    nop() [23] # 3 wartetakte
    label('loop') 
    nop() [31] # 4 wartetakte
    nop() [23] # 3 wartetakte
    jmp(x_dec, 'loop') [7]
    wrap()

#sm = rp2.StateMachine(0, signal, freq=3_000, out_base=Pin(6))
sm = rp2.StateMachine(0, signal, freq=173_725, set_base=Pin(9))

sm.active(1)

SM0_CLKDIV = 0x50200000 + 0x0c8
print(bin(mem32[SM0_CLKDIV]))

# MHZ_1=0b11111010000000000000000
# MHZ_2=0b01111101000000000000000
# KHZ_10=0b110000110101000000000000000000
# KHZ_20=0b011000011010100000000000000000
# mem32[SM0_CLKDIV]=MHZ_1

sleep(1)
print(1)
sleep(1)
print(2)
sleep(1)
print(3)
sleep(1)
print(4)
sleep(1)
print(5)
sleep(4)
print("leaving")

sm.active(0)

