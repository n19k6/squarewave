#                  +-----+
#     +------------| USB |----+
#     + [01] 
#
#
#
#
#
#
#


# todos: raphael
# pinout ascii

# https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
# https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf
# https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf

# https://www.ashleysheridan.co.uk/blog/Getting+Discrete+Values+from+a+Potentiometer

PIN_SPI_ONE_SCK=2
PIN_SPI_ONE_MOSI=3
PIN_SPI_ONE_MISO=4
PIN_SPI_ONE_CS=5



from machine import Pin, SPI
from time import sleep, sleep_ms
#from mcp3008 import MCP3008

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

spi = SPI(0, sck=Pin(PIN_SPI_ONE_SCK), mosi=Pin(PIN_SPI_ONE_MOSI), miso=Pin(PIN_SPI_ONE_MISO), baudrate=10000)
cs = Pin(PIN_SPI_ONE_CS, Pin.OUT)
cs.value(1) # disable chip at start

#led = Pin(25, Pin.OUT)
#led.off()

chip = MCP3008(spi, cs)

state = True

l=[0,0,0,0,0,0,0,0]

i = 0
while True:
    a=[chip.read(7),chip.read(6),chip.read(5),chip.read(4),chip.read(8),chip.read(1),chip.read(2),chip.read(3)]
    d=max(abs(l[0]-a[0]),abs(l[1]-a[1]),abs(l[2]-a[2]),abs(l[3]-a[3]),abs(l[4]-a[4]),abs(l[5]-a[5]),abs(l[6]-a[6]),abs(l[7]-a[7]))
    if (d>20):
        l=a
        #print(d)
        m=[l[0]//16,l[1]//16,l[2]//16,l[3]//16,l[4]//16,l[5]//16,l[6]//16,l[7]//16]
        print(i, end=" ")
        i = i+1
        print(m)
        #if (m[0]>=32 and led.value()==0):
        #    led.on()
        #if (m[0]<32 and led.value()==1):
        #    led.off()
    sleep(0.1)