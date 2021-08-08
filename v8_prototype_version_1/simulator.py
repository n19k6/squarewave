from machine import Pin, SPI
from time import sleep, sleep_ms


def main():
    
    print(type(mcp3008_spi))
    print(type(mcp3008_cs))
    print(type(mcp3008_out_buf))
    print(type(mcp3008_in_buf))
    
    mcp3008_cs.value(0) # select
    print(mcp3008_cs.value())
    mcp3008_out_buf[1] = ((not False) << 7) | (0 << 4)
    mcp3008_spi.write_readinto(mcp3008_out_buf,mcp3008_in_buf)
    mcp3008_cs.value(1) # turn off
    print(mcp3008_cs.value())
    print( ((mcp3008_in_buf[1] & 0x03) << 8) | mcp3008_in_buf[2])
    #print("read(0) {}".format(read(0))
    #print("Before: b={}".format(b))
    

def mcp3008_read(pin):
    '''this is the doc string of the function'''
    global mcp3008_spi
    global mcp3008_cs
    global mcp3008_out_buf
    global mcp3008_in_buf
    
    print(mcp3008_cs.value())
    
    mcp3008_cs.value(0) # select
    print(mcp3008_cs.value())
    mcp3008_out_buf[1] = ((not False) << 7) | (pin << 4)
    mcp3008_spi.write_readinto(mcp3008_out_buf,mcp3008_in_buf)
    mcp3008_cs.value(1) # turn off
    return ((mcp3008_in_buf[1] & 0x03) << 8) | mcp3008_in_buf[2]


if __name__ == '__main__':
   
    print("start")

    # initialize
    mcp3008_spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=10000)
    mcp3008_cs = Pin(5, Pin.OUT)
    mcp3008_cs.value(1) # disable chip at start

    mcp3008_cs.value(1) # ncs on
    mcp3008_out_buf = bytearray(3)
    mcp3008_out_buf[0] = 0x01
    mcp3008_in_buf = bytearray(3)
    
    print(mcp3008_read(7))
    
    print("ende")
   

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
