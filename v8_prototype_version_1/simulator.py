from machine import Pin, SPI
from time import sleep, sleep_ms, ticks_ms
from math import floor

def main():
    
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
    
    #a=[chip.read(7),chip.read(6),chip.read(5),chip.read(4),chip.read(0),chip.read(1),chip.read(2),chip.read(3)]
    global m
    m = [7,6,5,4,0,1,2,3]
    
    led = Pin(25, Pin.OUT)
    led.off()
    sleep(1)
    last_measurement = mcp3008_read_all()
    
    c = 0
    print(c,last_measurement); c=c+1
    
    last_value = [last_measurement[0]//16, last_measurement[1]//16, last_measurement[2]//16, last_measurement[3]//16, \
                  last_measurement[4]//16, last_measurement[5]//16, last_measurement[6]//16, last_measurement[7]//16]
    
    led.value(last_value[3]//512)
    
    #print(mcp3008_read(m[0]))
    min_1 = 1023
    max_1 = 0
    
    while True:
        #t0=ticks_ms()
        #t1=ticks_ms()
        current_measurement = mcp3008_read_all()
        #t1=ticks_ms()
        # TODO: auftrennen nach kanaelen!!!
        current_value = [current_measurement[0]//16, current_measurement[1]//16, current_measurement[2]//16, current_measurement[3]//16, \
                         current_measurement[4]//16, current_measurement[5]//16, current_measurement[6]//16, current_measurement[7]//16]
        distance = max(abs(current_measurement[0]-last_measurement[0]), \
                       abs(current_measurement[1]-last_measurement[1]), \
                       abs(current_measurement[2]-last_measurement[2]), \
                       abs(current_measurement[3]-last_measurement[3]), \
                       abs(current_measurement[4]-last_measurement[4]), \
                       abs(current_measurement[5]-last_measurement[5]), \
                       abs(current_measurement[6]-last_measurement[6]), \
                       abs(current_measurement[7]-last_measurement[7]))
        min_1 = min(min_1, current_measurement[6])
        max_1 = max(max_1, current_measurement[6])
        if distance>20:
            #print(c,current_measurement); c=c+1
            print("[",k1(current_value, last_value),"]",c,current_measurement, min_1, max_1); c=c+1
            # led
            if(current_measurement[3]//512 != last_measurement[3]//512):
                led.value(current_measurement[3]//512)
                print("led changed:", current_measurement[3]//512)
            # frequency ox1
            if(current_value[4] != last_value[4]):
                # 0-63 -> 10**(-1-1)
                print("ox1 frequency changed:", floor_precision(10**(translate(current_value[4], 0, 63, -1, 1)),2))
            # duty cycle ox1
            if(current_value[5] != last_value[5]):
                # 0-63 -> 10-90
                print("ox1 duty changed:", int(translate(current_value[5], 0, 63, 10, 90)))
            
            last_measurement = current_measurement
            last_value = current_value
        #t1=ticks_ms()
        #print(t1-t0)
        sleep(0.1)

def k1(a,b):
    i = 0
    for index,item in enumerate(a):
        if a[index] != b[index]:
            i = i+1
    return i

def floor_precision(value, precision):
    return floor(value*(10**precision))/(10**precision)

def translate(value, min_1, max_1, min_2, max_2):
    range_1 = max_1 - min_1
    range_2 = max_2 - min_2
    normalized_value = float(value - min_1) / float(range_1)
    return min_2 + (normalized_value * range_2)

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
