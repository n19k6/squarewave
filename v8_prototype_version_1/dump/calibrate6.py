from machine import Pin, SPI, Timer
from time import sleep, sleep_ms, ticks_ms, ticks_diff
from math import floor
#from usys import atexit
import usys 

#https://www.ashleysheridan.co.uk/blog/Getting+Discrete+Values+from+a+Potentiometer

def main():
    global p
    p = [7,6,5,4,0,1,2,3]
    
    global mcp3008_spi
    global mcp3008_cs
    global mcp3008_out_buf
    global mcp3008_in_buf
    # initialize
    mcp3008_spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=10000)
    mcp3008_cs = Pin(5, Pin.OUT)
    mcp3008_cs.value(1) # disable chip at start

    mcp3008_cs.value(1) # ncs on
    mcp3008_out_buf = bytearray(3)
    mcp3008_out_buf[0] = 0x01
    mcp3008_in_buf = bytearray(3)
    
    global ox1_freq
    global ox1_duty
    global ox2_freq
    global ox2_duty
    ox1_freq = 0
    ox1_duty = 0
    ox2_freq = 0
    ox2_duty = 0
    s1_shift = 0
    s2_shift = 0
    signal_freq = 0
    
    ox1_ox2_timer = Timer()
    signal_shift_timer = Timer()
    signal_freq_timer = Timer()
    
    bound = [0]*65
    for i in range(65):
        bound[i]=(1024/(64-1))*(i-1)

    def calc_option(option, value):
        direction = 0
        if (value >= (bound[option+1]+10)):
            direction = 1
        if (value <= (bound[option]-10)):
            direction = -1
        option = option+direction
        m_v = value//16
        direction2 = 0
        if option-m_v>2:
            direction2 = m_v-option
        if option-m_v<-2:
                direction2 = m_v-option
        option = option+direction2
        return option

    def tick_ox1_ox2(timer):
        t0 = ticks_ms()
        global ox1_freq
        global ox1_duty
        global ox2_freq
        global ox2_duty
        #global mcp3008_cs
        #global mcp3008_out_buf
        #global mcp3008_in_buf
        #global mcp3008_spi
        #global p
        m4 = mcp3008_read(p[4])
        m5 = mcp3008_read(p[5])
        m6 = mcp3008_read(p[6])
        m7 = mcp3008_read(p[7])
        #print(m)
        #so = co(so, m)
        new_ox1_freq = calc_option(ox1_freq, m4)
        new_ox1_duty = calc_option(ox1_duty, m5)
        new_ox2_freq = calc_option(ox2_freq, m6)
        new_ox2_duty = calc_option(ox2_duty, m7)
        
        diff = int(new_ox1_freq != ox1_freq)+int(new_ox1_duty != ox1_duty)+int(new_ox2_freq != ox2_freq)+int(new_ox2_duty != ox2_duty)
        #print(diff)
        if (diff != 0):
            t1 = ticks_ms()
            #print(so,m1, ticks_diff(t1, t0))
            #print((new_ox1_freq, ticks_diff(t1, t0)), m4, m4//16)
            print((diff, ticks_diff(t1, t0)),(new_ox1_freq, new_ox1_duty, new_ox2_freq, new_ox2_duty))
            ox1_freq = new_ox1_freq
            ox1_duty = new_ox1_duty
            ox2_freq = new_ox2_freq
            ox2_duty = new_ox2_duty            
    
    print("a1")
    ox1_ox2_timer.init(freq=10, mode=Timer.PERIODIC, callback=tick_ox1_ox2)
    print("a2")
    sleep(40)
    ox1_ox2_timer.deinit()

def main2():
    
    usys.exit(1)
    
    global mcp3008_spi
    global mcp3008_cs
    global mcp3008_out_buf
    global mcp3008_in_buf
    # initialize
    mcp3008_spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=10000)
    mcp3008_cs = Pin(5, Pin.OUT)
    mcp3008_cs.value(1) # disable chip at start

    mcp3008_cs.value(1) # ncs on
    mcp3008_out_buf = bytearray(3)
    mcp3008_out_buf[0] = 0x01
    mcp3008_in_buf = bytearray(3)
    
    global m
    m = [7,6,5,4,0,1,2,3]
    
    led = Pin(25, Pin.OUT)
    led.off()
    
    o = 64
    so = 0
    t = 3
    for i in range(600):
        t0 = ticks_ms()
        m = mcp3008_read(7)
        so = co(so, m)
        #print(so)
        t1 = ticks_ms()
        m1, m2 = divmod(m,16)
        print(so,m1, ticks_diff(t1, t0))
        if so-m1>2:
            so=m1+0
            print("a1", so)
        else:
            if so-m1<-2:
                so=m1-0
                print("a2", so)
        sleep(0.1)
    #sleep(1)
    #measure(10)
    #sleep(1)
    #measure(20)
    #sleep(1)
    #measure(40)
    #sleep(1)
    #measure(80)
    #sleep(1)
    #measure(160)
    
def co(co, iv):
    if(iv >= (ov(co+1)+10)):
        co = co+1
    else:
        if (iv <= (ov(co)-10)):
            co = co-1
    return co

def ov(cu):
    global o
    return (1024/(64-1))*(cu-1)

def measure(n):
    min_all = [1023,1023,1023,1023,1023,1023,1023,1023]
    max_all = [0,0,0,0,0,0,0,0]
    abs_all = [0,0,0,0,0,0,0,0]
    
    for i in range(n):
        m = mcp3008_read_all()
        for index,item in enumerate(m):
            min_all[index] = min(min_all[index], item)
            max_all[index] = max(max_all[index], item)
        sleep(0.1)
    print(min_all)
    print(max_all)
    for index,item in enumerate(abs_all):
        abs_all[index] = abs(min_all[index]-max_all[index])
    print(abs_all)

def mcp3008_read_all():
    return [mcp3008_read(m[0]), mcp3008_read(m[1]), mcp3008_read(m[2]), mcp3008_read(m[3]), \
            mcp3008_read(m[4]), mcp3008_read(m[5]), mcp3008_read(m[6]), mcp3008_read(m[7])]

def mcp3008_read(pin):
    '''this is the doc string of the function'''
    global mcp3008_spi
    global mcp3008_cs
    global mcp3008_out_buf
    global mcp3008_in_buf
    
    mcp3008_cs.value(0) # select
    mcp3008_out_buf[1] = ((not False) << 7) | (pin << 4)
    mcp3008_spi.write_readinto(mcp3008_out_buf,mcp3008_in_buf)
    mcp3008_cs.value(1) # turn off
    return ((mcp3008_in_buf[1] & 0x03) << 8) | mcp3008_in_buf[2]


if __name__ == '__main__':
   
    print("invoking main")
    main()
    print("end of program")
   

#led = Pin(25, Pin.OUT)
#led.off()

#chip = MCP3008(spi, cs)

#state = True

#l=[0,0,0,0,0,0,0,0]

#while True:
    #in_0.value(state)
    #in_1.value(not state)
    #sleep(0.05)
    #state = not state
    #actual_0 = chip.read(0)
    #actual_1 = chip.read(1)
    #actual_2 = chip.read(2)
    #actual_3 = chip.read(3)
    #actual_4 = chip.read(4)
    #actual_5 = chip.read(5)
    #actual_6 = chip.read(6)
    #actual_7 = chip.read(7)
    #print(actual_0, end='')
    #print(","+str(actual_1))
    
    #print(str(actual_0)+","+str(actual_1)+","+str(actual_2)+","+str(actual_3)+","+str(actual_4)+","+str(actual_5)+","+str(actual_6)+","+str(actual_7))
    #a=[chip.read(0),chip.read(1),chip.read(2),chip.read(3),chip.read(4),chip.read(5),chip.read(6),chip.read(7)]
 #   a=[chip.read(7),chip.read(6),chip.read(5),chip.read(4),chip.read(0),chip.read(1),chip.read(2),chip.read(3)]
    #d=(l[0]-a[0])**2+(l[1]-a[1])**2+(l[2]-a[2])**2+(l[3]-a[3])**2+(l[4]-a[4])**2+(l[5]-a[5])**2+(l[6]-a[6])**2+(l[7]-a[7])**2
   # d=max(abs(l[0]-a[0]),abs(l[1]-a[1]),abs(l[2]-a[2]),abs(l[3]-a[3]),abs(l[4]-a[4]),abs(l[5]-a[5]),abs(l[6]-a[6]),abs(l[7]-a[7]))
  #  if (d>20):
    #    l=a
        #print(d)
     #   m=[l[0]//16,l[1]//16,l[2]//16,l[3]//16,l[4]//16,l[5]//16,l[6]//16,l[7]//16]
      #  print(m)
       # if (m[0]>=32 and led.value()==0):
          #  led.on()
       # if (m[0]<32 and led.value()==1):
        #    led.off()
   # sleep(0.1)
