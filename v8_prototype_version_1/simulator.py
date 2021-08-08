from machine import Pin, SPI
from time import sleep, sleep_ms
#from mcp3008 import MCP3008
from rp2 import PIO, StateMachine, asm_pio
#from machine import Pin, mem32

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

@rp2.asm_pio(sideset_init=PIO.OUT_LOW)
def pwm_prog():
    #pull(noblock) .side(0)
    pull(noblock)
    mov(x, osr) # Keep most recent pull data stashed in X, for recycling by noblock
    mov(y, isr) # ISR must be preloaded with PWM count max
    jmp(not_x, "continue")
    #jmp("continue")
    #label("null")
    nop().side(0)
    label("continue")
    label("pwmloop")
    jmp(x_not_y, "skip")
    nop()         .side(1)
    label("skip")
    jmp(y_dec, "pwmloop")

class PIOPWM:
    def __init__(self, sm_id, pin, count_freq, max_count=(1 << 16) - 1):
        print(pin)
        self._sm = StateMachine(sm_id, pwm_prog, freq=2 * count_freq, sideset_base=Pin(pin))
        # Use exec() to load max count into ISR
        self._sm.put(max_count)
        self._sm.exec("pull()")
        self._sm.exec("mov(isr, osr)")
        self._sm.active(1)
        self._max_count = max_count
        self._pin = pin

    def _set(self, value):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        if value>self._max_count:
            self._sm.active(0)
            print("off: ", value)
            Pin(self._pin, Pin.OUT).value(1)
        else:
            if not(self._sm.active()):
                self._sm.put(self._max_count)
                self._sm.exec("pull()")
                self._sm.exec("mov(isr, osr)")
                self._sm.active(1)
                print("on: ", value)
            value = max(value, -1)
            value = min(value, self._max_count)
            self._sm.put(value)
        
    def set(self, value):
        # Minimum value is -1 (completely turn off), 0 actually still produces narrow pulse
        value = max(value, -1)
        value = min(value, self._max_count)
        print(value)
        self._sm.put(value)

spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=10000)
cs = Pin(5, Pin.OUT)
cs.value(1) # disable chip at start

led = Pin(25, Pin.OUT)
led.off()

chip = MCP3008(spi, cs)

state = True

a=[chip.read(7),chip.read(6),chip.read(5),chip.read(4),chip.read(0),chip.read(1),chip.read(2),chip.read(3)]
l=a
print([l[0]//16,l[1]//16,l[2]//16,l[3]//16,l[4]//16,l[5]//16,l[6]//16,l[7]//16])

pwm1=PIOPWM(1, 14, 65_79)
#pwm2=PIOPWM(2, 15, 65_7900)

#PIOPWM(2, 15, pwm_prog, max_count=(1 << 16) - 1, count_freq=int(657_900))

pwm1.set(int((1<<16)*(l[2]//16)/64))
#pwm2.set(int((1<<16)*0.75))

#sleep(5)

#pwm1.set(-1)
#pwm2.set(-1)


#sm4.active(0)

while True:
    
    #print(str(actual_0)+","+str(actual_1)+","+str(actual_2)+","+str(actual_3)+","+str(actual_4)+","+str(actual_5)+","+str(actual_6)+","+str(actual_7))
    #a=[chip.read(0),chip.read(1),chip.read(2),chip.read(3),chip.read(4),chip.read(5),chip.read(6),chip.read(7)]
    a=[chip.read(7),chip.read(6),chip.read(5),chip.read(4),chip.read(0),chip.read(1),chip.read(2),chip.read(3)]
    #d=(l[0]-a[0])**2+(l[1]-a[1])**2+(l[2]-a[2])**2+(l[3]-a[3])**2+(l[4]-a[4])**2+(l[5]-a[5])**2+(l[6]-a[6])**2+(l[7]-a[7])**2
    d=max(abs(l[0]-a[0]),abs(l[1]-a[1]),abs(l[2]-a[2]),abs(l[3]-a[3]),abs(l[4]-a[4]),abs(l[5]-a[5]),abs(l[6]-a[6]),abs(l[7]-a[7]))
    #print(d)
    if (d>20):
        l=a
        #print(d)
        m=[l[0]//16,l[1]//16,l[2]//16,l[3]//16,l[4]//16,l[5]//16,l[6]//16,l[7]//16]
        print(m)
        pwm1.set(int((1<<16)*(m[0])/64))
        if (m[0]>=32 and led.value()==0):
            led.on()
        if (m[0]<32 and led.value()==1):
            led.off()
    sleep(0.05)