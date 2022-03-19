import machine
import time

port = machine.UART(0)

i = 0

while True:
    time.sleep(1)
    port.write(str(i)+"\r\n")
    i = i+1
