# Example based on pio_ws2812.py, but modified to use
# a DMA channel to push out the data to the PIO

# https://github.com/hoihu/projects/blob/master/pico/dma.py
# https://github.com/raspberrypi/pico-examples/blob/master/pio/i2c/i2c.pio
# https://gregchadwick.co.uk/blog/playing-with-the-pico-pt5/
# https://www.raspberrypi.org/forums/viewtopic.php?t=307605

import array, time
from machine import Pin
import rp2


#trigger = Pin(15, Pin.OUT)
#trigger.value(1)

Pin(17, Pin.OUT).value(0) # clock
Pin(18, Pin.OUT).value(0) # code


@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_HIGH,
    out_init=rp2.PIO.OUT_HIGH,
    set_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_RIGHT,
    autopull=True,
    #pull_thresh=32,
    #pull_thresh=4,
    #fifo_join=rp2.PIO.JOIN_TX
)
def send_data():
    #wrap_target()
    #out(pins, 1)
    label("start")
    out(x, 1)
    #nop().side(0)
    jmp(x, "a").side(1) [1]
    nop()
    set(pins, 1) [2]
    nop().side(0) [3]
    jmp("start")
    #wrap()
    label("a")
    nop()
    set(pins, 0) [2]
    nop().side(0)  [3]  
    jmp("start")
    #wrap()


sm = rp2.StateMachine(0, send_data, freq=100_000, sideset_base=Pin(17), out_base=Pin(18), set_base=Pin(18))

#char output[] = {0x00, 0x00, 0x7e, 0x01, 0x68, 0x00, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x4d, 0x00, 0x7e, 0x00, 0x00};

# direction is last from right to left and then top to buttom
#         <----------- start
#         <-----------
#         <-----------
#     end <-----------

def put_data(x):
    print("put_data")
    sm.put(0b10000000011111100000000000000000)
    sm.put(0b00000000000001010000000000010110)
    sm.put(0b10110010000000000000000000000000)
    sm.put(0b00000000000000000111111000000000)

p2 = Pin(16, Pin.IN, Pin.PULL_DOWN)
p2.irq(put_data, Pin.IRQ_FALLING)


#print(sm.tx_fifo())
sm.active(1)

print("program is running for 60 seconds")

time.sleep(60)

#time.sleep(0.5)
#trigger.toggle()
#time.sleep(0.5)
#trigger.toggle()

print("program is terminating")
sm.active(0)


