#
# init controller, init signal generators (start signals immediatly)
#
#
#
#
#
#
#
#
#
#
# https://www.ashleysheridan.co.uk/blog/Getting+Discrete+Values+from+a+Potentiometer

from machine import Pin, SPI, Timer
from time import sleep

class Configuration():
    
    LAMBDA1_PIN = 2
    
    LAMBDA1_DUTY_VALUE = 0
    LAMBDA1_FREQ_VALUE = 1
    
#mcp3008.py
class MCP3008:
    """Access MCP3008 and read potentiometer values."""

    def __init__(self, spi, cs):
        self.cs = cs
        self.cs.value(1) # ncs on
        self._spi = spi
        self._out_buf = bytearray(3)
        self._out_buf[0] = 0x01
        self._in_buf = bytearray(3)

    def read(self, pin):
        self.cs.value(0) # select
        self._out_buf[1] = ((True) << 7) | (pin << 4)
        self._spi.write_readinto(self._out_buf, self._in_buf)
        self.cs.value(1) # turn off
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]


# controller.py
class Controller():
    """Reads potentiometer values and propagates changes towards signal generators."""

    def __init__(self):
        self._observers = []
        self._spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=10000)
        self._cs = Pin(5, Pin.OUT)
        self._cs.value(1) # disable chip at start
        self._adc = MCP3008(self._spi, self._cs)
        self._partition = []
        for channel in range(8):
            self._partition.append(self._adc.read(channel)//16)
        self._bound = []
        for i in range(65):
            self._bound.append(int((1024/(64-1))*(i-1)))
    
    def register(self, observer):
        self._observers.append(observer)
    
    def notify(self, **data):
        for observer in self._observers:
            observer.notify(self, **data)
    
    def partition(self, channel):
        return self._partition[channel]
    
    def f1(self, changed, channels):
        #changed[0] = False
        for i in range(len(channels)):
        #for channel in [0,1]:                
            value = self._adc.read(channels[i])
            option = self._partition[channels[i]]
            direction = 0
            if (value >= (self._bound[option+1]+10)):
                direction = 1
                changed[i] = True
            if (value <= (self._bound[option]-10)):
                direction = -1
                changed[i] = True
            option = option+direction
            m_v = value//16
            direction2 = 0
            if option-m_v>2:
                direction2 = m_v-option
                changed[i] = True
            if option-m_v<-2:
                direction2 = m_v-option
                changed[i] = True
            self._partition[channels[i]] = option+direction2
 
    def update(self, timer):
        changed = [False, False]
        channels = [0, 1]
        self.f1(changed, channels)
        if changed == [True, True]:
            self.notify(part0=self._partition[channels[0]], part1=self._partition[channels[1]])
        if changed == [True, False]:
            self.notify(part0=self._partition[channels[0]])
        if changed == [False, True]:
            self.notify(part1=self._partition[channels[1]])            
            
    def update2(self, timer):
        #print("update")
        changed = False
        for channel in [0,1]:                
            value = self._adc.read(channel)
            option = self._partition[channel]
            direction = 0
            if (value >= (self._bound[option+1]+10)):
                direction = 1
                changed = True
            if (value <= (self._bound[option]-10)):
                direction = -1
                changed = True
            option = option+direction
            m_v = value//16
            direction2 = 0
            if option-m_v>2:
                direction2 = m_v-option
                changed = True
            if option-m_v<-2:
                direction2 = m_v-option
                changed = True
            self._partition[channel] = option+direction2
        if changed:
            print(self._partition)
            self.notify(part0=self._partition[0], part1=self._partition[1])
      
# lambda_signal.py
class LambdaSignal():
    """Generates lambda signals."""

    def __init__(self, controller, sm_id, channel_frequency, channel_duty_cycle, pin):
        controller.register(self)
        self._frequency = controller.partition(channel_frequency)
        self._duty_cycle = controller.partition(channel_duty_cycle)
        # init sm and run
        
    def notify(self, observable, **data):
        print("received: ", data)


def main():
    debug("starting main")
    
    controller = Controller()
    lambda1_signal = LambdaSignal(controller, 1, Configuration.LAMBDA1_FREQ_VALUE, Configuration.LAMBDA1_DUTY_VALUE, Configuration.LAMBDA1_PIN)
    
    adc_timer = Timer()

    adc_timer.init(freq=10, mode=Timer.PERIODIC, callback=controller.update)
    
    sleep(10)
    
    adc_timer.deinit()

def debug(message):
    print("Debug: " + message)

if __name__ == '__main__':
    main()
