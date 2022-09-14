dummy

pico: dma 8 outputs using pmod board
check digital outputs first

https://www.hackster.io/56254/using-the-pmod-r2r-with-arduino-uno-ad3de4

0-255 -> 0-3.3V

960 werte pro periode
mem_slot_2[i] = 0b0000_0000_0000_0000_0000_0000_0000_0000
960/4 = 240 32bit words

calculate micropython code for array

-1V = 0, 1V=255

pico+logic analyzer (im keller)

---
pins ansteuern
volt messen (nach wiederstaenden)
ausrechnen (drehzahl 300-mindestens 6.000 besser 10.000)
signal mit oszilaskop messen

---
20220913:
MicroPython v1.16 on 2021-06-18
update to v1.19.1
machine.bootloader()
and copy uf2 file to RPI-RP2
MicroPython v1.19.1 on 2022-06-18


https://vanhunteradams.com/Pico/DAC/DMA_DAC.html
https://forum.micropython.org/viewtopic.php?f=21&t=10717
https://stackoverflow.com/questions/66388451/how-to-use-raspberry-pi-pico-with-dac-with-spi-to-generate-sine-wave-of-1-khz-wi
https://codeutility.org/dma-how-to-use-raspberry-pi-pico-with-dac-with-spi-to-generate-sine-wave-of-1-khz-with-20-k-samples-per-cycle-stack-overflow/
https://people.ece.cornell.edu/land/courses/ece4760/RP2040/index_rp2040_testing.html
https://www.youtube.com/watch?v=OenPIsmKeDI (Raspberry Pi Pico PIO - Ep. 8 - Introduction to DMA)
https://www.youtube.com/watch?v=PrMQpv9iCFw
rp2040-datasheet.pdf DMA section

https://iosoft.blog/2021/10/26/pico-adc-dma/




