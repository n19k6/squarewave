# https://www.instructables.com/Arbitrary-Wave-Generator-With-the-Raspberry-Pi-Pic/
# https://github.com/Wren6991/PicoDVI
# http://www.breakintoprogram.co.uk/projects/pico/composite-video-on-the-raspberry-pi-pico

# DMA PIO PICO

from time import sleep, sleep_ms
from machine import Pin, Timer
import rp2

pin_20 = Pin(20, Pin.OUT)




