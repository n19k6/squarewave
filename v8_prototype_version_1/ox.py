from machine import Pin, SPI
from time import sleep, sleep_ms
#from mcp3008 import MCP3008
from rp2 import PIO, StateMachine, asm_pio
#from machine import Pin, mem32

# document pwm_prog

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


led = Pin(25, Pin.OUT)
led.off()

pwm1=PIOPWM(1, 14, 65_7900)
led.on()
#pwm2=PIOPWM(2, 15, 65_7900)

#PIOPWM(2, 15, pwm_prog, max_count=(1 << 16) - 1, count_freq=int(657_900))
sleep(20)
pwm1._set(-1)
#pwm1.set(int((1<<16)*(l[2]//16)/64))
#pwm2.set(int((1<<16)*0.75))
led.off()
#sleep(5)

#pwm1.set(-1)
#pwm2.set(-1)


