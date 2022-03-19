from machine import Pin
from machine import PWM
from time import sleep

led = Pin(25, Pin.OUT)
pwm_c1 = PWM(Pin(16))
pwm_c2 = PWM(Pin(17))


led.toggle()

pwm_c1.freq(1000)
pwm_c1.duty_u16(int(65025/2))

pwm_c2.freq(1000)
pwm_c2.duty_u16(int(65025/4))

sleep(10)
