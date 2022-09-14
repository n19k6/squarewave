#https://hackspace.raspberrypi.com/books/micropython-pico/pdf/download

#  Raspberry Pico Pinout, e.g. https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf
#
#                                            +-----+
#     +--------------------------------------| USB |--------------------------------------+
#     | [01] GPO                             +-----+                            VBUS [40] |
#     | [02] GP1                                                                VSYS [39] |
#     | [03] GND                                                                 GND [38] |
#     | [04] GP2 SPI0_SCK                                                     3V3_EN [37] |
#     | [05] GP3 SPI0_TX                                                     3V3_OUT [36] |
#     | [06] GP4 SPI0_RX                                                    ADC_VREF [35] |
#     | [07] GP5 SPI0_CS                                                        GP28 [34] |
#     | [08] GND                                                                 GND [33] |
#     | [09] GP6 CRANKSHAFT 34-2                                                GP27 [32] |
#     | [10] GP7 IGF 4                                                          GP26 [31] |
#     | [11] GP8 CAMSHAFT 3-1                                                    RUN [30] |
#     | [12] GP9 DEBUG                                                          GP22 [29] |
#     | [13] GND                                                                 GND [28] |
#     | [14] GP10                                                               GP21 [26] |
#     | [15] GP11                                                               GP20 [26] |
#     | [16] GP12                                                               GP19 [25] |
#     | [17] GP13                                                  CODE         GP18 [24] |
#     | [18] GND                                                                 GND [23] |
#     | [19] GP14 OX1                                              RXCK_CLK     GP17 [22] |
#     | [20] GP15 OX2                                              TXCT_TRIGGER GP16 [21] |
#     +--------------------------------------|--|--|--------------------------------------+
#                                            |  |  |
#                                            S  G  S

import machine
import utime

pin2 = machine.Pin(2, machine.Pin.OUT)
pin3 = machine.Pin(3, machine.Pin.OUT)
pin4 = machine.Pin(4, machine.Pin.OUT)
pin5 = machine.Pin(5, machine.Pin.OUT)
pin6 = machine.Pin(6, machine.Pin.OUT)
pin7 = machine.Pin(7, machine.Pin.OUT)
pin8 = machine.Pin(8, machine.Pin.OUT)
pin9 = machine.Pin(9, machine.Pin.OUT)

iv = [0,0,0,0,0,0,0,0,0]
iv = [0,0,0,0,0,0,0,0,0]

pin2.value(iv[0])
pin3.value(iv[1])
pin4.value(iv[2])
pin5.value(iv[3])
pin6.value(iv[4])
pin7.value(iv[5])
pin8.value(iv[6])
pin9.value(iv[7])

pins = [pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9]

for i in range(8):
    if i>100:
        print("skipping pin"+str(i))
    else:
        print("wave on pin"+str(i))
        #pins[i].value(1)
        for j in range(20):
            pins[i].value(1)
            utime.sleep(0.1)
            pins[i].value(0)
            utime.sleep(0.1)
        utime.sleep(5)
        pins[i].value(0)
    

#while True:
#    pin2.value(1)
#    utime.sleep(0.1)
#    pin2.value(0)
#    utime.sleep(0.1)
    
