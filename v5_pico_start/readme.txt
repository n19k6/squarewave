20210313:

begriffe:


Vx:
alle poties als 32 stellungs poties zu verstehen

V10:
kurbelwelle dreht mit 0,200-20000 U/min 34+2 zacken, duty 25%
nockenwelle 3+4 synchron zu kurbelwelle mit verschiebung
zuendsignal synchron zu kurbelwelle mit verschiebung
zuenaussetzer 1,2,3,4 einzeln komplet aus oder an
wegfahrsperre
zwei lambda sonden signale (=PWM) 0,1 Hz, 1Hz, 10 Hz + duty cyle  = 4 poties


loesungsansaetze:
a) lambda via pwm library
b) andere signale via PIO mit sync oder PIO aus speicher

V11:
zuendaussetzer nicht nur an oder aus sondern aussetzer regelbar von 1/1000 aussetzer bis 1000/1000 aussetzer
frage: per zufall (schwierig?)

V12:
kurbelwelle dreht nicht mit konstanter geschwindigkeit innerhalb einer drehung


###################################

https://www.heise.de/developer/artikel/Ein-Picobello-Microcontroller-Raspberry-Pi-Pico-Board-5045274.html
https://www.cnx-software.com/2021/01/27/a-closer-look-at-raspberry-pi-rp2040-programmable-ios-pio/
https://tutorials-raspberrypi.de/raspberry-pi-pico-mikrocontroller-programmieren/

https://hackspace.raspberrypi.org/articles/what-is-programmable-i-o-on-raspberry-pi-pico
https://www.seeedstudio.com/blog/2021/01/25/programmable-io-with-raspberry-pi-pico/
https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython
https://www.cnx-software.com/2021/01/27/a-closer-look-at-raspberry-pi-rp2040-programmable-ios-pio/



MCP3008-I/P

https://www.adafruit.com/product/931
-> nicht verfuegbar
https://shop.pimoroni.com/products/1-12-oled-breakout?variant=29421050757203
-> 14 EUR
https://www.adafruit.com/product/1463
-> 10 EUR
BME280
MPU9250 board
MPU6050 board
-> adafruit 3886-> 7 EUR

Raspberry Pi Pico - USB HID Auto Clicker with Circuit Python

5x2 kabel breadboard 
5x2 femaleXfemale

blues teile breadboard book

20210307:
https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf
https://blog.rareschool.com/2021/02/raspberry-pi-pico-project-2-mcp3008.html

todos:
implement wegfahrsperre
stop and instanciate pio maschine with frequency from poti
research on sync pios, read from memory
document requirements V10+V11+V12
order mcp3008, 10kOhm poties 20, jumper, adapter osci, level shifter ic
#############################
Hi,
I am a PIO beginner. I am exited about the board and got started fast using the good documentation.
I am porting a arduino sketch I programmed month ago for an arduino nano to generate a digital signal using a hardware timer and an ISR.
It did worked but the the hardware was not capable to deliver the signal with the needed frequency, so I thought a good idea to try and get started with the pico.
Especially I like the easy way to do programming with the Thonny IDE, hence no compile cycle or uploading of programs necessary.
My idea is to use micropython for the not time critical parts and use the PIOs for signal generation.

To get started the examples  micropython PIO examples are very valuable: https://github.com/raspberrypi/pico-examples

To understand/use the PIO capabilities it would be great to have two mini examples demonstrating the following:
a) cycle accurate sync of statemachines (see section 3.2.7 Interactions Between State Machines from the rp2040 datasheet: This allows cycle-accurate synchronisation between state machines)
b) reading/consuming data from RAM

The context of my questions is the following: 
I have dump of a signal (on two pins, one clock, one data) that should be triggered if a special input pin goes low (see 20210322c_arduino_reference.png)
I managed to implement the first 25% of the signal with PIO instructions and than reached the mark of 32 instructions, I think with much tinkering I might be able to represent the signal inside the 32 instractions, did only use the X register so far. (see 20210322a.py and 20210322a.png)

Nevertheless if I know/understand cycle-accurate synchronisation between state machines it would be far more straightforward to generate the two synced signals.

Thanks.

Best regards,
Raphael
