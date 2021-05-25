from machine import Pin, mem32
from rp2 import PIO, StateMachine, asm_pio
from time import sleep


@asm_pio(sideset_init=PIO.OUT_LOW)
def _pwm_prog():
    pull(noblock) .side(0)
    mov(x, osr) # Keep most recent pull data stashed in X, for recycling by noblock
    mov(y, isr) # ISR must be preloaded with PWM count max
    label("pwmloop")
    jmp(x_not_y, "skip")
    nop()         .side(1)
    label("skip")
    jmp(y_dec, "pwmloop")
    
@asm_pio(sideset_init=PIO.OUT_LOW)
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
    def __init__(self, sm_id, pin, max_count, count_freq):
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

# Pin 25 is LED on Pico boards
#5_000 -> 0.076 Hz
#6_579 -> 0.1 Hz
#65_790 -> 1 Hz
#657_900 -> 10 Hz
#6_579_000 -> 100 Hz

SM0_CLKDIV = 0x50200000 + 0x0c8

Pin(17, Pin.OUT).value(0)
Pin(17, Pin.OUT).value(1)
pwm = PIOPWM(0, 16, max_count=(1 << 16) - 1, count_freq=657_900)
Pin(17, Pin.OUT).value(0)

print(bin(mem32[SM0_CLKDIV]))

CLKDIV_6_579 =     0b100101000110111110110000000000
CLKDIV_65_790 =    0b000011101101011111111000000000
CLKDIV_657_900 =   0b000000010111101111111100000000
CLKDIV_6_579_000 = 0b000000000010010111111100000000

#mem32[SM0_CLKDIV]=0b01111101000000000000000

for i in range(2):
    
    if i == 0:
        mem32[SM0_CLKDIV]=mem32[SM0_CLKDIV]
    if i == 1:
        mem32[SM0_CLKDIV]=CLKDIV_6_579_000
        
        
    Pin(17, Pin.OUT).value(1)
    pwm.set(1<<15)
    sleep(0.6)
    Pin(17, Pin.OUT).value(0)
    Pin(17, Pin.OUT).value(1)
    pwm.set(0)
    sleep(0.6)
    Pin(17, Pin.OUT).value(0)
    Pin(17, Pin.OUT).value(1)
    pwm.set(-1)
    sleep(0.6)
    Pin(17, Pin.OUT).value(0)
    Pin(17, Pin.OUT).value(1)
    # 75%
    pwm.set(int((1<<15)*1.5))
    sleep(0.6)
    Pin(17, Pin.OUT).value(0)
    Pin(17, Pin.OUT).value(1)
    pwm.set(-1)
    sleep(0.6)
    Pin(17, Pin.OUT).value(0)

#while True:
#for i in range(2 ** 8):
#    pwm.set(i ** 2)
#    sleep(0.01)

    
pwm._sm.active(0)