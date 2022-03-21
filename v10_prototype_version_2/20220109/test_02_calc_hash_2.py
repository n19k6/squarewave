#freq_list = [5,10,100]
freq_list = [2.5,2.5,4.166,5,5,6.666,7.5,8.333,9.166,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100]
if len(freq_list)<3:
    raise Exception("freq_list to short")
if len(freq_list)>64:
    raise Exception("freq_list to long")

# hack first element will be ignored
# 0.4 exception fValueError: freq out of range
pwm_list = [0.4,0.4,1,10]
if len(pwm_list)<3:
    raise Exception("pwm_list to short")
if len(pwm_list)>64:
    raise Exception("pwm_list to long")


freq_list2 = [0]*64
k = -1
ad = 0
for i in range(64):
    #print(int((i*len(freq_list))/64))
    j = int((i*len(freq_list))/64)
    #print(i, k, j, freq_list[j])
    if j == k:
        nv = freq_list[min(j+1,len(freq_list)-1)]
        di = nv-freq_list[j]
        dr = di/(64/len(freq_list))
        ad = ad+dr
        #print(i, j, freq_list[j], "-", freq_list[min(j+1,len(freq_list)-1)], ad)
        #print(i, j, freq_list[j]+ad)
        print("*")
        freq_list2[i] = freq_list[j]+ad
    else:
        #print(i, j, freq_list[j], "*")
        freq_list2[i] = freq_list[j]
        ad = 0
    k = j

print(freq_list2)

pwm_list2 = [0]*64
k = -1
ad = 0
for i in range(64):
    #print(int((i*len(freq_list))/64))
    j = int((i*len(pwm_list))/64)
    #print(i, k, j, freq_list[j])
    if j == k:
        nv = pwm_list[min(j+1,len(pwm_list)-1)]
        di = nv-pwm_list[j]
        dr = di/(64/len(pwm_list))
        ad = ad+dr
        #print(i, j, freq_list[j], "-", freq_list[min(j+1,len(freq_list)-1)], ad)
        #print(i, j, freq_list[j]+ad)
        print("*")
        pwm_list2[i] = pwm_list[j]+ad
    else:
        #print(i, j, freq_list[j], "*")
        pwm_list2[i] = pwm_list[j]
        ad = 0
    k = j

print(pwm_list2)

#import sys
#sys.exit(0)

from machine import Pin, mem32
import rp2
from time import sleep

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)

def signal():
    wrap_target()
    #out(x, 1)
    #out(pins, 3)
    #out(pins, 4) [8]
    set(pins, 1) [7] 
    set(pins, 0) [23] # 3 wartetakte (1+23 = 1+7+8+8)
    set(x, 16) [7]
    nop() [23] # 3 wartetakte
    label('loop') 
    nop() [31] # 4 wartetakte
    nop() [23] # 3 wartetakte
    jmp(x_dec, 'loop') [7]
    wrap()

#sm = rp2.StateMachine(0, signal, freq=3_000, out_base=Pin(6))
#sm = rp2.StateMachine(0, signal, freq=173_725, set_base=Pin(9)) # 150.8

# dreisatz 140/150.8*173_725
sm0 = rp2.StateMachine(0, signal, freq=161_283, set_base=Pin(26)) # 140


SM0_CLKDIV = 0x50200000 + 0x0c8


clk_div_list = []
clk_freq_list = []
clk_rpm_list = []

for i in range(64):
    j = i+1
    #k = int((140*j)/64)
    k = freq_list2[i]
    f = int((161_283*k)/140)
    #sm = rp2.StateMachine(0, signal, freq=173_725, set_base=Pin(9))
    sm0 = rp2.StateMachine(0, signal, freq=f, set_base=Pin(9))
    b = bin(mem32[SM0_CLKDIV])
    #print(bin(mem32[SM0_CLKDIV]))
    print(j, end=": ")
    print(k, end=" ")
    print(f, end=" ")
    print(b)
    clk_div_list.append(b)
    clk_freq_list.append(str(k) + " Hz")
    clk_rpm_list.append(str(k*60) + " rpm")
    
# dreisatz 140/150.8*173_725
sm1 = rp2.StateMachine(1, signal, freq=161_283, set_base=Pin(26)) # 140


SM1_CLKDIV = 0x50200000 + 0x0e0


pwm_div_list = []
pwm_freq_list = []

for i in range(64):
    j = i+1
    #k = int((140*j)/64)
    k = pwm_list2[i]
    f = int(20018*k)
    print(k,f)
    #sm = rp2.StateMachine(0, signal, freq=173_725, set_base=Pin(9))
    sm1 = rp2.StateMachine(1, signal, freq=f, set_base=Pin(9))
    b = bin(mem32[SM1_CLKDIV])
    #print(bin(mem32[SM0_CLKDIV]))
    print(j, end=": ")
    print(k, end=" ")
    print(f, end=" ")
    print(b)
    pwm_div_list.append(b)
    pwm_freq_list.append(str(k) + " Hz")
    
print()
print("<######################## AB HIER BIS ZUM ENDE KOPIEREN #########################>")
print()
print('from array import array')
print()
print("clk_freq_list = [")
for i in range(63):
    print('    "'+clk_freq_list[i]+'",')
print('    "'+clk_freq_list[63]+'"')
print("]")

print()
print("clk_rpm_list = [")
for i in range(63):
    print('    "'+clk_rpm_list[i]+'",')
print('    "'+clk_rpm_list[63]+'"')
print("]")

print()
print('clk_div_list = array("I", [0 for _ in range(64)])')
print()
for i in range(64):
    #print(clk_freq_list[i])
    print("clk_div_list["+str(i)+"] = "+pwm_div_list[i])

print()
print("pwm_freq_list = [")
for i in range(63):
    print('    "'+pwm_freq_list[i]+'",')
print('    "'+pwm_freq_list[63]+'"')
print("]")

print()
print('pwm_div_list = array("I", [0 for _ in range(64)])')
print()
for i in range(64):
    #print(clk_freq_list[i])
    print("pwm_div_list["+str(i)+"] = "+pwm_div_list[i]) 