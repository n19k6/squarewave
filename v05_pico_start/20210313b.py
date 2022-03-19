#20210313b.py

from machine import Pin, SPI
from time import sleep, sleep_ms
#from mcp3008 import MCP3008

from machine import PWM

from rp2 import PIO, StateMachine, asm_pio


# try PWM with PIO
# https://www.onetransistor.eu/2021/02/rpi-pico-pio-state-machine-square-wave.html
# https://www.instructables.com/Arbitrary-Wave-Generator-With-the-Raspberry-Pi-Pic/



def ten2four(ten):
    return int(ten/32)

class MCP3008:

    def __init__(self, spi, cs, ref_voltage=3.3):
        """
        Create MCP3008 instance

        Args:
            spi: configured SPI bus
            cs:  pin to use for chip select
            ref_voltage: r
        """
        self.cs = cs
        self.cs.value(1) # ncs on
        self._spi = spi
        self._out_buf = bytearray(3)
        self._out_buf[0] = 0x01
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

    def reference_voltage(self) -> float:
        """Returns the MCP3xxx's reference voltage as a float."""
        return self._ref_voltage

    def read(self, pin, is_differential=False):
        """
        read a voltage or voltage difference using the MCP3008.

        Args:
            pin: the pin to use
            is_differential: if true, return the potential difference between two pins,


        Returns:
            voltage in range [0, 1023] where 1023 = VREF (3V3)

        """

        self.cs.value(0) # select
        self._out_buf[1] = ((not is_differential) << 7) | (pin << 4)
        self._spi.write_readinto(self._out_buf, self._in_buf)
        self.cs.value(1) # turn off
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]

def unchanged(new, old, threshold):
	d = 0
	for i in range(len(new)):
		d = d + abs(new[i]-old[i])
	if d < threshold:
		b = True
	else:
		b = False
	#print(d)
	return b

def translate(x, in_min, in_max, out_min, out_max):
	return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def raw_translate(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=10000)
cs = Pin(22, Pin.OUT)
cs.value(1) # disable chip at start

#in_0 = Pin(20, Pin.OUT)
in_1 = Pin(21, Pin.OUT)

chip = MCP3008(spi, cs)

#https://docs.micropython.org/en/latest/esp8266/tutorial/pwm.html
#https://github.com/raspberrypi/pico-micropython-examples
#pwm = PWM(Pin(20)) # GP20
#pwm.freq(10)
#https://github.com/micropython/micropython/blob/master/ports/rp2/machine_pwm.c
#pwm.freq(1) -> ValueError: freq too small
#pwm.duty_u16(32768) # 50%
#pwm.duty_u16(16384) # 25%

@asm_pio(set_init=PIO.OUT_LOW)
def square():
    wrap_target()
    set(pins, 1) [20]
    set(pins, 0) [30]
    wrap()
    
sm = rp2.StateMachine(0, square, freq=20000000000.0, set_base=Pin(20))

sm.active(1)

state = True

last_0 = 0
last_1 = 0

nr = 0

while True:
    #in_0.value(state)
    #in_1.value(not state)
    #sleep(0.1)
    #state = not state
    actual_0 = chip.read(0)
    actual_1 = chip.read(1)
    
    b1 = unchanged([actual_0, actual_1], [last_0, last_1], 20)
    
    if not b1:
        [last_0, last_1] = [actual_0, actual_1]
   
        [b_0, b_1] = [translate(actual_0,0,1024,0,64), translate(actual_1,0,1024,0,64)]
        print(str(nr)+": ", end='')
        print(b_0, end='')
        print(","+str(b_1))
        nr = nr+1
        print(str(translate(b_0,0,63,0,100))+" Prozent")
        print(int((translate(b_0,0,63,0,100))*0.01*65536))
        print(str(translate(b_1,0,63,10,1000))+" Hz")
        #pwm.duty_u16(int(raw_translate(b_0,0,63,0,100)*(2**16)/100))
        #pwm.freq(translate(b_1,0,63,10,1000))
        
        
        
        #print(ten2four(actual_0), end='')
        #print(","+str(ten2four(actual_1)))
        
    sleep(0.5)