import array, time
from machine import Pin, mem32
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def kurbelwelle():
    pull()
    mov(x, osr)
    label("delay")
    jmp(x_dec, "delay")
    #nop() [2]
    wrap_target()
    set(pins, 1)
    set(pins, 0) [2]
    set(pins, 1)
    set(pins, 0) [1]
    set(x, 31)
    label("zacken")
    set(pins, 1)
    set(pins, 0) [1]
    jmp(x_dec, "zacken")
    nop() [7]
    wrap()


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def nockenwelle():
    pull()
    mov(x, osr)
    label("delay")
    jmp(x_dec, "delay")
    #nop() [3]
    wrap_target()
    set(pins, 1)
    set(pins, 0) [2]
    nop() [31]
    set(pins, 1)
    set(pins, 0) [2]
    nop() [31]
    set(pins, 1)
    #set(pins, 0) [3]
    #nop() [31]
    #set(pins, 0) [3]
    #nop() [31]
    set(pins, 0) [3+3]
    nop() [31]
    nop() [31] 
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_HIGH)
def zuendsignal2():
    pull()
    mov(x, osr)
    label("delay")
    jmp(x_dec, "delay")
    #nop() [4]
    wrap_target()
    set(pins, 0)
    set(pins, 1) [2]
    nop() [31]
    wrap()

# possible frequencies 2000-125_000_000
sm = rp2.StateMachine(1, nockenwelle, freq=1_0_000, set_base=Pin(18))
sm2 = rp2.StateMachine(0, zuendsignal2, freq=1_0_000, set_base=Pin(17))
sm3 = rp2.StateMachine(2, kurbelwelle, freq=1_0_000, set_base=Pin(19))

ADR_PIO0_CTRL = 0x50200000 + 0x000
SM0_ADDR = 0x50200000 + 0x0d4
SM1_ADDR = 0x50200000 + 0x0ec
SM0_CLKDIV = 0x50200000 + 0x0c8
SM1_CLKDIV = 0x50200000 + 0x0e0
SM2_CLKDIV = 0x50200000 + 0x0f8
SM3_CLKDIV = 0x50200000 + 0x110

print(sm)
print(sm2)
print(sm3)

d = 4
d2 = 5
d3 = 0

Pin(16, Pin.OUT).value(0)

#sm.active(1)
#sm2.active(1)

START_SM0 = mem32[SM0_ADDR]
START_SM1 = mem32[SM1_ADDR]

print((mem32[SM0_ADDR]))
print((mem32[SM1_ADDR]))

sm.put(d)
sm2.put(d2)
sm3.put(d3)

mem32[ADR_PIO0_CTRL] = mem32[ADR_PIO0_CTRL] | 0b00000000_00000000_00000111_01110000
mem32[ADR_PIO0_CTRL] = mem32[ADR_PIO0_CTRL] | 0b00000000_00000000_00000000_00000111
print(bin(mem32[ADR_PIO0_CTRL]))

time.sleep(0.5)
# change frequency: change SMx_CLKDIV and use CLKDIV_RESTART

print("high")
Pin(16, Pin.OUT).value(1)

MHZ_1=0b11111010000000000000000
MHZ_2=0b01111101000000000000000

KHZ_10=0b110000110101000000000000000000
KHZ_20=0b011000011010100000000000000000

mem32[SM0_CLKDIV]=KHZ_20
mem32[SM1_CLKDIV]=KHZ_20
mem32[SM2_CLKDIV]=KHZ_20
mem32[ADR_PIO0_CTRL] = 0b00000000_00000000_00000000_00000000

print((mem32[SM0_ADDR]))
print((mem32[SM1_ADDR]))

#mem32[SM0_ADDR] = START_SM0
#mem32[SM1_ADDR] = START_SM1

# necessary to start program from first line of asm code
sm.restart()
sm2.restart()
sm3.restart()

print((mem32[SM0_ADDR]))
print((mem32[SM1_ADDR]))

#print(rp2.asm_pio_encode("nop()[1]", 0))

sm.put(d)
sm2.put(d2)
sm3.put(d3)

mem32[ADR_PIO0_CTRL] = mem32[ADR_PIO0_CTRL] | 0b00000000_00000000_00000111_01110000
mem32[ADR_PIO0_CTRL] = mem32[ADR_PIO0_CTRL] | 0b00000000_00000000_00000000_00000111


time.sleep(0.5)


sm.active(0)
sm2.active(0)
sm3.active(0)
