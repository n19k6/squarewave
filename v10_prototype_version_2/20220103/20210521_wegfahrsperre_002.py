# Example based on pio_ws2812.py, but modified to use
# a DMA channel to push out the data to the PIO

# https://github.com/hoihu/projects/blob/master/pico/dma.py
# https://github.com/raspberrypi/pico-examples/blob/master/pio/i2c/i2c.pio
# https://gregchadwick.co.uk/blog/playing-with-the-pico-pt5/
# https://www.raspberrypi.org/forums/viewtopic.php?t=307605

import array, time
from machine import Pin
import rp2


#trigger = Pin(14, Pin.OUT)
#trigger.value(1)

#Pin(16, Pin.OUT).value(0)
#Pin(17, Pin.OUT).value(0)
#Pin(18, Pin.OUT).value(1)
#Pin(19, Pin.OUT).value(1)

Pin(17, Pin.OUT).value(1) # clock
Pin(18, Pin.OUT).value(1) # code

Pin(19, Pin.OUT).value(1) # clock
Pin(20, Pin.OUT).value(1) # code

@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_HIGH,
    out_init=rp2.PIO.OUT_HIGH,
    set_init=rp2.PIO.OUT_HIGH,
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
    jmp(x, "a").side(0) [1]
    nop()
    set(pins, 1) [2]
    nop().side(1) [3]
    jmp("start")
    #wrap()
    label("a")
    nop()
    set(pins, 0) [2]
    nop().side(1)  [3]  
    jmp("start")
    #wrap()




@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_HIGH,
    out_init=rp2.PIO.OUT_HIGH,
    set_init=rp2.PIO.OUT_HIGH,
    out_shiftdir=rp2.PIO.SHIFT_RIGHT,
    autopull=True,
    #pull_thresh=32,
    #pull_thresh=4,
    #fifo_join=rp2.PIO.JOIN_TX
)
def send_data2():
    #wrap_target()
    #out(pins, 1)
    label("start")
    out(x, 1)
    #nop().side(0)
    jmp(x, "a").side(0) [1]
    nop()
    set(pins, 1) [2]
    nop().side(1) [3]
    jmp("start")
    #wrap()
    label("a")
    nop()
    set(pins, 0) [2]
    nop().side(1)  [3]  
    jmp("start")
    #wrap()

sm = rp2.StateMachine(0, send_data, freq=100_000, sideset_base=Pin(18), out_base=Pin(17), set_base=Pin(17))
sm2 = rp2.StateMachine(1, send_data2, freq=100_000, sideset_base=Pin(20), out_base=Pin(19), set_base=Pin(19))

#char output[] = {0x00, 0x00, 0x7e, 0x01, 0x68, 0x00, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x4d, 0x00, 0x7e, 0x00, 0x00};

# direction is last from right to left and then top to buttom
#         <----------- start
#         <-----------
#         <-----------
#     end <-----------

def put_data(x):
    sm.put(0b01111111100000011111111111111111);
    sm.put(0b11111111111110101111111111101001);
    sm.put(0b01001101111111111111111111111111);
    sm.put(0b11111111111111111000000111111111);


def put_data_sm():
    sm.put(0b01111111100000011111111111111111);
    sm.put(0b11111111111110101111111111101001);
    sm.put(0b01001101111111111111111111111111);
    sm.put(0b11111111111111111000000111111111);

def put_data_sm2():
    sm2.put(0b01111111100000011111111111111111);
    sm2.put(0b11111111111110101111111111101001);
    sm2.put(0b01001101111111111111111111111111);
    sm2.put(0b11111111111111111000000111111111);
    sm.put(0b01111111100000011111111111111111);
    sm.put(0b11111111111110101111111111101001);
    sm.put(0b01001101111111111111111111111111);
    sm.put(0b11111111111111111000000111111111);

#p2 = Pin(15, Pin.IN, Pin.PULL_UP)
#p2.irq(put_data, Pin.IRQ_FALLING)


#print(sm.tx_fifo())
sm.active(1)
sm2.active(1)

time.sleep(0.5)

for i in range(10):
    print(i)
    #put_data_sm()
    put_data_sm2()
    time.sleep(1)
    #time.sleep(0.1)
    #trigger.value(0)
    #time.sleep(0.002)
    #trigger.value(1)  

time.sleep(0.2)

sm.active(0)
sm2.active(0)

