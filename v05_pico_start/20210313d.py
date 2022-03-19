#https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/pio_1hz.py

# Example using PIO to blink an LED and raise an IRQ at 1Hz.

from time import sleep, sleep_ms
from machine import Pin, Timer
import rp2

pin_20 = Pin(20, Pin.OUT)
tim = Timer()
lambda1_on_ms = 0

def tick(timer):
    global pin_20
    global lambda1_on_ms
    pin_20.value(1)
    sleep_ms(lambda1_on_ms)
    pin_20.value(0)
    
#tim.init(freq=10.1, mode=Timer.PERIODIC, callback=tick)
#sleep(5)
#tim.init(freq=20.2, mode=Timer.PERIODIC, callback=tick)    
#sleep(10)

# freq 0.1-10 Hz, duty = 0.1-0.9
def lambda1(freq1, duty):
    global lambda1_on_ms
    lambda1_on_ms = int(1/freq1*duty*1000)
    #print(lambda1_on_ms)
    tim.init(freq=freq1, mode=Timer.PERIODIC, callback=tick)
    
lambda1(10.2,0.5)
sleep(2)
lambda1(5.2,0.123)
#lambda1(10.2,0.5)
sleep(7)


# 
# @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
# def blink_1hz():
#     # Cycles: 1 + 1 + 6 + 32 * (30 + 1) = 1000
#     irq(rel(0))
#     #nop()                       [29]
#     set(pins, 1)
#     #set(y, 10)
#     #label("y_high")
#     set(x, 31)                  [5]
#     label("delay_high")
#     nop()                       [29]
#     jmp(x_dec, "delay_high")
#     #jmp(y_dec, "y_high")
# 
#     # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
#     set(pins, 0)
#     #set(y, 10)
#     #label("y_low")
#     set(x, 31)                  [6]
#     label("delay_low")
#     nop()                       [29]
#     jmp(x_dec, "delay_low")
#     #jmp(y_dec, "y_low")
# 
# @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
# def blink_0_1hz():
#     # Cycles: 1 + 1 + 6 + 32 * (30 + 1) = 1000
#     # 1+1+8+10*(6+32*(30+1)+1)
#     
#     irq(rel(0))
#     #nop()                       [29]
#     set(pins, 1)
#     set(y, 9) [7]
#     label("y_high")
#     set(x, 31)                  [5]
#     label("delay_high")
#     nop()                       [29]
#     jmp(x_dec, "delay_high")
#     jmp(y_dec, "y_high")
# 
#     # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
#     # 1+9+10*(6+32*(30+1)+1)
#     set(pins, 0) 
#     set(y, 9) [8]
#     label("y_low")
#     set(x, 31)                  [5]
#     label("delay_low")
#     nop()                       [29]
#     jmp(x_dec, "delay_low")
#     jmp(y_dec, "y_low")
# 
# 
# # Create the StateMachine with the blink_1hz program, outputting on Pin(20).
# # frequency must be between 2000 and 125_000_000
# sm = rp2.StateMachine(0, blink_1hz, freq=20000, set_base=Pin(20))
# 
# # Set the IRQ handler to print the millisecond timestamp.
# #sm.irq(lambda p: print("sm1:"+str(time.ticks_ms())))
# 
# # Start the StateMachine.
# sm.active(1)
# 
# # Each PIO instance has a 32-slot instruction memory
# sm2 = rp2.StateMachine(1, blink_0_1hz, freq=2000, set_base=Pin(19))
# 
# # Set the IRQ handler to print the millisecond timestamp.
# sm2.irq(lambda p: print("sm2:"+str(time.ticks_ms())))
# sm2.active(1)


