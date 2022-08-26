a)

push: i2s data via dma

https://www.reddit.com/r/raspberrypipico/comments/lcmhs5/got_i2s_dac_working_with_pico/

 

spi via dma

https://vanhunteradams.com/Pico/DAC/DMA_DAC.html (SPI interface)

https://mcturra2000.wordpress.com/2021/08/09/rp2040-using-dma-to-set-spi-dac-mcp4921/

 

 

b)

convert pwm to analog using low filter

https://github.com/romilly/pico-code/blob/master/docs/fungen.md

 

c) r2r DAC

 

 

 

hardware:

* adafruit circuitpython DAC

https://www.instructables.com/Arbitrary-Wave-Generator-With-the-Raspberry-Pi-Pic/

 

https://learn.adafruit.com/mcp4725-12-bit-dac-tutorial

 

https://www.hackster.io/news/learn-how-to-use-pwm-to-generate-an-audio-signal-from-your-raspberry-pi-pico-00347dece8b8

 

https://github.com/rgrosset/pico-pwm-audio

https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf#page=24

 

 

https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf#page=24

 

 

 

a) Resistor DAC

https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf#page=24 (3.2.1. Resistor DAC)

https://digilent.com/reference/_media/reference/pmod/pmodr2r/pmodr2r_sch.pdf

 

 

 

 

b) Low Passfilter (PWM -> Analog)

https://github.com/romilly/pico-code/blob/master/docs/fungen.md

 

 

c) Dedicated DAC

https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf#page=24 (3.4.2. PCM(I2S audio, PCM5101A) [PCM]

https://github.com/miketeachman/micropython-i2s-examples (I2S DAC)

https://github.com/romilly/pico-code/blob/master/src/pico_code/pico/experiments/pio_dac.py

http://blog.rareschool.com/2021/02/raspberry-pi-pico-simple-projects.html

 

d) DMA

https://iosoft.blog/category/dma/

 

Kaufen (boards):

Berrybase:

Adafruit MCP4725 Breakout Board - 12-Bit DAC mit I2C Interface

MCP4725

5,10

12-Bit

I2C

 

Kaufen (ics):

 

 

Hardware:

Pmod R2R: Resistor Ladder D/A Converter, digilent

 

https://circuitdigest.com/tags/mcp4725

 
